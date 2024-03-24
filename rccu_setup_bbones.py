import bpy

def setup_bbones(armature):
    for b in armature.bones:
        # find if the bone is supposed to tbe a bendy bone ('|BB|')
        # and if it's a deforming bone (first 4 chars will be 'DEF-')
        if '|BB|' in b.name and 'DEF-' in b.name[:4]:
            parent = b.parent
            # bbone info --------------------------------------------------------------
            b.bbone_segments                  = parent.bbone_segments                  
            b.bbone_x                         = parent.bbone_x*0.75 # for visual display
            b.bbone_z                         = parent.bbone_z*0.75 # for visual display
            b.bbone_curveinx                  = parent.bbone_curveinx             
            b.bbone_curveinz                  = parent.bbone_curveinz             
            b.bbone_curveoutx                 = parent.bbone_curveoutx            
            b.bbone_curveoutz                 = parent.bbone_curveoutz            
            b.bbone_rollin                    = parent.bbone_rollin               
            b.bbone_rollout                   = parent.bbone_rollout              
            b.bbone_scalein[0]                = parent.bbone_scalein[0]           
            b.bbone_scalein[1]                = parent.bbone_scalein[1]           
            b.bbone_scalein[2]                = parent.bbone_scalein[2]           
            b.bbone_scaleout[0]               = parent.bbone_scaleout[0]          
            b.bbone_scaleout[1]               = parent.bbone_scaleout[1]          
            b.bbone_scaleout[2]               = parent.bbone_scaleout[2]          
            b.bbone_easein                    = parent.bbone_easein               
            b.bbone_easeout                   = parent.bbone_easeout              
            b.use_scale_easing                = parent.use_scale_easing                                
            b.bbone_handle_use_scale_start[0] = parent.bbone_handle_use_scale_start[0] 
            b.bbone_handle_use_scale_start[1] = parent.bbone_handle_use_scale_start[1] 
            b.bbone_handle_use_scale_start[2] = parent.bbone_handle_use_scale_start[2] 
            b.bbone_handle_use_ease_start     = parent.bbone_handle_use_ease_start     
            b.bbone_handle_use_scale_end[0]   = parent.bbone_handle_use_scale_end[0]   
            b.bbone_handle_use_scale_end[1]   = parent.bbone_handle_use_scale_end[1]   
            b.bbone_handle_use_scale_end[2]   = parent.bbone_handle_use_scale_end[2]   
            b.bbone_handle_use_ease_end       = parent.bbone_handle_use_ease_end   
            # handle info -------------------------------------------------------------
            b.bbone_handle_type_start         = parent.bbone_handle_type_start
            b.bbone_handle_type_end           = parent.bbone_handle_type_end
            b.bbone_custom_handle_start       = parent.bbone_custom_handle_start
            b.bbone_custom_handle_end         = parent.bbone_custom_handle_end