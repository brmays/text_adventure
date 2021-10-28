from os import getcwd
from os.path import join
from sys import exit
import json

class JSONHandler():
    def __init__(self, asset_dir, asset_dict):
        self.asset_dir = asset_dir
        self.asset_dict = asset_dict

    def error_and_exit(self, message):
        print(message)
        input(">")
        exit()

    def populate_classes(self):
        dir = join(getcwd(), self.asset_dir)
        class_list = {}

        for json_file, _class in self.asset_dict.items():
            this_file = ""
            try:
                this_file = open(join(dir, json_file), encoding='utf-8')
            except:
                self.error_and_exit(f"{json_file} is missing. Please check {dir} .")
            data = json.load(this_file)
            json_format_error = f"{json_file} is not formatted correctly. Check example.json"
            if 'assets' not in data: self.error_and_exit(json_format_error)
            this_dict = {}
            for asset in data['assets']:
                if 'name' not in asset: self.error_and_exit(json_format_error)
                this_dict[asset['name']] = asset
            class_list[json_file.split('.')[0]] = (_class(this_dict))
        return class_list
