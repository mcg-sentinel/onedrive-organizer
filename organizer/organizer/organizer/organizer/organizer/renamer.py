import datetime
import os

class Renamer:
    def __init__(self, config):
        self.pattern = config["naming"]["pattern"]
        self.default_department = config["naming"].get("default_department", "GEN")
        self.default_project = config["naming"].get("default_project", "MISC")

    def suggest_name(self, file_info):
        dept = file_info.get("department", self.default_department)
        project = file_info.get("project", self.default_project)
        date = file_info.get("modifiedDate", datetime.datetime.utcnow())
        version = file_info.get("version", "v01")
        ext = os.path.splitext(file_info["name"])[1].lstrip(".")
        new_name = self.pattern.format(
            department=dept,
            project=project,
            date=date,
            version=version,
            ext=ext,
        )
        return new_name
