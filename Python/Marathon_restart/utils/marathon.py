from pprint import pprint
import requests
from posixpath import join as urljoin
import json
import logging
import time


class MarathonAPI(object):
    def __init__(self, marathon_url_api, username, password, require_token=False, auth_url=None):
        self.url = marathon_url_api
        self.username = username
        self.password = password
        self.require_token = require_token
        self.auth_url = auth_url
        self.token = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_app_info(self, app):
        if not isinstance(app, MarathonApp):
            raise Exception("Use only MarathonApp object!")
        try:
            headers = dict()
            if self.require_token:
                if not self.token:
                    resp = requests.post(url=self.auth_url, headers={"Content-Type": "application/json"},
                                         data=json.dumps({"uid": self.username, "password": self.password})).json()
                    self.token = resp["token"]

                headers["Authorization"] = "token=" + self.token

            url = urljoin(self.url, app.group, app.name)

            response = requests.get(url=url, auth=(self.username, self.password) if not self.require_token else None,
                                    headers=headers)

            return response.json()
        except Exception as e:
            self.logger.error(e)

    def get_configuration(self, app):
        cfg_dict = dict()

        js = self.get_app_info(app=app)

        # Putting deployment params
        for field in ("id", "instances", "cpus", "disk", "constraints", "mem"):
            cfg_dict[field] = js["app"].get(field)

        return cfg_dict

    def get_tasks_info(self, app):
        hosts_info_list = list()
        js = self.get_app_info(app=app)

        for task in js["app"]["tasks"]:
            hosts_info_list.append({
                "id": task.get("id"),
                "host": task.get("host"),
                "state": task.get("state"),
                "startedAt": task.get("startedAt"),
                "appId": task.get("appId"),
                "ports": task.get("ports"),
                "slaveId": task.get("slaveId"),
                "version": task.get("version")
            })

        return hosts_info_list

    def wait_for_app(self, app, version):
        """
        :param app:
        :param version:
        :return:
        """
        max_tries = 30
        retry = 0
        wait_time = 10

        if not version or type(version) != str:
            self.logger.warning("wait_for_app skipped... no version is given")
            return

        while retry < max_tries:
            try:
                js = self.get_app_info(app=app)
            except:
                continue

            for task in js["app"]["tasks"]:
                if task.get("version") == version and task.get("state") == "TASK_RUNNING":
                    self.logger.info("{} app is up and running".format(app.name))
                    return True

            self.logger.info("{} app is not running yet, waiting 10 sec".format(app.name))
            time.sleep(wait_time)
            retry += 1

    def suspend(self, app):
        self.logger.info("Suspending {}".format(app.name))
        self.scale(app, 0)
        return None

    def scale(self, app, instance_num=None):
        """
        :param app:
        :param instance_num:
        :return:
        """
        self.logger.info("Scaling {}".format(app.name))

        if not isinstance(app, MarathonApp):
            raise Exception("Use only MarathonApp object!")
        try:
            headers = dict()
            if self.require_token:
                if not self.token:
                    resp = requests.post(url=self.auth_url, headers={"Content-Type": "application/json"},
                                         data=json.dumps({"uid": self.username, "password": self.password})).json()
                    self.token = resp["token"]

                headers["Authorization"] = "token=" + self.token

            url = urljoin(self.url, app.group, app.name)

            if type(instance_num) != int:
                self.logger.info("Remapping instances number for {}".format(app.name))
                instance_num = app.instances

            response = requests.put(url=url, auth=(self.username, self.password) if not self.require_token else None,
                                    headers=headers, data=json.dumps(dict(instances=instance_num)))

            return response.json().get("version")
        except Exception as e:
            self.logger.error(e)

    def restart(self, app):
        """
        http://iwakalua-prov.geovzw.ad.vzwcorp.com:9090/service/mon-marathon-service-two/v2/apps//tsu/qafunc/fotainit/restart
        :return:
        """
        self.logger.info("Restarting {}".format(app.name))

        if not isinstance(app, MarathonApp):
            raise Exception("Use only MarathonApp object!")
        try:
            headers = dict()
            if self.require_token:
                if not self.token:
                    resp = requests.post(url=self.auth_url, headers={"Content-Type": "application/json"},
                                         data=json.dumps({"uid": self.username, "password": self.password})).json()
                    self.token = resp["token"]

                headers["Authorization"] = "token=" + self.token

            url = urljoin(self.url, app.group, app.name, "restart")

            response = requests.post(url=url, auth=(self.username, self.password) if not self.require_token else None,
                                     headers=headers, data=json.dumps(dict(force=False)))

            self.logger.info(response.json())

            return response.json().get("version")

        except Exception as e:
            self.logger.error(e)

    def destroy(self, app):
        """

        :param app:
        :return:
        """
        if not isinstance(app, MarathonApp):
            raise Exception("Use only MarathonApp object!")
        try:
            headers = dict()
            if self.require_token:
                if not self.token:
                    resp = requests.post(url=self.auth_url, headers={"Content-Type": "application/json"},
                                         data=json.dumps({"uid": self.username, "password": self.password})).json()
                    self.token = resp["token"]

                headers["Authorization"] = "token=" + self.token

            url = urljoin(self.url, app.group, app.name)

            response = requests.delete(url=url, auth=(self.username, self.password) if not self.require_token else None,
                                       headers=headers)

            return response.json()
        except Exception as e:
            print(e)


class MarathonApp(object):
    def __init__(self, name):
        self.name = name
        self.__instances = None
        self.__group = None

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, name):
        self.__group = name

    @group.deleter
    def group(self):
        self.__group = None

    @property
    def instances(self):
        return self.__instances

    @instances.setter
    def instances(self, value):
        self.__instances = value


class MarathonGroup(object):
    def __init__(self, name):
        self.name = name
        self.apps = dict()

    def add_app(self, app):
        if not isinstance(app, MarathonApp):
            raise Exception("Cannot add non-MarathonApp object!")
        self.apps[app.name] = app
        app.group = self.name

    def get_apps(self):
        return self.apps.items()

    def __setitem__(self, key, value):
        self.apps[key] = value

    def __getitem__(self, item):
        return self.apps.get(item)

if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s] %(asctime)-15s %(message)s", level=logging.DEBUG)

    m_api = MarathonAPI("http://iwakalua-prov.geovzw.ad.vzwcorp.com:9090/service/mon-marathon-service-two/v2/apps",
                        "dcos", "vzdcos", require_token=True,
                        auth_url="http://iwakalua-prov.geovzw.ad.vzwcorp.com:9090/acs/api/v1/auth/login")

    # Creating group
    qafunc_group = MarathonGroup("tsu/qafunc")

    # Creating apps
    loc_app = MarathonApp("loc")
    qafunc_group.add_app(loc_app)

    # Using marathon api to get some info
    for name, app in qafunc_group.get_apps():
        print("Getting deployment cfg for {} app...".format(name))
        pprint(m_api.get_configuration(app), indent=4)
        print("Getting tasks info for {} app...".format(name))
        pprint(m_api.get_tasks_info(app), indent=4)
        print("-" * 80)

        version = m_api.restart(app)
        m_api.wait_for_app(app, version=version)