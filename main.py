from type import Type
from copy import deepcopy

program_symbol = "program"
int_symbol = "int"
print_symbol = "print"
open_bracket_symbol = "{"
close_bracket_symbol = "}"
semicolon_symbol = ";"
equal_symbol = "="


class Program:
    def __init__(self, parent=None):
        self.parent = parent
        self.name = ""
        self.variables = {}
        self.commands = []


def get_variable(variable):
    return variable.split(semicolon_symbol)[0]


class Scope:
    def __init__(self, type, lines):
        self.scope_type = type

        self.code = ""
        for line in lines:
            self.code += line
        self.programs = {}
        self.create_programs()
        for p in self.programs:
            if self.programs[p].parent is not None:
                print(p, self.programs[p].parent, self.programs[p].variables, self.programs[p].commands)
            else:
                print(p, "None", self.programs[p].variables, self.programs[p].commands)
        self.run()

    def create_programs(self):
        print(self.code.split())
        commands = self.code.split()
        parent = None
        program = None
        variable = None
        last_command = None
        for index in range(len(commands)):
            command = commands[index]
            if command == program_symbol:
                program = Program(parent)
                last_command = program_symbol
            elif command == open_bracket_symbol:
                parent = program.name
                last_command = None
            elif command == close_bracket_symbol:
                if parent is not None:
                    program = self.programs[parent]
                    parent = program.parent
                    last_command = None
            elif command == int_symbol:
                last_command = int_symbol
            elif command == equal_symbol:
                last_command = equal_symbol
            elif command == print_symbol:
                last_command = print_symbol
            else:
                if last_command == program_symbol:
                    self.programs[command] = program
                    program.name = command
                    last_command = None
                elif last_command == int_symbol:
                    program.variables[get_variable(command)] = 0
                    if semicolon_symbol in command:
                        last_command = None
                    else:
                        variable = get_variable(command)
                elif last_command == equal_symbol:
                    if type(program.variables[variable]) == int:
                        program.commands.append((equal_symbol, variable, int(get_variable(command))))
                        last_command = None
                        variable = None
                elif last_command == print_symbol:
                    program.commands.append((print_symbol, get_variable(command)))
                else:
                    if semicolon_symbol in command:
                        program.commands.append(get_variable(command))
                    else:
                        variable = command
                    last_command = None

    def run(self):
        main_program = None
        for program in self.programs.values():
            if program.parent is None:
                main_program = program
                break
        if self.scope_type == Type.STATIC:
            self.static_scope_running(main_program)
        else:
            self.dynamic_scope_running(main_program)

    def static_scope_running(self, main_program):
        finished = False
        running_programs = {}
        program = deepcopy(main_program)
        running_programs[program.name] = []
        running_programs[program.name].append(program)
        while not finished:
            if program is None:
                finished = True
            else:
                if not program.commands:
                    if program.parent is None:
                        finished = True
                    else:
                        program = running_programs[program.parent][-1]
                else:
                    command = program.commands.pop(0)
                    if print_symbol in command:
                        variable = command[1]
                        print(variable + " = " + str(running_programs[program.parent][-1].variables[variable]))
                    elif equal_symbol in command:
                        variable = command[1]
                        value = command[2]
                        program.variables[variable] = value
                    else:
                        program = deepcopy(self.programs[command])
                        if program.name not in running_programs:
                            running_programs[program.name] = []
                        running_programs[program.name].append(program)

    def dynamic_scope_running(self, main_program):
        pass


def main():
    file = open("sample.txt", "r")
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
