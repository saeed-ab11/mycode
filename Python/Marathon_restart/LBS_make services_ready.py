import logging
import threading

from Practices.Marathon_restart.utils.marathon import MarathonApp, MarathonGroup, MarathonAPI


class LBSMarathonManager(object):
    def __init__(self, marathon_api, marathon_group_str):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.api = marathon_api
        self.group = MarathonGroup(marathon_group_str)
        self.__scenario = None

    def load_scenario(self, scenario):
        self.__scenario = scenario

    def register_apps(self):
        self.logger.info("Registering applications")

        for step in self.__scenario:
            for action, data in step.items():
                for app in data["apps"]:
                    self.logger.info("Adding {} to the {} group".format(app, self.group.name))
                    self.group.add_app(MarathonApp(app))

    @staticmethod
    def start_threads(threads):
        for thread in threads:
            thread.start()

    @staticmethod
    def wait_for_threads(threads):
        for thread in threads:
            thread.join()

    def run_scenario(self):
        def execution_routine(api, action, app):
            step_metod = getattr(api, action)
            out = step_metod(app)
            self.api.wait_for_app(app, out)

        self.logger.info("Running scenario")
        for step in self.__scenario:
            for action, data in step.items():
                self.logger.info("STEP: {}".format(action))

                if data["threaded"]:
                    thread_list = []
                    for app in data["apps"]:
                        thread_list.append(threading.Thread(target=execution_routine,
                                                            args=(self.api, action, self.group[app])))
                    self.start_threads(thread_list)
                    self.wait_for_threads(thread_list)
                else:
                    for app in data["apps"]:
                        execution_routine(self.api, action, self.group[app])

    def check_deployment(self):
        for name, app in self.group.get_apps():
            try:
                self.logger.info("Getting deployment cfg for {} app...".format(name))
                cfg = self.api.get_configuration(app)

                # Check if instances are more than 0, i.e - application is running
                assert cfg.get("instances") > 0

                # Save the current number of instances
                self.group[name].instances = cfg.get("instances")

                self.logger.info("Getting tasks info for {} app...".format(name))
                for task in self.api.get_tasks_info(app):
                    # Check if the task is running and no any other extra tasks
                    assert task.get("state") == "TASK_RUNNING"

            except AssertionError:
                self.logger.error("{} application is suspended or has other issues".format(name))

        self.logger.info("Deployment is checked, no issues!")

if __name__ == "__main__":
    """
    """
    logging.basicConfig(format="[%(levelname)s] %(asctime)-15s %(message)s", level=logging.INFO)

    lbs_manager = LBSMarathonManager(
        MarathonAPI("http://iwakalua-prov.geovzw.ad.vzwcorp.com:9090/service/mon-marathon-service-two/v2/apps",
                    "dcos", "vzdcos", require_token=True,
                    auth_url="http://iwakalua-prov.geovzw.ad.vzwcorp.com:9090/acs/api/v1/auth/login"),
        "tsu/qafunc")

    scenario = [
        {
            "restart": {
                "apps": ["cassandra1", "cassandra2", "cassandra3"],
                "threaded": True
            }
        },
        {
            "suspend": {
                "apps": ["loc", "submgmt"],
                "threaded": False
            }
        },
        {
            "restart": {
                "apps": ["submgmtinit", "locinit"],
                "threaded": False
            }
        },
        {
            "scale": {
                "apps": ["submgmt", "loc"],
                "threaded": False
            }
        }
    ]

    lbs_manager.load_scenario(scenario)
    lbs_manager.register_apps()
    lbs_manager.check_deployment()
    lbs_manager.run_scenario()
