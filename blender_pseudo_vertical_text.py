from itertools import zip_longest
import bpy


def str_index_empty_string(string, index):
    "Like string[index], but return an empty string on IndexError."
    try:
        return string[index]
    except IndexError:
        return ""


# We use a trailing newline as the marker instead of the zero-width
# space, because Blender doesn't actually render the zero-width space
# as zero-width.
def is_pseudo_vertical(text):
    """Is `text` already converted to pseudo vertical writing?
    We use a trailing newline as a marker.
    """
    return text[-1] == "\n"


def text_to_pseudo_vertical(text, lines_rtl=True):
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


def text_to_horizontal(text, lines_rtl=True):
    """Convert `text` back to horizontal.

    If `lines_rtl` is True, the rightmost column becomes the first line, the
    second rightmost column becomes the second line, and so on (default).
    """
    if not is_pseudo_vertical(text):
        return text
    text = text[0:-1]  # Get rid of the marker
    columns = text.split("\n")
    # I had to do this instead of using zip_longest in order to handle my
    # use case
    max_length = len(max(columns, key=len))
    lines = []
    # Say we have
    #
    #   c a
    #   d b
    #     e
    #
    # We go from the right, extract (a, b, e) and push it onto `lines`,
    # then (c, d, "") (using an empty string as the index is out of bounds)
    # and push it onto `lines`, and so on.
    for i in range(-1, -max_length - 1, -1):
        col = [str_index_empty_string(column, i) for column in columns]
        # We also strip any full-width spaces that we may have added.
        lines.append("".join(col).rstrip("　"))
    if not lines_rtl:
        lines = reversed(lines)
    return "\n".join(lines)


# The operator. The ID seems to always start with object.?
class ToVerticalOperator(bpy.types.Operator):
    bl_idname = "object.to_pseudo_vertical"
    bl_label = "To vertical"
    bl_description = "Convert to vertical writing"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, _context):
        for obj in bpy.context.selected_objects:
            if obj.type == "FONT":
                obj.data.body = text_to_pseudo_vertical(obj.data.body)
        return {"FINISHED"}


class ToHorizontalOperator(bpy.types.Operator):
    bl_idname = "object.to_horizontal"
    bl_label = "To horizontal"
    bl_description = "Convert back to horizontal writing"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, _context):
        for obj in bpy.context.selected_objects:
            if obj.type == "FONT":
                obj.data.body = text_to_horizontal(obj.data.body)
        return {"FINISHED"}


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
        self.layout.operator("object.to_horizontal")
