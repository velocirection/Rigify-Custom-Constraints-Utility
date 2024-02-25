import bpy
import os
import sys

# imports ------------------------------------------------------------
if "bpy" in locals():
    import importlib
    if "rccu_string_utils" in locals():
        importlib.reload(rccu_string_utils)

from . import rccu_string_utils

from .rccu_string_utils import (extract_name_from_pointer_string, 
                               str_to_bool)
# --------------------------------------------------------------------

# add driver by args ---------------------------------------------------------
def add_driver( target_id:'',
                driver_data_path='',
                driver_bone_name='',
                driver_constraint_name='',
                driver_property_name='',
                expression='',
                is_simple_expression=True,
                is_valid=True,
                driver_type='',
                use_self='',
                var_list=''):
    '''
        adds a driver based on the arguments. var_list should be a list and targets should be a list of var_list.
    '''
                    
    # add the driver.
    print('target_id: ' + str(target_id))
    object_name = extract_name_from_pointer_string(str(target_id))
    armature = bpy.context.scene.objects[object_name]
    #armature.pose.bones[bone.name].constraints[constraintName]
    d = armature.pose.bones[driver_bone_name].constraints[driver_constraint_name].driver_add(driver_property_name, -1)
    d.driver.expression           = expression
    #d.driver.is_simple_expression = str_to_bool(is_simple_expression)
    d.driver.is_valid             = str_to_bool(is_valid)
    d.driver.type                 = driver_type
    d.driver.use_self = str_to_bool(use_self)
    # add the variables:
    if var_list is not None:
        for var in var_list:
            v = d.driver.variables.new()
            v.name                       = var['variable_name']
            v.type                       = var['variable_type']
            print('v.name: '+ var['variable_name'])            
            t = 0
            for target in var['targets']:
                print('variable: ' + str(v.name) + ' | target #' + str(t) + ': \n' + str(target))
                print('TARGETID: '+ target['id'])
                
                '''
                split = target['id'].split('\"')
                found_name = ''
                for item in split:
                    print(item)
                    if '<' not in item and '>' not in item:
                        found_name = item
                '''
                found_name = extract_name_from_pointer_string(target['id'])
                print('found name: ' + found_name)
                v.targets[t].id               = bpy.data.objects[found_name]
                v.targets[t].bone_target      = target['bone_target']
                v.targets[t].context_property = target['context_property']
                v.targets[t].data_path       = target['data_path']
                #v.targets[0].id_type        = id_type
                v.targets[t].rotation_mode   = target['rotation_mode']
                v.targets[t].transform_space = target['transform_space']
                v.targets[t].transform_type  = target['transform_type']
                t += 1
    return
# ----------------------------------------------------------------------------

# add constraints by args ----------------------------------------------------
def add_constraint_general(armature_name='',constraint_name='constraint', bone_name='bone',
                           constraint_type='COPY_LOCATION',
                           target='null', subtarget='null', influence=1.0,
                           target_space='WORLD', owner_space='WORLD',
                           mix_mode='ADD',
                           # copy location/rotation/scale
                           use_offset=False,
                           euler_order='AUTO',
                           use_x=True, use_y=True, use_z=True, 
                           invert_x=False, invert_y=False, invert_z=False,
                           power=1.0,
                           use_make_uniform=False,
                           use_add=False,
                           offset=0.0,
                           # transformation specific
                           map_from='LOCATION',map_to='LOCATION',
                           from_rotation_mode='AUTO',
                           to_euler_order='AUTO',
                           # mode modes
                            mix_mode_rot='ADD',mix_mode_scale='REPLACE',
                           # map channels
                           map_to_x_from='X', map_to_y_from='Y', map_to_z_from='Z',
                           # min/max values per property
                           from_min_x=0,from_min_y=0,from_min_z=0,
                           from_max_x=0,from_max_y=0,from_max_z=0,
                           from_min_x_scale=0,from_min_y_scale=0,from_min_z_scale=0,
                           from_max_x_scale=0,from_max_y_scale=0,from_max_z_scale=0,
                           from_min_x_rot=0,from_min_y_rot=0,from_min_z_rot=0,
                           from_max_x_rot=0,from_max_y_rot=0,from_max_z_rot=0,
                           
                           to_min_x=0,to_min_y=0,to_min_z=0,
                           to_max_x=0,to_max_y=0,to_max_z=0,
                           to_min_x_scale=0,to_min_y_scale=0,to_min_z_scale=0,
                           to_max_x_scale=0,to_max_y_scale=0,to_max_z_scale=0,
                           to_min_x_rot=0,to_min_y_rot=0,to_min_z_rot=0,
                           to_max_x_rot=0,to_max_y_rot=0,to_max_z_rot=0,
                           
                           # action specific
                           action='none',
                           transform_channel='LOCATION_X',
                           use_bone_object_action=False,
                           
                           min=0.0, max=0.0,
                           frame_start=0,frame_end=0,
                           
                           forward_axis='FORWARD_X',
                           up_axis='UP_X',
                           use_fixed_location=False,
                           use_curve_radius=False,
                           use_curve_follow=False,
                           
                           floor_location='FLOOR_X',
                           use_rotation=False,
                           
                           free_axis='SAMEVOL_Y',
                           mode='STRICT',
                           
                           volume=1.00,
                           use_bulge_min=False,
                           use_bulge_max=False,
                           bulge_smooth=0.0,
                           bulge_min=1.0,
                           bulge_max=1.0,
                           keep_axis='SWING_Y',
                           
                           
                           # limits
                           distance=0.0,
                           limit_mode='LIMITDIST_INSIDE',
                           use_transform_limit=False,
                           
                           head_tail=0.0,
                           
                           use_min_x=False,
                           use_min_y=False,
                           use_min_z=False,
                           
                           use_max_x=False,
                           use_max_y=False,
                           use_max_z=False,
                           
                           min_x=0.0,
                           min_y=0.0,
                           min_z=0.0,
                           
                           max_x=0.0,
                           max_y=0.0,
                           max_z=0.0,
                           
                           #child of
                           use_location_x=True,
                           use_location_y=True,
                           use_location_z=True,
                           use_rotation_x=True,
                           use_rotation_y=True,
                           use_rotation_z=True,
                           use_scale_x=True,
                           use_scale_y=True,
                           use_scale_z=True,
                           
                           use_limit_x=False,
                           use_limit_y=False,
                           use_limit_z=False,
                           
                           
                           #track to
                           track_axis='TRACK_X',
                           use_target_z=False,
                           
                           #stretch to @todo add more
                           rest_length=0.0,
                           bulge=1.0,
                           
                           space_subtarget=None,
                           use_eval_time=False,
                           eval_time=0.0,
                           
                           shrinkwrap_type='NEAREST_SURFACE',
                           project_axis='POS_Z',
                           project_axis_space='LOCAL',
                           project_limit=0,
                           use_project_opposite=False,
                           cull_face='OFF',
                           use_invert_cull=False,
                           wrap_mode='ON_SURFACE',
                           use_track_normal=False,

                           # follow path
                           use_3d_position=False,
                           use_active_clip=False,
                           use_undistorted_position=False,
                           frame_method='STRETCH',
                           camera=None,
                           depth_object=None,
                           
                           
                           use_motion_extrapolate=False):

    
    print(f">add_constraint_general: Trying to add \"{constraint_name}\" to \"{bone_name}\"")
    print(target)
    print(frame_end)
    #obj = bpy.context.active_object
    obj = bpy.context.active_object
    # Check if the active object is an armature
    if obj and obj.type == 'ARMATURE':
        armature = obj.data

        # check if the bone name is in the armature's bones.
        if bone_name in armature.bones:
            # if the bone was found, set bone to the found bone.
            bone = armature.bones[bone_name]
            # create a new constraint
            constraint = obj.pose.bones[bone_name].constraints.new(type=constraint_type)

            # name -------------------------------
            if hasattr(constraint, 'name'):
                constraint.name = constraint_name
                
            if hasattr(constraint, 'target'):
                try:
                    constraint.target = bpy.data.objects[target]
                except:
                    constraint.target = None
                
            if hasattr(constraint, 'subtarget'):
                constraint.subtarget = subtarget
                
            if hasattr(constraint, 'influence'):
                constraint.influence = float(influence)
            
            if hasattr(constraint, 'use_motion_extrapolate'):
                constraint.use_motion_extrapolate = str_to_bool(use_motion_extrapolate)

            if hasattr(constraint, 'map_from'):
                constraint.map_from = map_from
                
            if hasattr(constraint, 'map_to'):
                constraint.map_to = map_to
                
            if hasattr(constraint, 'transform_channel'):
                constraint.transform_channel = transform_channel 
                 
            if hasattr(constraint, 'target_space'):
                constraint.target_space = target_space

            if hasattr(constraint, 'offset'):
                constraint.offset = offset
                
            if hasattr(constraint, 'min'):
                constraint.min = float(min)
                
            if hasattr(constraint, 'max'):
                constraint.max = float(max)
 
            if hasattr(constraint, 'distance'):
                constraint.distance = float(distance)
                
            if hasattr(constraint, 'limit_mode'):
                constraint.limit_mode = limit_mode
                
            if hasattr(constraint, 'use_transform_limit'):
                constraint.use_transform_limit = str_to_bool(use_transform_limit)
                
            if hasattr(constraint, 'mix_mode'):
                constraint.mix_mode = mix_mode
                
            if hasattr(constraint, 'head_tail'):
                constraint.head_tail = float(head_tail)
                
            if hasattr(constraint, 'target_space'):
                constraint.target_space = target_space
                
            if hasattr(constraint, 'owner_space'):
                constraint.owner_space = owner_space
                
            if hasattr(constraint, 'action'):
                constraint.action = bpy.data.actions[action]
                
            if hasattr(constraint, 'use_bone_object_action'):
                constraint.use_bone_object_action = str_to_bool(use_bone_object_action)
                
            if hasattr(constraint, 'frame_start'):
                constraint.frame_start = int(frame_start)
                
            if hasattr(constraint, 'frame_end'):
                constraint.frame_end = int(frame_end)
                
            if hasattr(constraint, 'forward_axis'):
                constraint.forward_axis = forward_axis
                
            if hasattr(constraint, 'up_axis'):
                constraint.up_axis = up_axis
                
            if hasattr(constraint, 'track_axis'):
                constraint.track_axis = track_axis
                
            if hasattr(constraint, 'use_target_z'):
                constraint.use_target_z = use_target_z
                
            if hasattr(constraint, 'use_fixed_location'):
                constraint.use_fixed_location = use_fixed_location
                
            if hasattr(constraint, 'use_curve_radius'):
                constraint.use_curve_radius = use_curve_radius
                
            if hasattr(constraint, 'use_curve_follow'):
                constraint.use_curve_follow = use_curve_follow
                
            if hasattr(constraint, 'floor_location'):
                constraint.floor_location = floor_location
                
            if hasattr(constraint, 'use_rotation'):
                constraint.use_rotation = use_rotation
                
            if hasattr(constraint, 'euler_order'):
                constraint.euler_order = euler_order
                
            if hasattr(constraint, 'use_transform_limit'):
                constraint.use_transform_limit = str_to_bool(use_transform_limit)
                
            if hasattr(constraint, 'use_x'):
                constraint.use_x = str_to_bool(use_x)
            
            if hasattr(constraint, 'use_y'):
                constraint.use_y = str_to_bool(use_y)
                
            if hasattr(constraint, 'use_z'):
                constraint.use_z = str_to_bool(use_z)
                
            if hasattr(constraint, 'invert_x'):
                constraint.invert_x = str_to_bool(invert_x)
            
            if hasattr(constraint, 'invert_y'):
                constraint.invert_y = str_to_bool(invert_y)
                
            if hasattr(constraint, 'invert_z'):
                constraint.invert_z = str_to_bool(invert_z)
                
            if constraint_type == 'FOLLOW_TRACK':
                constraint.use_3d_position          = use_3d_position
                constraint.use_active_clip          = use_active_clip 
                constraint.use_undistorted_position = use_undistorted_position
                constraint.frame_method             = frame_method
                constraint.camera                   = camera
                constraint.depth_object             = depth_object
                
            if constraint_type == 'LIMIT_SCALE':
                constraint.use_min_x = str_to_bool(use_min_x)
                constraint.use_min_y = str_to_bool(use_min_y)
                constraint.use_min_z = str_to_bool(use_min_z)
                constraint.use_max_x = str_to_bool(use_max_x)
                constraint.use_max_y = str_to_bool(use_max_y)
                constraint.use_max_z = str_to_bool(use_max_z)
                constraint.min_x = float(min_x)
                constraint.min_y = float(min_y)
                constraint.min_z = float(min_z)
                constraint.max_x = float(max_x)
                constraint.max_y = float(max_y)
                constraint.max_z = float(max_z)
                
            if constraint_type == 'LIMIT_LOCATION':
                constraint.use_min_x = str_to_bool(use_min_x)
                constraint.use_min_y = str_to_bool(use_min_y)
                constraint.use_min_z = str_to_bool(use_min_z)
                constraint.use_max_x = str_to_bool(use_max_x)
                constraint.use_max_y = str_to_bool(use_max_y)
                constraint.use_max_z = str_to_bool(use_max_z)
                constraint.min_x = float(min_x)
                constraint.min_y = float(min_y)
                constraint.min_z = float(min_z)
                constraint.max_x = float(max_x)
                constraint.max_y = float(max_y)
                constraint.max_z = float(max_z)
                
            if constraint_type == 'LIMIT_ROTATION':
                constraint.use_limit_x = str_to_bool(use_limit_x)
                constraint.use_limit_y = str_to_bool(use_limit_y)
                constraint.use_limit_z = str_to_bool(use_limit_z)
                constraint.min_x = float(min_x)
                constraint.min_y = float(min_y)
                constraint.min_z = float(min_z)
                constraint.max_x = float(max_x)
                constraint.max_y = float(max_y)
                constraint.max_z = float(max_z)
                
            if constraint_type == 'ACTION':
                constraint.mix_mode = mix_mode

            if constraint_type == 'ARMATURE':
                constraint.use_deform_preserve_volume = use_deform_preserve_volume
                constraint.use_bone_envelopes         = use_bone_envelopes
                constraint.use_current_location       = use_current_location

            if constraint_type == 'CHILD_OF':
                constraint.use_location_x = use_location_x
                constraint.use_location_y = use_location_y
                constraint.use_location_z = use_location_z
                constraint.use_rotation_x = use_rotation_x
                constraint.use_rotation_y = use_rotation_y
                constraint.use_rotation_z = use_rotation_z
                constraint.use_scale_x    = use_scale_x
                constraint.use_scale_y    = use_scale_y
                constraint.use_scale_y    = use_scale_y

            if constraint_type == 'TRANSFORM':
                constraint.from_min_x       = float(from_min_x)
                constraint.from_min_y       = float(from_min_y)
                constraint.from_min_z       = float(from_min_z)
                constraint.from_max_x       = float(from_max_x)
                constraint.from_max_y       = float(from_max_y)
                constraint.from_max_z       = float(from_max_z)
                constraint.from_min_x_scale = float(from_min_x_scale)
                constraint.from_min_y_scale = float(from_min_y_scale)
                constraint.from_min_z_scale = float(from_min_z_scale)
                constraint.from_max_x_scale = float(from_max_x_scale)
                constraint.from_max_y_scale = float(from_max_y_scale)
                constraint.from_max_z_scale = float(from_max_z_scale)
                constraint.from_min_x_rot   = float(from_min_x_rot)
                constraint.from_min_y_rot   = float(from_min_y_rot)
                constraint.from_min_z_rot   = float(from_min_z_rot)
                constraint.from_max_x_rot   = float(from_max_x_rot)
                constraint.from_max_y_rot   = float(from_max_y_rot)
                constraint.from_max_z_rot   = float(from_max_z_rot)
                constraint.map_to         = map_to
                constraint.to_euler_order = to_euler_order
                constraint.map_to_x_from  = map_to_x_from
                constraint.map_to_y_from  = map_to_y_from
                constraint.map_to_z_from  = map_to_z_from
                constraint.to_min_x       = float(to_min_x)
                constraint.to_min_y       = float(to_min_y)
                constraint.to_min_z       = float(to_min_z)
                constraint.to_max_x       = float(to_max_x)
                constraint.to_max_y       = float(to_max_y)
                constraint.to_max_z       = float(to_max_z)
                constraint.to_min_x_rot   = float(to_min_x_rot)
                constraint.to_min_y_rot   = float(to_min_y_rot)
                constraint.to_min_z_rot   = float(to_min_z_rot)
                constraint.to_max_x_rot   = float(to_max_x_rot)
                constraint.to_max_y_rot   = float(to_max_y_rot)
                constraint.to_max_z_rot   = float(to_max_z_rot)
                constraint.to_min_x_scale = float(to_min_x_scale)
                constraint.to_min_y_scale = float(to_min_y_scale)
                constraint.to_max_z_scale = float(to_max_z_scale)
                constraint.to_min_z_scale = float(to_min_z_scale)
                constraint.to_max_x_scale = float(to_max_x_scale)
                constraint.to_max_y_scale = float(to_max_y_scale)
                # extra mix modes:
                constraint.mix_mode_scale = mix_mode_scale
                constraint.mix_mode_rot   = mix_mode_rot
                
            if constraint_type == 'STRETCH_TO':
                constraint.volume = volume
                constraint.use_bulge_min = str_to_bool(use_bulge_min)
                constraint.use_bulge_max = str_to_bool(use_bulge_max)
                constraint.bulge_smooth = float(bulge_smooth)
                constraint.bulge_min = float(bulge_min)
                constraint.bulge_max = float(bulge_max)
                constraint.keep_axis = keep_axis
                
            if constraint_type == 'MAINTAIN_VOLUME':
                constraint.mode = mode
                constraint.free_axis = free_axis

                
                
            if constraint_type == 'SHRINKWRAP':
                constraint.shrinkwrap_type      = shrinkwrap_type
                constraint.project_axis         = project_axis
                constraint.project_axis_space   = project_axis_space
                constraint.project_limit        = float(project_limit)
                constraint.use_project_opposite = str_to_bool(use_project_opposite)
                #print('use_project_opposite BOOL IS THIS: '+str(str_to_bool(use_project_opposite)))
                constraint.cull_face            = cull_face
                constraint.use_invert_cull      = str_to_bool(use_invert_cull)
                #print('use_invert_cull BOOL IS THIS: '+str(str_to_bool(use_invert_cull)))
                constraint.wrap_mode            = wrap_mode
                constraint.use_track_normal     = str_to_bool(use_track_normal)
                #print('use_track_normal BOOL IS THIS: '+str(str_to_bool(use_track_normal)))


            #print(f"   >Action constraint \"{constraint_name}\" added to \"{bone_name}\"")
        else:
            print(f"   >Bone \"{bone_name}\" not found.")
    else:
        print(">!error: No active armature found in the scene.")
        
# ----------------------------------------------------------------------------
