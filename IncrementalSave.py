"""A simple Blender addon that saves a .blend file incrementally. Currently only tested on
 Windows.
Installation: Go to Edit > Preferences > Add-ons > Install Add-on and double click on this file.
Usage: Press F3 in the 3D viewport, type 'increme..' until you see "Incremental Save" and press "Enter".
Note: You must save the file initially before incrementing.
created by Reid Tissing (https://github.com/ReidTissing/IncrementalSave or www.buriedanimal.com)
"""

bl_info = {
    "name": "Incremental Save",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import os

class IncrementalSave(bpy.types.Operator):
    """Incremental Save"""
    bl_idname = "object.incremental_save"
    bl_label = "Incremental Save"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if bpy.data.is_saved:
            #import and decode filepath
            filepath_bytes = os.fsencode(bpy.data.filepath)
            filepath_utf8 = filepath_bytes.decode('utf-8', "replace")
            
            #split into directory and filename
            dirname, filename = os.path.split(filepath_utf8)
            filenoext = filename[:-6]
            #find last digit saved
            i = 1
            while os.path.exists(dirname + "\\" + filenoext + "%s.blend" % i):
                i += 1
            head, sep, tail = filenoext.partition('.blend')

            #check if last character is digit and strip if so
            if head[-1].isdigit():
                newname = head[0:-1]
                suffix = head[-1]
                suffix = int(suffix) + 1
                fullpath = dirname + "\\" + newname + str(suffix) + ".blend"
            else:
                newname = head
                fullpath = dirname + "\\" + newname + str(i) + ".blend"
            #save it
            fullpath = fullpath.encode('utf-8', "replace")
            bpy.ops.wm.save_mainfile(filepath=fullpath)
            return {'FINISHED'}
        else:
            #if file has not been saved, warn user with popup
            def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
                def draw(self, context):
                    self.layout.label(text="Save file before trying to incrementally save.")
                bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
            ShowMessageBox("This is a message", "Error", 'ERROR')
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(IncrementalSave)


def unregister():
    bpy.utils.unregister_class(IncrementalSave)
    
if __name__ == "__main__":
    register()