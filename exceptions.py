 # -*- coding:utf-8 -*-

class BeilyException(Exception):

    __c = 0
    __m = ""

    def __init__(self, code, msg):
        self.__c = code
        self.__m = msg

    def code(self):
        return self.__c

    def message(self):
        return self.__m

    def __str__(self):
        return "err(code=" + str(self.__c) + ") " +  self.__m