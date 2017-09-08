class AwesomeSuace:
    def __init__(self,ingredient1,ingredient2):
        # initialize variables
        self.one_part = ingredient1
        self.two_parts = ingredient2

        # something to figure out when an object is created
        self.hot = False

        if ingredient1 == 'seriracha' or ingredient2 == 'seriracha':
            self.hot = True

    def __str__(self):
        return 'One part ' + self.one_part + ' and two parts ' + self.two_parts

as1 = AwesomeSuace('seriracha', 'Mayo')
print as1

