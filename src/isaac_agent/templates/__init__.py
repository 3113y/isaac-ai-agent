"""Templates module for Isaac AI Agent"""

from isaac_agent.templates.lua_skeletons import LuaTemplateManager  # deprecated
from isaac_agent.templates.reference_template import ReferenceTemplate, ReferenceFile
from isaac_agent.templates.patterns import ModArchitectureGuide, FilePattern

__all__ = [
    "LuaTemplateManager",  # deprecated
    "ReferenceTemplate",
    "ReferenceFile",
    "ModArchitectureGuide",
    "FilePattern",
]
