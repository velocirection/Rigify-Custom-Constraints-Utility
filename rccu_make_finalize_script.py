import bpy

def make_rigify_finalize_script(metarig):
    print(f'make_rigify_finalize_script| Called...')
    try:
        armature_name = metarig.rigify_target_rig.name
    except:
        print(f'>make_postgen_script|{metarig.name} has invalid rigify_target_rig')
        return
    
    # make new text block.
    text_block = bpy.data.texts.new(name=armature_name+"_fs.py")
    
    # text to put in the python script:
    target_rig_name = armature_name
    comment_str = f'# \'rigify_finalize_script\' for \'{armature_name}\', generated by the Rigify Custom Constraints Utility\n\n'
    imports = f'import bpy\n'
    code_str = f'bpy.ops.scene.rcculoadconstraints()'
    
    # put the text into the script:
    text_block.from_string(f"{comment_str}{imports}{code_str}")
    
    # set the metarig post generation scrip to the created one:
    metarig.rigify_finalize_script = text_block
    

#make_rigify_finalize_script(bpy.data.objects['METARIG-mitch'].data)