from . import _steps
from . import process
from .i18n import languages
from .stepcollection.stepcollection import define_steps

define_steps(r"^behave_cmdline\.steps\.(?P<lang>[^\.]+)$",
             _steps,
             languages)
