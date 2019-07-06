from scope import Scope


def sample1(scope_type):
    scope = Scope()
    scope.set_scope(scope_type)
    scope.x = int

    def main():
        scope.x = 14
        f()
        g()

    def f():
        scope.x = 13
        h()

    def g():
        scope.x = 12
        h()

    def h():
        print("print", scope.x)

    main()
