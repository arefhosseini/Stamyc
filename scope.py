class Scope(object):
    def __init__(self):
        object.__setattr__(self, "variables", {})

    def set_scope(self, scope_type):
        self.scope_type = scope_type

    def __setattr__(self, attr, value):
        print("set", attr, value)
        self.variables[attr] = value

    def __getattr__(self, attr):
        if attr not in self.variables:
            raise AttributeError
        else:
            return self.variables[attr]