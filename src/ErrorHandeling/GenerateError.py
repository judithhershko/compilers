# from colorama import Fore
#
# def printError(error):
#     print(Fore.RED + error)


class Undeclared(Exception):
    def __init__(self, unresolved):
        self.unresolved = unresolved

    def __str__(self):
        err = ""
        for elem in self.unresolved:
            err = err + "\n\tError: Line " + str(elem[1]) + " has an undefined " + str(elem[0])
        return err
