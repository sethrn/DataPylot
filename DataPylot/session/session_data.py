import pandas as pd
from pathlib import Path
import sys
from config.about_tab_paths import ABOUT_TAB_PATHS 

class SessionData():
    def __init__(self, app):
        self.app = app
        self.DataFrames = {}
        '''
        self.DataFrames = {
            "df_name":  {
                "data":
                "data_idx":
                "previous_data":
            }    
        }
        '''
        self.Outputs = []
        self.imports = set()
        self.Models = {}
        self.current_aboutStep = None

    def addDataFrame(self, name, df):
        existing_data = self.DataFrames[name]["data"] if name in self.DataFrames else None
       
        self.DataFrames[name] = {
            "data": df,
            "data_idx": len(self.Outputs),
            "previous_data": existing_data
        }

    def getDataFrame(self, name):
        return self.DataFrames.get(name, {}).get("data")

    def getDFNames(self):
        return list(self.DataFrames.keys())

    def getDFFeatures(self, name):
        if not self.DataFrames.get(name, {}).get("data", {}).empty:
            return list(self.DataFrames.get(name).get("data").columns)

    # Undo DataFrame change features
    def canUndo(self, index):
        return any(
            meta.get("data_idx") == index and meta.get("previous_data") is not None
            for meta in self.DataFrames.values()
        )

    def getUndoableDataFrameAtIndex(self, index):
        for name, meta in self.DataFrames.items():
            if meta.get("data_idx") == index and meta.get("previous_data") is not None:
                return name
        return None

    def undoDataFrameChange(self, name):
        if name in self.DataFrames:
            meta = self.DataFrames[name]
            if meta.get("previous_data") is not None:
                meta["data"] = meta["previous_data"]
                meta["data_idx"] = None
                meta["previous_data"] = None
        self.app.main_stage.refresh_children()

    # DataFrame deletion
    def deleteDataFrame(self, name):
        self.DataFrames.pop(name, None)

    # Output logic
    def addOutput(self, text):
        self.Outputs.append(text)
        self.app.code_window.onCodeAdded(len(self.Outputs)-1)

    def getOutputs(self):
        return self.Outputs

    def getOutputsLength(self):
        return len(self.Outputs)

    def getOutput(self, index):
        if 0 <= index < len(self.Outputs):
            return self.Outputs[index]

    def deleteOutput(self, index):
        if 0 <= index < len(self.Outputs):
            self.Outputs.pop(index)

            for meta in self.DataFrames.values():
                if meta["data_idx"] == index:
                    meta["previous_data"] = None
                elif meta["data_idx"] is not None and meta["data_idx"] > index:
                    meta["data_idx"] -= 1

    # Importing DataFrame
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

            self.addDataFrame(name, df)
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

    def addModel(self, name, model_type):
        self.Models[name] = model_type

    def getModels(self):
        return list(self.Models.keys())

    def getModelType(self, name):
        return self.Models.get(name)

    def setAboutStep(self, tab_name):
        about_path = ABOUT_TAB_PATHS.get(tab_name, None)
        if about_path:
            self.current_aboutStep = about_path

    def getAboutStep(self):
        if self.current_aboutStep is None:
            self.current_aboutStep = "startup.txt"
        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent

        about_path = base_dir / "edu" / self.current_aboutStep

        return about_path


