import bpy
import os
import sys
bl_info = {
    "name": "Rigify custom constraints utility BETA",
    "author": "Velocirection (V-rex)",
    "version" : (0, 0, 0, 2),
    "blender" : (4, 0, 0),
    "location": "View3D - Properties",
    "description": "Utility to add custom constraints to a generated rigify armature.\n-Creates a folder and text file per-rig.\n-Saves constraints with 'CUST-' prefix on none MCH/DEF/ORG bones. Note: The following constraints are not support: Camera Solver, Follow Track, Object Solver, Armature",
    "warning": "",
    "wiki_url": "",
    "category": "rigging"}

release_mode = True
if release_mode:
    if "bpy" in locals():
        import importlib
        if "rccu_write_utils" in locals():
            importlib.reload(rccu_write_utils)
        if "rccu_read_utils" in locals():
            importlib.reload(rccu_read_utils)
        if "rccu_make_finalize_script" in locals():
            importlib.reload(rccu_make_finalize_script)

    #from . import rigify_utility_messyscript
    from . import rccu_make_finalize_script
    from . import rccu_write_utils
    from . import rccu_read_utils
    
    from .rccu_make_finalize_script     import ( make_rigify_finalize_script)
    from .rccu_write_utils              import ( write_generated_rig_constraint_link_file)
    from .rccu_read_utils               import ( read_generated_rig_constraint_link_file)

if release_mode == False:
    dir = os.path.dirname(bpy.data.filepath)
    if not dir in sys.path:
        sys.path.append(dir )
        #print(sys.path)

    #import rigify_utility_messyscript_wp
    import rccu_make_finalize_script
    import rccu_write_utils
    import rccu_read_utils

    # this next part forces a reload in case you edit the source after you first start the blender session
    import importlib
    #imp.reload(rigify_utility_messyscript_wp)
    importlib.reload(rccu_make_finalize_script)
    importlib.reload(rccu_write_utils)
    importlib.reload(rccu_read_utils)
    
    #from rigify_utility_messyscript_wp import ( clear_custom_constraints)
                                            
    from rccu_make_finalize_script     import ( make_rigify_finalize_script)
    from rccu_write_utils              import ( write_generated_rig_constraint_link_file)
    from rccu_read_utils               import ( read_generated_rig_constraint_link_file)

                                        
# ----------------------------------------------
# Import modules
# ----------------------------------------------
class rccuMatchObjectAndDataName(bpy.types.Operator):
    bl_idname = 'scene.rccumatchobjectanddataname'
    bl_label = '#RCCU#MATCH'
    bl_description = 'Renames the data object\'s name to the object\'s name (this is necessary for the add-on to work properly)'
    
    def execute(self, context):
        print('>rccuMatchObjectAndDataName| Called...')     
        obj = bpy.context.active_object
        if obj and obj.type == 'ARMATURE':
            obj.data.name = obj.name
        self.report({'INFO'}, 'Renamed armature data name to armature object name.')
        return {'FINISHED'}
    
    
    
class rccuSetupRunScript(bpy.types.Operator):
    bl_idname = 'scene.rccusetuprunscript'
    bl_label = '#RCCU#SETUPRUNSCRIPT'
    bl_description = 'Creates a script and assigns to the \'Target Rig\'s\' \'Run Script\' property (This is the script that runs after Rigify generates the rig)'
    
    def execute(self, context):
        print('>rccuSetupRunScript| Called...')
        scene = context.scene
        obj = bpy.context.active_object
        if obj and obj.type == 'ARMATURE':
            obj.data.name = obj.name
        self.report({'INFO'}, f'Created \'run script\' for metarig \'{scene.metarig_object}\'')
        scene = context.scene
        
        make_rigify_finalize_script(scene.metarig_object.data)
        return {'FINISHED'}
    
    



class rccuSaveConstraints(bpy.types.Operator):
    bl_idname = 'scene.rccusaveconstraints'
    bl_label = '#RCCU#SAVE_CONSTRAINTS'
    bl_description = 'Saves the custom constraints to the constraint link file'
    
    def execute(self, context):
        print('>rccuSaveConstraints| Called...')        
        scene = context.scene
        # call the function from the module
        generated_rig = bpy.data.armatures[scene.metarig_object.name].rigify_target_rig
        if generated_rig is None:
            generated_rig = bpy.context.active_object
        if generated_rig and generated_rig.type == 'ARMATURE':
            armature = generated_rig.data
            code = write_generated_rig_constraint_link_file(armature)
        # error checking:
        if code == 0:
            self.report({'INFO'}, 'save_custom_constraints exited with code 0 (success)')
        else:
            self.report({'ERROR'}, 'save_custom_constraints did not exit properly')
            
        return {'FINISHED'}






class rccuLoadConstraints(bpy.types.Operator):
    bl_idname = 'scene.rcculoadconstraints'
    bl_label = '#RCCU#LOAD_CONSTRAINTS'
    bl_description = 'Loads custom constraints from the \'Target Rig\'s\' constraint link file (Warning: Currently drivers are not cleared so do not use this operator if your custom constraints have drivers, setup the run script and re-generate the rig instead!)'
    
    def execute(self, context):
        print('>rccuLoadConstraints| Called...')
        scene = context.scene
        # call the function from the module
        
        #generated_rig = bpy.data.armatures[scene.metarig_object.name].rigify_target_rig
        
        generated_rig = bpy.data.armatures[scene.metarig_object.name].rigify_target_rig
        if generated_rig is None:
            generated_rig = bpy.context.active_object
        if generated_rig and generated_rig.type == 'ARMATURE':
            armature = generated_rig.data
            code = read_generated_rig_constraint_link_file(armature)
        # error checking:
        if code == 0:
            self.report({'INFO'}, 'save_custom_constraints exited with code 0 (success)')
        else:
            self.report({'ERROR'}, 'save_custom_constraints did not exit properly')
        

        return {'FINISHED'}
    
class rccuClearConstraints(bpy.types.Operator):
    bl_idname = 'scene.rccuclearconstraints'
    bl_label = '#RCCU#CLEAR_CONSTRAINTS'
    bl_description = ' '
    
    def execute(self, context):
        scene = context.scene
        print('>rccuClearConstraints| Called...')
        # call the function from the module
        self.report({'INFO'}, 'Cleared constraints.')
        clear_custom_constraints()
        return {'FINISHED'}
    
class rccuRegenerateRig(bpy.types.Operator):
    bl_idname = 'scene.rccuregeneraterig'
    bl_label = '#RCCU#REGENERATE_RIG'
    bl_description = 'Calls the \'Re-Generate Rig\' function from Rigify on the \'Metarig\''
    def execute(self, context):
        scene = context.scene
        print('>rccuRegenerateRig| Called...')
        bpy.ops.object.select_all(action='DESELECT')
        scene.metarig_object.hide_set(False)
        scene.metarig_object.hide_viewport = False
        if scene.metarig_object != None:
            scene.metarig_object.select_set(True)
            bpy.context.view_layer.objects.active = scene.metarig_object
            bpy.ops.pose.rigify_generate()
        else:
            self.report({'ERROR'}, 'Unable to call \'bpy.ops.pose.rigify_generate()\'')
        return {'FINISHED'}


def scene_poll_armature(self, object):
    return object.type == 'ARMATURE'
    
# MAIN PANEL ---------------------------------------------------------------
class RCCU_PT_panel(bpy.types.Panel):
    bl_label = 'Rigify Custom Constraint Utility'
    bl_idname = 'RCCU_PT_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vrextras'
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.label(text='Tips:')
        layout.label(text='-Select the generated rig (not metarig)')
        layout.label(text='-Only constraints with \'CUST-\' prefix are affected')
        layout.label(text='-MCH/DEF/ORG bones are not affected.')
        layout.label(text='-Armature object name must match name of armature data.')
        # armatures/bone box ------------------------------
        box = layout.box()
        #split = box.split()
        armature = bpy.context.view_layer.objects.active

        box.operator(operator='scene.rccusaveconstraints', text='Save custom constraints')
        box.operator(operator='scene.rcculoadconstraints', text='Load custom constraints')
        box.operator(operator='scene.rccusetuprunscript', text='Setup Run Script')
        #box.operator(operator='scene.ruclearconstraints', text='Clear custom constraints')
        box.operator(operator='scene.rccuregeneraterig', text='Re-Generate Rig')
        #box.row()
        
        #split = box.split()
        #col1 = split.column()
        #col2 = split.column()
        box.label(text='Metarig: ')
        box.prop(scene, 'metarig_object', text="")
        if scene.metarig_object != None:
            box.label(text='Target Rig: ')
            box.prop(bpy.data.armatures[scene.metarig_object.name], 'rigify_target_rig', text="")
            box.label(text='Run Script: ')
            box.prop(bpy.data.armatures[scene.metarig_object.name], 'rigify_finalize_script', text="")
        
        if armature != None and armature.type != 'ARMATURE':
            box.enabled = False  
        
        # warnings -------------------------------------------
        #armature = bpy.context.view_layer.objects.active
        armature = scene.metarig_object
        generated_rig = None
        
        if armature == None:
            row = layout.row()
            row.label(text=f'Warning: metarig is not selected!')
        
        if armature != None:
            generated_rig = bpy.data.armatures[scene.metarig_object.name].rigify_target_rig
            
        if armature != None and armature.type == 'ARMATURE':
            row = layout.row()
            row.label(text=f'Metarig: \'{armature.name}\'')
            
        if generated_rig != None and generated_rig.type == 'ARMATURE':
            row = layout.row()
            row.label(text=f'Target Rig: \'{generated_rig.name}\'')
            
        if generated_rig != None and generated_rig.name != generated_rig.data.name:
            row = layout.row()
            row.label(text=f'Warning: Generated rig object name and data rig don\'t match!')
            row = layout.row()
            row.operator(operator='scene.rccumatchobjectanddataname', text='Match names')
            return
        
        
def register():
    bpy.utils.register_class(RCCU_PT_panel)
    bpy.utils.register_class(rccuSaveConstraints)
    bpy.utils.register_class(rccuLoadConstraints)
    bpy.utils.register_class(rccuClearConstraints)
    bpy.utils.register_class(rccuMatchObjectAndDataName)
    bpy.utils.register_class(rccuRegenerateRig)
    bpy.utils.register_class(rccuSetupRunScript)
    bpy.types.Scene.metarig_object = bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Metarig object",
        poll=scene_poll_armature,
        description="The metarig",
    )
    bpy.types.Scene.metarig_target = bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Target metarig",
        poll=scene_poll_armature,
        description="The generated rig.",
    )
    
def unregister():
    bpy.utils.unregister_class(RCCU_PT_panel)
    bpy.utils.unregister_class(rccuSaveConstraints)
    bpy.utils.unregister_class(rccuLoadConstraints)
    bpy.utils.unregister_class(rccuClearConstraints)
    bpy.utils.unregister_class(rccuMatchObjectAndDataName)
    bpy.utils.unregister_class(rccuRegenerateRig)
    bpy.utils.unregister_class(rccuSetupRunScript)
    del bpy.types.Scene.metarig_target
    del bpy.types.Scene.metarig_object
    
if __name__ == '__main__':
    register()
