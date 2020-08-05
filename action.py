
class Action(object):
    def __init__(self, name, function, description = None, arguments = []):
        self.name = name
        self.function = function
        self.description = description
        self.arguments = arguments

    def getname(self):
        return self.name
    
    def getdescription(self):
        return self.description

    def execute(self, messagecallback, arguments):
        return self.function(messagecallback, arguments)

