#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" This is the engine module of Biovarase. This class  inherit from other classes."""
import sys
import os
import inspect
import datetime
from dbms import DBMS
from tools import Tools
from qc import QC
from westgards import Westgards
from exporter import Exporter
from launcher import Launcher




class Engine(DBMS, Tools, QC, Westgards, Exporter, Launcher,):
    def __init__(self,):
        super().__init__()

        self.no_selected = "Attention!\nNo record selected!"
        self.delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"

    def __str__(self):
        return "class: {0}\nMRO:{1}".format(self.__class__.__name__, [x.__name__ for x in Engine.__mro__])

    def get_python_version(self,):
        return "Python version: %s" % ".".join(map(str, sys.version_info[:3]))

    def busy(self, caller):
        caller.config(cursor="watch")

    def not_busy(self, caller):
        caller.config(cursor="")

    def get_file(self, file):
        """Return full path of the directory where program resides."""
        return os.path.join(os.path.dirname(__file__), file)

    def on_log(self, container, function, exc_value, exc_type, module):

        now = datetime.datetime.now()
        log_text = "{0}\n{1}\n{2}\n{3}\n{4}\n\n".format(now, function, exc_value, exc_type, module)
        log_file = open('log.txt', 'a')
        log_file.write(log_text)
        log_file.close()

    def get_log_file(self):
        path = self.get_file("log.txt")
        self.open_file(path)

    def on_debug(self, module, function, *args):

        now = datetime.datetime.now()
        s = "\n\n{0}\n{1}\n{2}\n\n".format(now, module, function)
        f = open('debug.txt', 'a')
        f.write(s)
        for i in args:
            s = "{0}\n".format(i)
            f.write(s)
        f.close()

    def get_elements(self):

        try:
            path = self.get_file("elements")
            f = open(path, "r")
            e = f.readline()
            f.close()
            return e
        except:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def set_elements(self, elements):

        try:
            with open("elements", "w") as f:
                f.write(str(elements))


        except:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_dimensions(self):

        try:
            d = {}
            path = self.get_file("dimensions")
            with open(path, "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
                    d[currentline[0]] = currentline[1]

            return d
        except:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_ddof(self):
        try:
            path = self.get_file("ddof")
            f = open(path, "r")
            v = f.readline()
            f.close()
            return int(v)
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def set_ddof(self, value):

        try:
            with open("ddof", "w") as f:
                f.write(str(value))

        except:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])


    def get_zscore(self):
        try:
            path = self.get_file("zscore")
            f = open(path, "r")
            v = f.readline()
            f.close()
            return float(v)
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def set_zscore(self, value):
        try:
            with open("zscore", "w") as f:
                f.write(str(value))
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_show_error_bar(self):
        try:
            path = self.get_file("show_error_bar")
            f = open(path, 'r')
            v = f.readline()
            f.close()
            return int(v)
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])


    def set_show_error_bar(self, value):

        try:
            with open("show_error_bar", "w") as f:
                f.write(str(value))

        except:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_icon(self):
        return """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAAXNSR0IArs4c
                  6QAAAPBQTFRFAAAAAGbMas7///8A3/3/qeM7AFrH+v//AF/HAJn//v//ndgA
                  AJgAhJGdipaii5ejhZKeACelwOoSZs0wACmlKC41Y8wwKS81p9s6ACykACSl
                  LasAACmhJKcAdMgA3v3/NbcAa8QAyeoA1PYAAFzJACSk9/wAs+8UEJ8AXMYA
                  ruYA//+bZs0yTLcA2/A6AF/JAGDW//94JSoy////IikyjNgmYGt0m9cF4f//
                  gtUABJsA//9b//9NfN0y5PRgACaiACalX2lzQbMA//7//f8AP7IAACql2/QM
                  Xb8A//+p6P//yOoAAGLWFKkAACWl8fqIerPNswAAAAF0Uk5TAEDm2GYAAAABY
                  ktHRACIBR1IAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3AgREA0rdM
                  kpsgAAAJBJREFUGNNVytUSwjAURdHcpKXQUsHd3d3dHf7/b4CZQHPP215zCPn
                  OsHTdMog9U1UU1RRgE+h3Q0MBSPtK72KT/Ji2EDhS1IlBwgBSj7oAwQ4BXGqd
                  OWO2gPxahrfTP0BQnjVH55j7J+DzspuWOZQ5QH1wKma1ZCPBL7Ao7VmuOqmkH
                  /wSXxWiz7XHf4x84g33ag0Bx8dLigAAAABJRU5ErkJggg=="""


    def get_expiration_date(self, expiration_date):
        return (datetime.datetime.strptime(expiration_date, "%d-%m-%Y").date() - datetime.date.today()).days

    def get_license(self):
        """get license"""
        try:
            path = self.get_file("LICENSE")
            f = open(path, "r")
            v = f.read()
            f.close()
            return v
        except FileNotFoundError:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])


def main():

    foo = Engine()
    print(foo)
    input('end')

if __name__ == "__main__":
    main()
