import subprocess
from types import SimpleNamespace
import venv


# based on: https://stackoverflow.com/a/60072329

class EnvBuilder(venv.EnvBuilder):

    def __init__(self, *args, **kwargs):
        self.context: SimpleNamespace = SimpleNamespace()
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        self.context = context

    def run_module(self, module_name: str, args: list[str]):
        command = [self.context.env_exe, '-m', module_name] + args
        print(command)
        return subprocess.check_call(command)

    def install_requirements(self, path: str):
        self.run_module('pip', ['install', '-r', path])
