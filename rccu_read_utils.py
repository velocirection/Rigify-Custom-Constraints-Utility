import bpy
import os
import sys

# imports ------------------------------------------------------------
if "bpy" in locals():
    import importlib
    if "rccu_string_utils" in locals():
        importlib.reload(rccu_string_utils)
    if "rccu_add_utils" in locals():
        importlib.reload(rccu_add_utils)

from . import rccu_string_utils
from . import rccu_add_utils

from .rccu_add_utils import (add_constraint_general,
                            add_driver)

from .rccu_string_utils import (make_directory_string)
# --------------------------------------------------------------------
    
    
# constants ----------------------------------------------------------
DELIMITER = "$:"
CUSTOM_CONSTRAINT_PREFIX = 'CUST-'
# --------------------------------------------------------------------

def clear_custom_constraints(armature_name):
    obj = bpy.data.objects[armature_name]
    if obj and obj.type == 'ARMATURE':
        armature = obj.data

        # Check if the armature has a bone named "testbone"
        for bone in armature.bones:
            # if the bone was found, set bone to the found bone.
            #bone = armature.bones[bone_name]
            # clear constraints to make sure it's clean.
            # clear_constraints(bone.name)
            # create a new constraint
            constraints = obj.pose.bones[bone.name].constraints
            for constraint in constraints:
                if 'CUST-' in constraint.name:
                    obj.pose.bones[bone.name].constraints.remove(constraint)
                    #obj.pose.bones[bone.name].constraints[constraint.name].remove()
                                            
# read file stuff -----------------------------------------------------------
READ_STATE_IDLE = 0; # reading useless lines.
READ_STATE_COLLECTING = 1; # gathering parameters
READ_STATE_FINALIZE = 2; # add the constraint

READ_STATE_COLLECTING_CONSTRAINT = 3; # gathering parameters
READ_STATE_COLLECTING_DRIVER = 4; # gathering parameters
READ_STATE_COLLECTING_DRIVER_VARIABLE = 5; # gathering parameters'
READ_STATE_COLLECTING_DRIVER_VARIABLE_TARGET = 6; # gathering parameters
READ_STATE_FINALIZE_CONSTRAINT = 7; # add the constraint
READ_STATE_FINALIZE_DRIVER = 8; # add the constraint
def read_generated_rig_constraint_link_file(armature):    
    # clear all custom constraints first
    clear_custom_constraints(armature.name)
    
    
    # open the file:
    wDir = make_directory_string(armature)
    f = open(wDir, "r")
    
    # start reading:
    readState = 0; # what the reader is doing.
    # define constraints arguments
    constraintsArgs = {}
    # define driver args
    driverArgs = {}
    driverArgs['target_id'] = armature
    driverArgs['var_list'] = [{}]
    driverVariable = 0;
    driverVariableTarget = 0;
    for line in f:
        # if idle, read until hitting something important.
        cLine = line
        cLine = cLine.replace("\n", "")
        
        if '@BEGIN' in cLine:
            if 'CONSTRAINT' in cLine:
                readState = READ_STATE_COLLECTING_CONSTRAINT
                print('>Reading constraint:')
            if 'DRIVE' in cLine:
                if 'VARIABLE' in cLine:
                    if 'TARGET' in cLine:
                        if driverVariableTarget == 0:
                            driverArgs['var_list'][driverVariable]['targets'] = [{}]
                        readState = READ_STATE_COLLECTING_DRIVER_VARIABLE_TARGET
                    else:
                        readState = READ_STATE_COLLECTING_DRIVER_VARIABLE                        
                else:
                    readState = READ_STATE_COLLECTING_DRIVER                            
                

        #print(cLine)
        if '@END' in cLine:
            if 'CONSTRAINT' in cLine:
                readState = READ_STATE_FINALIZE_CONSTRAINT
                print('>End constraint:')
            if 'DRIVE' in cLine:
                if 'VARIABLE' in cLine:
                    if 'TARGET' in cLine:
                        driverVariableTarget += 1
                        readState = READ_STATE_IDLE
                    else:
                        driverVariable += 1
                        driverVariableTarget = 0
                        readState = READ_STATE_IDLE                    
                else:
                    readState = READ_STATE_FINALIZE_DRIVER
        
        
        if readState == READ_STATE_IDLE:
            # get current line.
            
            # if the line is a comment, print it.
            if len(cLine) > 0 and cLine[0] == "#":
                print(cLine) #comment line
                
        # if collecting, add to the constraints argument.
        if readState == READ_STATE_COLLECTING_CONSTRAINT:
            if '@BEGIN' in cLine:
                print(" ")
            elif '@END' in cLine:
                print(" ")
            else: 
                # split the line based on the "$:" delimiter
                cLineSplit = cLine.split(DELIMITER)
                key = cLineSplit[0]
                value = 0
                if len(cLineSplit) > 1:
                    # only name is found.  
                    value = cLineSplit[1]
                if key == 'type':
                    key = 'constraint_type'
                #print(f'{key} : {value}')
                constraintsArgs[key] = value
                #cLine = f.readline()
                
        if readState == READ_STATE_COLLECTING_DRIVER:
            print('Collecting driver: ' + cLine)
            if '@BEGIN' in cLine or '@END' in cLine:
                print("")
            elif cLine[0] == '#': 
                print('')
            else: 
                # split the line based on the "$:" delimiter
                cLineSplit = cLine.split(DELIMITER)
                key = cLineSplit[0]
                value = 0
                if len(cLineSplit) > 1:
                    # only name is found.  
                    value = cLineSplit[1]
                if key == 'type':
                    key = 'target_id'
                print(f'{key} : {value}')
                driverArgs[key] = value
                #cLine = f.readline()
                
        if readState == READ_STATE_COLLECTING_DRIVER_VARIABLE:
            print('Collecting driver variable: ' + str(driverVariable))
            if '@BEGIN' in cLine or '@END' in cLine:
                print("")
            elif cLine[0] == '#': 
                print('')
            else:
                # split the line based on the "$:" delimiter
                cLineSplit = cLine.split(DELIMITER)
                key = cLineSplit[0]
                value = 0
                if len(cLineSplit) > 1:
                    # only name is found.  
                    value = cLineSplit[1]
                if key == 'type':
                    key = 'target_id'
                print(f'FOUND THIS: {key} : {value}')
                if driverVariable > len(driverArgs['var_list'])-1:
                    driverArgs['var_list'].append({})
                print('len var_list: '+str(len(driverArgs['var_list'])))
                driverArgs['var_list'][driverVariable][key] = value
                #driverArgs['var_list'][driverVariable] = {key:value}
                #cLine = f.readline()
            
            
        if readState == READ_STATE_COLLECTING_DRIVER_VARIABLE_TARGET:
            print(f'>collecting driver variable {driverVariable} variable target {driverVariableTarget}---')
            if '@BEGIN' in cLine or '@END' in cLine:
                print('')
            elif cLine[0] == '#': 
                print('')
            else:
                # split the line based on the "$:" delimiter
                cLineSplit = cLine.split(DELIMITER)
                key = cLineSplit[0]
                value = 0
                if len(cLineSplit) > 1:
                    # only name is found.  
                    value = cLineSplit[1]
                # maybe remove this????    
                #if key == 'type':
                    #key = 'target_id'
                    
                if driverVariableTarget > len(driverArgs['var_list'][driverVariable]['targets'])-1:
                    driverArgs['var_list'][driverVariable]['targets'].append({})
                    print('added 1, len is now: ' + str(len(driverArgs['var_list'][driverVariable]['targets'])))
                print(f'  >target key/value: {key} : {value}')
                #print(f'driverVariableTarget: {driverVariableTarget}')
                driverArgs['var_list'][driverVariable]['targets'][driverVariableTarget][key] = value
                print('  >this was just added:\n'+str(driverArgs['var_list'][driverVariable]['targets'][driverVariableTarget]))
                #print('targets HERE LOOK AT THIS:' + str(driverArgs['var_list'][driverVariable]['targets'][driverVariableTarget]))
                #cLine = f.readline()
            
                
        if readState == READ_STATE_FINALIZE_CONSTRAINT:
            #print(constraintsArgs)
            # add constraint.
            
            add_constraint_general(**constraintsArgs)
            
            # clear args
            constraintsArgs = {}
            # set reading to idle.
            readState = READ_STATE_IDLE
            #cLine = f.readline()
            
        if readState == READ_STATE_FINALIZE_DRIVER:
            # @todo make the driver with collected data.
            
            #print('driverArgs:\n'+str(driverArgs))
            #print('driverArgs[var_list]:\n'+str(driverArgs['var_list']))
            print('annoyingly long list stuff:')
            #print(driverArgs['var_list'][2]['variable_name'])
            #print(driverArgs['var_list'][2]['targets'])
            #print('driverArgs[var_list][1][targets]:\n'+str(driverArgs['var_list'][1]['targets']))
            print('')
            
            add_driver(**driverArgs)
            # reset everything
            driverArgs = {}
            driverArgs['target_id'] = armature
            driverArgs['var_list'] = [{}]
            driverVariable = 0
            driverVariableTarget = 0
            readState = READ_STATE_IDLE
            
    return 0  

        
            
            
# --------------------------------------------------------------------------