# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
import bpy, shlex, tempfile
from bpy.props import IntProperty, FloatProperty
from subprocess import Popen, PIPE


class ModalOperator(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "scene.modal_operator"
    bl_label = "Simple Modal Operator"
    
    _timer = None
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.rcalcrun.poll() is not None:
                self.line += 4
                if self.line >= len(self.alllines):
                    print ('finished')                    
                    return {'FINISHED'}
                self.rtrun = Popen(self.rtcmd.split(), stdin = PIPE, stdout = PIPE)
                self.rtrun.stdin.write(' '.join(self.alllines[self.line:self.line+4]).encode('utf-8'))
                self.rtrun.stdin.close()
                self.rcalcrun = Popen(self.rcalccmd, stdin = self.rtrun.stdout, stdout=PIPE) 
                print('{}% complete'.format(100*self.line/len(self.alllines)))                
            return {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}
   
    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, context.window)
        wm.modal_handler_add(self)
        self.line = 0
        self.rcalccmd = ['rcalc', '-e', '$1=(47.4*$1+120*$2+11.6*$3)/100'] 
        self.rtcmd = "/usr/local/radiance/bin/rtrace -n 4 -aa 0.1 -ad 4096 -ab 7 -as 2098 -faa -h -ov -I /home/ryan/Blender/radparams/radparams-0.oct"
        with open('/home/ryan/Blender/radparams/radparams.rtrace') as rtfile:
            self.alllines = rtfile.readlines()

        self.rtrun = Popen(self.rtcmd.split(), stdin = PIPE, stdout=PIPE)
        self.rtrun.stdin.write(' '.join(self.alllines[self.line:self.line+4]).encode('utf-8'))
        self.rtrun.stdin.close()
        self.rcalcrun = Popen(self.rcalccmd, stdin = self.rtrun.stdout, stdout=PIPE)    
        return {'RUNNING_MODAL'}

def register():
	bpy.utils.register_class(ModalOperator)


def unregister():
	bpy.utils.unregister_class(ModalOperator)


if __name__ == "__main__":
	register()
	
bpy.ops.scene.modal_operator()
