import imp
import inspect
import sys
import re

from behave import step

from . import _steps
from .i18n import languages


class BehaveCmdlineStepsLoader:
    def __init__(self, translation):
        self.translation = translation

    def load_module(self, fullname):
        try:
            return sys.modules[fullname]
        except KeyError:
            pass

        module = imp.new_module(fullname)
        module.__file__ = _steps.__file__
        module.__doc__ = _steps.__doc__
        module.__path__ = []
        module.__loader__ = self

        members = inspect.getmembers(_steps, inspect.isfunction)
        for name, value in members:
            translations = self.translation[name]
            for text in reversed(translations):
                value = step(text)(value)
            setattr(module, name, value)

        sys.modules.setdefault(fullname, module)
        return module


class BehaveCmdlineStepsFinder:
    module_pattern = re.compile(
        r"^behave_cmdline\.steps\.(?P<lang>[^\.]+)$")

    def find_module(self, fullname, path=None):
        match = self.module_pattern.match(fullname) 
        if match:
            request_lang = match.group("lang")
            try:
                translation = languages[request_lang]
            except KeyError:
                return None
            else:
                return BehaveCmdlineStepsLoader(translation)
        else:
            return None

__all__ = []
__path__ = []
sys.meta_path.append(BehaveCmdlineStepsFinder())
