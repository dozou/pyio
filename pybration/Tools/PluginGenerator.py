# -*- coding: utf-8 -*-
import sys
import os


class PluginGenerator:
    def __init__(self):
        self.info = dict()
        self.info['plugin_name'] = None
        self.info['dir_name'] = None
        self.info['author'] = None
        self.info['button'] = None
        self.info['module'] = "App"
        self.info['version'] = "0.0"
        self.info['directory'] = None
        self.info_check = False

    def check(self):
        print("")
        print("")
        print("")
        for i in self.info:
            if self.info[i] is None:
                raise ValueError("please check is '%s'" % i)
            print("[%s]: %s"%(i, self.info[i]))
        self.info_check = True

    def generate(self):
        self.__mkdir()
        self.__mk_yapsy_file()
        self.__mk_python_file()
        pass

    def __mkdir(self):
        os.mkdir(self.info['dir_name'])

    def __mk_yapsy_file(self):
        file_name = self.info['dir_name'] + "/" + self.info['plugin_name'] + ".yapsy-plugin"
        print(file_name)
        with open(file_name, "w") as file:
            file.write("[Core]\n")
            file.write("Name = %s\n" % self.info['plugin_name'])
            file.write("Module = %s\n" % self.info['module'])
            file.write("\n\n")
            file.write("[Documentation]\n")
            file.write("Author = %s\n" % self.info['author'])
            file.write("Version = %s\n" % self.info['version'])

    def __mk_python_file(self):
        file_name = self.info['dir_name'] + "/" + self.info['module'] + ".py"
        template_file = os.path.dirname(os.path.abspath(__file__)) + "/plugin_basis.py"
        with open(template_file, 'r') as file:
            template = file.read()

        for i in self.info:
            template = template.replace("$%s$" % i, self.info[i])

        with open(file_name,"w") as file:
            file.write(template)


def pyb_create():
    # print(os.getcwd())
    print(os.path.dirname(os.path.abspath(__file__)))
    plugin_obj = PluginGenerator()
    print("-----------------------------")
    print("| Pybration Plugin Generator |")
    print("-----------------------------")

    print("[plugin name]: ", end="")
    plugin_obj.info['plugin_name'] = input()
    plugin_obj.info['dir_name'] = plugin_obj.info['plugin_name'].lower()

    print("[author]: ", end="")
    plugin_obj.info['author'] = input()

    print("Do you use button function? [y/n]: ", end='')
    s = input()
    if s == 'y':
        plugin_obj.info["button"] = "True"
    else:
        plugin_obj.info['button'] = "False"

    plugin_obj.info['directory'] = os.getcwd()

    plugin_obj.check()
    plugin_obj.generate()


if __name__ == '__main__':
    pyb_create()
