import pandas as pd
import sys


class symbolTable():
    def __init__(self):
        self.table = pd.DataFrame({"Value": pd.Series(dtype="str"),
                                   "Type": pd.Series(dtype="str"),
                                   "Const": pd.Series(dtype="bool")})

    def addSymbol(self, name, value, symType, const):
        row = self.table.where(self.table["Name"] == name)
        if not row:
            self.table.loc[name] = [value, symType, const]
        else:
            if row["Const"]:
                print("This variable is an already defined const", file=sys.stderr)
            elif row["Type"] != symType:
                print("This variable is already defined with another type", file=sys.stderr)
            else:
                self.table.loc[name, ["Value"]] = value

    def findSymbol(self, name):
        return self.table.at[name, "Value"]
