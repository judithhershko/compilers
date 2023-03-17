import pandas as pd


class SymbolTable:  # TODO: ask to add memory location?
    def __init__(self):
        self.table = pd.DataFrame({"Value": pd.Series(dtype="str"),
                                   "Type": pd.Series(dtype="str"),
                                   "Const": pd.Series(dtype="bool"),
                                   "Ref": pd.Series(dtype="str"),
                                   "Level": pd.Series(dtype="int")})

    def addSymbol(self, name, value, symType, const=False, ref=None, level=0, decl=False):
        if (ref is None and level != 0) or (level == 0 and ref is not None):
            return "faulty pointer levels"
        if name not in self.table.index:
            self.table.loc[name] = [value, symType, const, ref, level]
            return "placed"
        else:
            row = self.table.loc[name]
            if decl:
                return "redeclaration"
            elif row["Const"]:
                return "const"
            elif row["Type"] != symType:
                return "type"
            elif row["Level"] != level:
                return "level"
            elif row["Level"] > 0:
                refRow = self.table.loc[ref]
                if refRow["level"] != level - 1:
                    return "pointerLevel"
                self.table.loc[name, ["Value"]] = value
                return "replaced"
            else:
                self.table.loc[name, ["Value"]] = value
                return "replaced"

    def findSymbol(self, name, deref=0):
        if name not in self.table.index:
            return None
        elif deref == 0:
            return self.table.at[name, "Value"]
        elif deref > 0 and self.table.at[name, "type"] == "pointer":
            return self.findSymbol(self.table.at[name, "ref"], deref=deref - 1)
        else:
            return None
