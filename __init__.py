"""
Blender pseudo vertical text: emulate support for vertical writing.

Copyright (C) 2021 Kisaragi Hiu <mail@kisaragi-hiu.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import bpy
from .blender_pseudo_vertical_text import (
    ToVerticalOperator,
    ToHorizontalOperator,
    PseudoVerticalPanel,
)


bl_info = {
    "name": "Pseudo vertical writing",
    "description": "Simulate CJK vertical writing with newlines",
    "author": "Kisaragi Hiu",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Item",
    "category": "Object",
}


def register():
    bpy.utils.register_class(ToVerticalOperator)
    bpy.utils.register_class(ToHorizontalOperator)
    bpy.utils.register_class(PseudoVerticalPanel)


def unregister():
    bpy.utils.unregister_class(ToVerticalOperator)
    bpy.utils.unregister_class(ToHorizontalOperator)
    bpy.utils.unregister_class(PseudoVerticalPanel)


if __name__ == "__main__":
    register()
