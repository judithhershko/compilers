import pandas as pd
import sys


class symbolTable():
    def __init__(self):
        self.table = pd.DataFrame({"Value": pd.Series(dtype="str"),
                                   "Type": pd.Series(dtype="str"),
                                   "Const": pd.Series(dtype="bool")})

    def addSymbol(self, name, value, symType, const):
        if name not in self.table.index:
            self.table.loc[name] = [value, symType, const]
            return "placed"
        else:
            row = self.table.loc[name]
            if row["Const"]:
                return "const"
            elif row["Type"] != symType:
                return "type"
            else:
                self.table.loc[name, ["Value"]] = value
                return "replaced"

    def findSymbol(self, name):
        if name not in self.table.index:
            return None
        return self.table.at[name, "Value"]
