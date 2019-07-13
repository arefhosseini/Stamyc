from scope import *


def main():
    file = open("samples/1_dynamic.txt", "r")
    if file.mode == "r":
        lines = file.readlines()
        if lines[0].strip() == "dynamic":
            lines.pop(0)
            Scope(Type.DYNAMIC, lines)
        elif lines[0].strip() == "static":
            lines.pop(0)
            Scope(Type.STATIC, lines)
        else:
            raise ValueError('First line should be static or dynamic')


if __name__ == "__main__":
    main()
