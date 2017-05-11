from . import _steps
from ..stepcollection.stepcollection import define_steps
from ..stepcollection.substeps import SubSteps
from .i18n import languages

substeps = SubSteps()

define_steps(r"^behave_cmdline\.steps\.naturalsearch\.(?P<lang>[^\.]+)$",
             _steps,
             languages,
             substeps.step)
