import os
import pathlib


def get_ddl_information():
    dir_path = os.path.join(os.getcwd(), "db-scripts")
    ddl_information = []
    for file in os.listdir(dir_path):
        filename = os.fsdecode(file)
        if filename.endswith('.sql'):
            with open(os.path.join(dir_path, file)) as f:
                ddl_information.append(f.read())

    return ddl_information
