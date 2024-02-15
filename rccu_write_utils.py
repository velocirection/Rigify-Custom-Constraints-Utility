import bpy
import os
import sys

# imports ------------------------------------------------------------
if "bpy" in locals():
    import importlib
    if "rccu_string_utils" in locals():
        importlib.reload(rccu_string_utils)

from . import rccu_string_utils

from .rccu_string_utils import (make_directory_string, extract_name_from_data_path)
# --------------------------------------------------------------------

# constants ----------------------------------------------------------
DELIMITER = "$:"
CUSTOM_CONSTRAINT_PREFIX = 'CUST-'
# --------------------------------------------------------------------

# format driver data for text file -----------------------------------
def format_driver_data(data, variable, prefix=""):
    return f"{prefix}{variable}{DELIMITER}{data}\n"
# --------------------------------------------------------------------

# --------------------------------------------------------------------
def write_driver_info(armature_name, bone_name, f):
    armature = bpy.context.scene.objects[armature_name]
    if armature.animation_data is None:            
        return
    
    bone = armature.pose.bones[bone_name]
    for drivers in armature.animation_data.drivers:
        if CUSTOM_CONSTRAINT_PREFIX in drivers.data_path and bone_name in drivers.data_path:
            f.write('@BEGIN DRIVER\n')
            driver = drivers.driver
            # this is where the datapath lives
            print('\n')
            print('Found drive----------------------------------')
            print('  DATAPATH: '+drivers.data_path)
            split = drivers.data_path.split('.')
            found_bone_name       = ''
            found_constraint_name = ''
            found_property_name   = ''
            # process the data path to get the information we want.
            found_bone_name = extract_name_from_data_path(drivers.data_path, 'bones')
            found_constraint_name = extract_name_from_data_path(drivers.data_path, 'constraints')
            
            # get the last thing in the data path by '.' delimiter. should always be a property.
            for i in range(len(split)):
                item = split[i]
                if i == len(split)-1:
                    found_property_name = item
                    print('  found_property_name: ' + found_property_name)

            f.write(format_driver_data(drivers.data_path,       'driver_data_path'))
            f.write(format_driver_data(found_bone_name,       'driver_bone_name')) 
            f.write(format_driver_data(found_constraint_name,       'driver_constraint_name'))
            f.write(format_driver_data(found_property_name,       'driver_property_name'))
            f.write(format_driver_data(driver.expression,       'expression'))
            f.write(format_driver_data(driver.is_simple_expression,       'is_simple_expression'))
            f.write(format_driver_data(driver.is_valid,       'is_valid'))
            f.write(format_driver_data(driver.type,       'type', 'driver_'))
            f.write(format_driver_data(driver.use_self,       'use_self'))
            f.write('#variables for this driver------\n')
            for variable in driver.variables:
                f.write('@BEGIN DRIVER VARIABLE\n')
                #print('    is_name_valid: '+str(variable.is_name_valid))
                f.write(format_driver_data(variable.is_name_valid, 'is_name_valid')) 
                #print('    name: '+str(variable.name))
                f.write(format_driver_data(variable.name, 'name', 'variable_')) 
                #print('    type: '+str(variable.type))
                f.write(format_driver_data(variable.type, 'type', 'variable_')) 
                #print('    targets:')
                target_count = 0
                for target in variable.targets:
                    f.write('@BEGIN DRIVER VARIABLE TARGET\n')
                    print('      target '+str(target_count)+':')
                    #print('        target.bone_target: '+str(target.bone_target))
                    f.write(format_driver_data(target.bone_target, 'bone_target')) 
                    #print('        target.context_property: '+str(target.context_property))
                    f.write(format_driver_data(target.context_property, 'context_property')) 
                    #print('        target.data_path: '+str(target.data_path))
                    f.write(format_driver_data(target.data_path, 'data_path')) 
                    #print('        target.id: '+str(target.id))
                    f.write(format_driver_data(target.id, 'id')) 
                    #print('        target.id_type: '+str(target.id_type))
                    f.write(format_driver_data(target.id_type, 'id_type'))
                    #print('        target.rotation_mode: '+str(target.rotation_mode))
                    f.write(format_driver_data(target.rotation_mode, 'rotation_mode'))
                    #print('        target.transform_space: '+str(target.transform_space))
                    f.write(format_driver_data(target.transform_space, 'transform_space'))
                    #print('        target.transform_space: '+str(target.transform_type))
                    f.write(format_driver_data(target.transform_type, 'transform_type'))
                    target_count += 1
                    f.write('@END DRIVER VARIABLE TARGET\n')
                f.write('@END DRIVER VARIABLE\n')
            f.write('@END DRIVER\n\n')
            print('\n')
    return
# --------------------------------------------------------------------

# format constraint data for text file -------------------------------
def format_constraint_data(data, variable, prefix=""):
    '''
        this one is a bit weird but here's what's going on: first, we 
        see if the constraint has the attribute 'variable' (which is
        a string, the name of the attribute attempted to be read. Then,
        we evaluate a string expression. This will get the value of the
        variable for writing to the file.
        
        Also handles a special case for target to get just the name.
    '''
    if hasattr(data, variable):
        #value = eval('data.'+variable)
        value = getattr(data, variable)
        print(f'>Trying {variable}................')
        if value != None:
            if variable == 'target' or variable == 'pole_target' or variable == 'action' or variable == 'space_object':        
                value = value.name
            print(f">format_constraint_data|returning: {prefix}{variable}{DELIMITER}{value}.")
            return f"{prefix}{variable}{DELIMITER}{value}\n"
        else:
            return ""
        '''
        elif variable == 'target':
            # puts a target variable anyway.
            return f"{prefix}{variable}{DELIMITER}None\n"
        '''

    else:
        return ""
# --------------------------------------------------------------------


      
def write_constraint_info(boneName, f):
    # writes the constraint data of boneName to file F.
    # Get the active object in the scene
    obj = bpy.context.active_object
    # Check if the active object is an armature
    print(f">write_constraint_info: called for bone {boneName}.")
    if obj and obj.type == 'ARMATURE':
        armature = obj.data
        # Check if the armature has a bone named boneName
        if boneName in armature.bones:
            # Get the bone named boneName
            bone = obj.pose.bones[boneName]
            # go through all bone constraints
            for constraint in bone.constraints:
                
                # get the type:
                if CUSTOM_CONSTRAINT_PREFIX not in constraint.name:
                    print("   >skipping...")
                else:
                    print(f">write_constraint_info|begin writing {constraint.name}.")
                    cType = constraint.type
                    f.write('@BEGIN CONSTRAINT\n')
                    f.write(format_constraint_data(bone,       'name', 'bone_'))                
                    f.write(format_constraint_data(constraint, 'name', 'constraint_'))      
                    f.write(format_constraint_data(constraint, 'type'))
                    f.write(format_constraint_data(constraint, 'target'))
                    f.write(format_constraint_data(constraint, 'subtarget'))
                    f.write(format_constraint_data(constraint, 'head_tail'))
                    f.write(format_constraint_data(constraint, 'action'))
                    f.write(format_constraint_data(constraint, 'min'))
                    f.write(format_constraint_data(constraint, 'max'))
                    f.write(format_constraint_data(constraint, 'frame_end'))
                    f.write(format_constraint_data(constraint, 'frame_start'))
                    f.write(format_constraint_data(constraint, 'use_x'))
                    f.write(format_constraint_data(constraint, 'use_y'))
                    f.write(format_constraint_data(constraint, 'use_z'))
                    f.write(format_constraint_data(constraint, 'invert_x'))
                    f.write(format_constraint_data(constraint, 'invert_y'))
                    f.write(format_constraint_data(constraint, 'invert_z'))
                    f.write(format_constraint_data(constraint, 'distance'))
                    f.write(format_constraint_data(constraint, 'limit_mode'))
                    f.write(format_constraint_data(constraint, 'use_transform_limit'))
                    f.write(format_constraint_data(constraint, 'target_space'))
                    f.write(format_constraint_data(constraint, 'owner_space'))
                    f.write(format_constraint_data(constraint, 'euler_order'))
                    f.write(format_constraint_data(constraint, 'power'))
                    f.write(format_constraint_data(constraint, 'use_make_uniform'))
                    f.write(format_constraint_data(constraint, 'use_offset'))
                    f.write(format_constraint_data(constraint, 'use_add'))
                    f.write(format_constraint_data(constraint, 'use_min_x'))
                    f.write(format_constraint_data(constraint, 'use_min_y'))
                    f.write(format_constraint_data(constraint, 'use_min_z'))
                    f.write(format_constraint_data(constraint, 'use_max_x'))
                    f.write(format_constraint_data(constraint, 'use_max_y'))
                    f.write(format_constraint_data(constraint, 'use_max_z'))   
                    f.write(format_constraint_data(constraint, 'min_x'))
                    f.write(format_constraint_data(constraint, 'min_y'))
                    f.write(format_constraint_data(constraint, 'min_z'))
                    f.write(format_constraint_data(constraint, 'max_x'))
                    f.write(format_constraint_data(constraint, 'max_y'))
                    f.write(format_constraint_data(constraint, 'max_z'))
                    f.write(format_constraint_data(constraint, 'mode'))
                    f.write(format_constraint_data(constraint, 'free_axis'))
                    f.write(format_constraint_data(constraint, 'volume'))
                    f.write(format_constraint_data(constraint, 'use_limit_x'))
                    f.write(format_constraint_data(constraint, 'use_limit_y'))
                    f.write(format_constraint_data(constraint, 'use_limit_z'))
                    f.write(format_constraint_data(constraint, 'use_motion_extrapolate'))
                    f.write(format_constraint_data(constraint, 'map_from'))
                    f.write(format_constraint_data(constraint, 'from_rotation_mode'))
                    f.write(format_constraint_data(constraint, 'from_min_x'))
                    f.write(format_constraint_data(constraint, 'from_min_y'))
                    f.write(format_constraint_data(constraint, 'from_min_z'))
                    f.write(format_constraint_data(constraint, 'from_max_x'))
                    f.write(format_constraint_data(constraint, 'from_max_y'))
                    f.write(format_constraint_data(constraint, 'from_max_z'))
                    f.write(format_constraint_data(constraint, 'from_min_x_rot'))
                    f.write(format_constraint_data(constraint, 'from_min_y_rot'))
                    f.write(format_constraint_data(constraint, 'from_min_z_rot'))
                    f.write(format_constraint_data(constraint, 'from_max_x_rot'))
                    f.write(format_constraint_data(constraint, 'from_max_y_rot'))
                    f.write(format_constraint_data(constraint, 'from_max_z_rot'))
                    f.write(format_constraint_data(constraint, 'from_min_x_scale'))
                    f.write(format_constraint_data(constraint, 'from_min_y_scale'))
                    f.write(format_constraint_data(constraint, 'from_min_z_scale'))
                    f.write(format_constraint_data(constraint, 'from_max_x_scale'))
                    f.write(format_constraint_data(constraint, 'from_max_y_scale'))
                    f.write(format_constraint_data(constraint, 'from_max_z_scale'))
                    
                    f.write(format_constraint_data(constraint, 'map_to'))
                    f.write(format_constraint_data(constraint, 'to_euler_order'))
                    f.write(format_constraint_data(constraint, 'map_to_x_from'))
                    f.write(format_constraint_data(constraint, 'map_to_y_from'))
                    f.write(format_constraint_data(constraint, 'map_to_z_from'))
                    
                    f.write(format_constraint_data(constraint, 'to_min_x'))
                    f.write(format_constraint_data(constraint, 'to_min_y'))
                    f.write(format_constraint_data(constraint, 'to_min_z'))
                    f.write(format_constraint_data(constraint, 'to_max_x'))
                    f.write(format_constraint_data(constraint, 'to_max_y'))
                    f.write(format_constraint_data(constraint, 'to_max_z'))
                    f.write(format_constraint_data(constraint, 'to_min_x_rot'))
                    f.write(format_constraint_data(constraint, 'to_min_y_rot'))
                    f.write(format_constraint_data(constraint, 'to_min_z_rot'))
                    f.write(format_constraint_data(constraint, 'to_max_x_rot'))
                    f.write(format_constraint_data(constraint, 'to_max_y_rot'))
                    f.write(format_constraint_data(constraint, 'to_max_z_rot'))
                    f.write(format_constraint_data(constraint, 'to_min_x_scale'))
                    f.write(format_constraint_data(constraint, 'to_min_y_scale'))
                    f.write(format_constraint_data(constraint, 'to_min_z_scale'))
                    f.write(format_constraint_data(constraint, 'to_max_x_scale'))
                    f.write(format_constraint_data(constraint, 'to_max_y_scale'))
                    f.write(format_constraint_data(constraint, 'to_max_z_scale'))
                    

                    f.write(format_constraint_data(constraint, 'main_axis'))
                    f.write(format_constraint_data(constraint, 'use_cyclic'))
                    f.write(format_constraint_data(constraint, 'track_axis'))
                    f.write(format_constraint_data(constraint, 'up_axis'))
                    # ik
                    f.write(format_constraint_data(constraint, 'pole_target'))
                    f.write(format_constraint_data(constraint, 'pole_subtarget'))
                    f.write(format_constraint_data(constraint, 'pole_angle'))
                    f.write(format_constraint_data(constraint, 'iterations'))
                    f.write(format_constraint_data(constraint, 'chain_count'))
                    f.write(format_constraint_data(constraint, 'use_tail'))
                    f.write(format_constraint_data(constraint, 'use_stretch'))
                    f.write(format_constraint_data(constraint, 'use_location'))
                    f.write(format_constraint_data(constraint, 'use_rotation'))
                    f.write(format_constraint_data(constraint, 'weight'))
                    f.write(format_constraint_data(constraint, 'orient_weight'))
                    #spline
                    f.write(format_constraint_data(constraint, 'use_even_divisions'))
                    f.write(format_constraint_data(constraint, 'use_chain_offset'))
                    f.write(format_constraint_data(constraint, 'use_curve_radius'))
                    f.write(format_constraint_data(constraint, 'y_scale_mode'))
                    f.write(format_constraint_data(constraint, 'xz_scale_mode'))
                    f.write(format_constraint_data(constraint, 'use_original_scale'))
                    f.write(format_constraint_data(constraint, 'bulge'))
                    f.write(format_constraint_data(constraint, 'bulge_min'))
                    f.write(format_constraint_data(constraint, 'bulge_max'))
                    f.write(format_constraint_data(constraint, 'bulge_smooth'))
                    f.write(format_constraint_data(constraint, 'use_bulge_max'))
                    f.write(format_constraint_data(constraint, 'use_bulge_min'))
                    f.write(format_constraint_data(constraint, 'use_bulge_max'))
                    
                    f.write(format_constraint_data(constraint, 'lock_axis'))
                    # @TODO and the rest
                    
                    f.write(format_constraint_data(constraint, 'space_object'))
                    f.write(format_constraint_data(constraint, 'space_subtarget'))
                    
                    
                    f.write(format_constraint_data(constraint, 'transform_channel'))
                    f.write(format_constraint_data(constraint, 'mix_mode'))
                    # special for transformation:
                    f.write(format_constraint_data(constraint, 'mix_mode_rot'))
                    f.write(format_constraint_data(constraint, 'mix_mode_scale'))
                    
                    f.write(format_constraint_data(constraint, 'use_eval_time'))
                    f.write(format_constraint_data(constraint, 'eval_time'))
                    f.write(format_constraint_data(constraint, 'transform_channel'))
                    f.write(format_constraint_data(constraint, 'use_bone_object_action'))
                    f.write(format_constraint_data(constraint, 'influence'))
                    
                    # @test track to
                    # @test stretch to
                    # @test spline IK
                    # @test clamp to
                    
                    # @todo armature?
                    # @TODO child of
                    # @TODO floor
                    # @TODO follow path
                    # @TODO pivot
                    
                    
                    # shrink wrap
                    f.write(format_constraint_data(constraint, 'shrinkwrap_type'))
                    f.write(format_constraint_data(constraint, 'project_axis'))
                    f.write(format_constraint_data(constraint, 'project_axis_space'))
                    f.write(format_constraint_data(constraint, 'project_limit'))
                    f.write(format_constraint_data(constraint, 'use_project_opposite'))
                    f.write(format_constraint_data(constraint, 'cull_face'))
                    f.write(format_constraint_data(constraint, 'use_invert_cull'))
                    f.write(format_constraint_data(constraint, 'wrap_mode'))
                    f.write(format_constraint_data(constraint, 'use_track_normal'))
        
                    
                    
                    
  
                    f.write('@END CONSTRAINT\n')    
                    f.write(f"\n") #write new line for readability.
                    
                
        else:
            print(f"write_constraint_info: bone {boneName} not found in armature.")
    else:
        print(">write_constraint_info: armature not selected.")
# --------------------------------------------------------------------

# write file stuff -----------------------------------------------------------
def write_generated_rig_constraint_link_file(armature):
    wDir = make_directory_string(armature)
    f = open(wDir, "w")
    
    # START WRITING TO FILE
    f.write(f"# ARMATURE \"{armature.name}\" GENERATED RIG CONSTRAINT LINK FILE #\n")
    f.write(f"\n") #write new line for readability.
    for bone in armature.bones:
        # write constraints to files for non MCH/DEF/ORG bones.
        if not 'MCH' in bone.name and not 'DEF' in bone.name and not 'ORG' in bone.name:
            # write constraint data
            write_constraint_info(bone.name, f)
            # write driver data of constraint data
            write_driver_info(armature.name, bone.name, f)
            
    # close the file:
    f.close()
    return 0
# ---------------------------------------------------------------------------