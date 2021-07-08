from itertools import zip_longest
import bpy


# We use a trailing newline as the marker instead of the zero-width
# space, because Blender doesn't actually render the zero-width space
# as zero-width.
def is_pseudo_vertical(text):
    """Is `text` already converted to pseudo vertical writing?
    We use a trailing newline as a marker.
    """
    return text[-1] == "\n"


def convert_to_pseudo_vertical(text, lines_rtl=True):
    """Convert `text`, a horizontal string, to a pseudo vertical writing string.

    If `lines_rtl` is True, "lines" in the vertical text read from right
    to left (default).

    A trailing newline is used as a marker for whether a text is
    already converted or not.
    """
    if is_pseudo_vertical(text):
        return text
    if lines_rtl:
        lines = reversed(text.split("\n"))
    else:
        lines = text.split("\n")
    columns = ["".join(x) for x in zip_longest(fillvalue="　", *lines)]
    newtext = "\n".join(columns) + "\n"  # marker
    return newtext


# Displaying it in the right sidebar under the Item category. This is
# the category "Transform" is in. Some editing commands put themselves
# in the Edit category; I'm not sure which is better.
#
# The ID convention: category_PT_name for panels
# Space type defines what editor it goes in.
#
# Calling self.layout.operator adds an operator as a button to the
# panel. Commands have to be made as operators.
class PseudoVerticalPanel(bpy.types.Panel):
    bl_idname = "ITEM_PT_text_pseudo_vertical"
    bl_label = "Pseudo Vertical Writing"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_category = "Item"

    def draw(self, _context):
        self.layout.operator("object.to_pseudo_vertical")


# The operator. The ID seems to always start with object.?
class PseudoVerticalOperator(bpy.types.Operator):
    bl_idname = "object.to_pseudo_vertical"
    bl_label = "To vertical"
    bl_description = "Convert to vertical writing"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, _context):

        for obj in bpy.context.selected_objects:
            if obj.type == "FONT":
                obj.data.body = convert_to_pseudo_vertical(obj.data.body)

        return {"FINISHED"}


bpy.utils.register_class(PseudoVerticalOperator)
bpy.utils.register_class(PseudoVerticalPanel)
