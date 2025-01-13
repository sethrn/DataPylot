import pandas as pd

class SessionData():
    def __init__(self, app):
        self.app = app
        self.DataFrames = {}
        self.imports = set()
        self.Models = []
        self.Outputs = []
        self.current_aboutStep = ""

    def addDataFrame(self, name, df):
        self.DataFrames[name] = df

    def getDataFrame(self, name):
        return self.DataFrames.get(name)

    def getDFNames(self):
        return list(self.DataFrames.keys())

    def getDFFeatures(self, name):
        if not self.DataFrames.get(name).empty:
            return list(self.DataFrames.get(name).columns)

    def addModel(self, model):
        self.Models.append(model)

    def getModels(self):
        return self.Models

    def addOutput(self, text):
        self.Outputs.append(text)
        self.app.code_window.onCodeAdded(len(self.Outputs)-1)

    def deleteOutput(self, index):
        self.Outputs.pop(index)

    def getOutputs(self):
        return self.Outputs

    def getOutput(self, index):
        if 0 <= index < len(self.Outputs):
            return self.Outputs[index]

    def TryAddDataFrame(self, name, filepath):
        try:
            if filepath.endswith(".csv"):
                df = pd.read_csv(filepath)
            elif filepath.endswith(".tsv"):
                df = pd.read_csv(filepath, sep="\t")
            elif filepath.endswith(".xlsx"):
                df = pd.read_excel(filepath)
            elif filepath.endswith(".txt"):
                df = pd.read_csv(filepath, sep="\t", header=None)
            elif filepath.endswith(".json"):
                df = pd.read_json(filepath)
            else:
                return False
            
            self.DataFrames[name] = df
            return True
        except Exception as e:
            return False

    def addImports(self, import_stmt):
        if isinstance(import_stmt, str):
            self.imports.add(import_stmt)
        elif isinstance(import_stmt, (list, set, tuple)):
            self.imports.update(import_stmt)

    def getImports(self):
        return list(self.imports)

    def setAboutStep(self, filepath):
        self.current_aboutStep = filepath

    def getAboutStep(self):
        return self.current_aboutStep


