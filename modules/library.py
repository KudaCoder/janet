from collections import defaultdict

from dataclasses_json import dataclass_json
from dataclasses import dataclass, field
from typing import List, Dict
import importlib
import inspect
import json
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
APP_DIR = os.environ.get("APP_DIR")
CONF_DIR = os.environ.get("CONF_DIR")


@dataclass_json
@dataclass
class App:
    name: str
    module: str
    _class: str
    method: str
    janet_input: bool
    thread_q: bool
    args: List = field(default_factory=list)
    kwargs: Dict = field(default_factory=dict)

    def get_class(self):
        module = importlib.import_module(self.module)
        _cls = getattr(module, self._class)
        return _cls


class AppController:
    def __init__(self):
        self.root_dir = os.path.abspath(os.curdir)
        self.app_dir = f"{self.root_dir}/{APP_DIR}"
        self.conf_dir = os.path.join(self.root_dir, CONF_DIR)
        self.app_conf = os.path.join(self.conf_dir, "apps.json")
        self.app_dict = {}
        self.update_library()

    def add(
        self,
        app_name,
        keyword,
        module=None,
        _class=None,
        method=None,
        janet_input=False,
        thread_q=False,
        args=[],
        kwargs={},
    ):
        if not self.app_dict:
            self.app_dict = dict()

        new_app = App(
            app_name, module, _class, method, janet_input, thread_q, args, kwargs
        )
        new_app_dict = new_app.to_dict()
        func = {keyword: new_app_dict}

        # If the app exists then add the new function
        if app_name in self.app_dict.keys() and func not in self.app_dict[app_name]:
            self.app_dict[app_name].append(func)
        # If the app doesn't exist then add app & function
        else:
            self.app_dict.update({app_name: [func]})

        with open(self.app_conf, "w") as f:
            json.dump(self.app_dict, f)

    def select(self, keywords):
        """
        This only works for single nested commands in apps.json
        """
        app = None
        if self.app_dict is not None:
            # Find the specific app name
            for k in self.app_dict.keys():
                if any(w for w in keywords if w == k):
                    app = self.app_dict[k]
                    break
        # Once app is found, loop through keywords to determine function
        func = None
        if app is not None:
            for idx, array in enumerate(app):
                keyword = list(array.keys())[0]
                if any(w for w in keywords if w == keyword):
                    func = app[idx][keyword]
                    func = App.from_dict(func)

        return func

    def update_library(self):
        apps = [
            f
            for f in os.listdir(self.app_dir)
            if os.path.isfile(os.path.join(self.app_dir, f))
        ]
        controllers = []
        modules = []
        for app in apps:
            module_name = app.split(".py")[0]
            module = importlib.import_module(f"modules.apps.{module_name}")
            controllers += [
                c for c in inspect.getmembers(module) if "Controller" in c[0]
            ]
            modules.append(module_name)

        for i, controller in enumerate(controllers):
            app_conf = defaultdict(list)
            command_names = controller[1].commands
            for app_name, commands in command_names.items():
                app_conf[app_name] = []
                for command in commands:
                    method = command["method"]
                    for key in command["keywords"]:
                        keyword = list(key.keys())[0]
                        janet_input, thread_q, args, kwargs = key[keyword].values()
                        app_conf[app_name].append(
                            {
                                keyword: {
                                    "module": module.__name__,
                                    "_class": controller[0],
                                    "method": method,
                                    "janet_input": janet_input,
                                    "thread_q": thread_q,
                                    "args": args,
                                    "kwargs": kwargs,
                                }
                            }
                        )
            with open(f"{self.conf_dir}/apps/{modules[i]}.json", "w") as f:
                json.dump(app_conf, f)

        for conf in os.listdir(f"{self.conf_dir}/apps"):
            with open(f"{self.conf_dir}/apps/{conf}", "r") as f:
                data = json.loads(f.read())
            for k, v in data.items():
                app_name = k
                for keyword_data in v:
                    keyword = list(keyword_data.keys())[0]
                    data = keyword_data[keyword]
                    self.add(app_name, keyword, **data)

        with open(self.app_conf, "w") as fp:
            json.dump(self.app_dict, fp)

        with open(self.app_conf, "r") as apps:
            self.app_dict = json.loads(apps.read())
