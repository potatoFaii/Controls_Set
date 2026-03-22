
import maya.cmds as cmds
import maya.mel as mel
import json
import os

_JSON_CACHE = {}
#   _____________  
# _/_JSON SETUP_/_ 
def obtainPresetData(path):
	if not os.path.exists(path):
		cmds.warning("Preset file does not exists.")
		return None
	try:
		with open(path, "r") as f:
			return json.load(f)
	except ValueError as e:
		cmds.warning("Failed to load preset file.")
		print("JSON  Error:{}".format(e))
		return None
# Load json file here
def loadPresetData(path, forceReload=False):
    global _JSON_CACHE
    if not forceReload and path in _JSON_CACHE:
        return _JSON_CACHE[path]
    data = obtainPresetData(path)
    _JSON_CACHE[path] = data or {}
    return _JSON_CACHE[path]
#  ________________
#_/_ Controls_Set_/ #
def createSetFunction(setName='Controls_Set'):
    if cmds.objExists(setName):
        cmds.delete(setName)
    cmds.sets(n=setName, em=True)
    print('REMINDER : {} READY'.format(setName))
    return setName
def getTransformNode():
	result = []
	ctrlShape = cmds.ls(type='nurbsCurve',long=True) or []
	for shape in ctrlShape:
		if not isNotReference(shape):
			continue
		parents = cmds.listRelatives(shape,p=True,type='transform') or []
		if not parents:
			continue
		tr = parents[0]
		if not isNotReference(tr):
			continue
		if not isVisible(tr):
			continue
		result.append(tr)
	return sorted(set(result))
def isVisible(obj):
    if not cmds.objExists("{}.visibility".format(obj)):
        return True
    return cmds.getAttr("{}.visibility".format(obj))
def isNotReference(obj):
	if not cmds.objExists("{}.overrideEnabled".format(obj)):
		return True
	if cmds.getAttr("{}.overrideEnabled".format(obj)):
		return cmds.getAttr("{}.overrideDisplayType".format(obj)) != 2
	return True
def getExcludeList(path,forceReload=False):
	exclude = set()
	data = loadPresetData(path,forceReload)
	grpList =  data.get("excludeList", [])  # Load json
	for grp in grpList:
		if not cmds.objExists(grp):
			print("//  Exclude group missing: [ {} ]".format(grp))
			continue
		exclude.add(grp)
		child = cmds.listRelatives(grp,ad=True,type='transform') or []
		exclude.update(child)
	return exclude
def getIncludeList(path,forceReload=False):
	include = set()
	data = loadPresetData(path,forceReload)
	grpList =  data.get("includeListItems", [])  # Load json
	for grp in grpList:
		if not cmds.objExists(grp):
			print("//  Include group missing: [ {} ]".format(grp))
			continue
		include.add(grp)
		child = cmds.listRelatives(grp,ad=True,type='transform') or []
		include.update(child)
	return include
def filterVisibleNodes(cbInBtn, cbExBtn, nodes, path, forceReload=False):
	includeSet = set()
	excludeSet = set()
	print(cbInBtn, cbExBtn)
	if cbInBtn:
		includeSet = getIncludeList(path, forceReload)
		if not includeSet:
			cmds.warning("Include enabled but include list is empty - ignoring include filter")
			cbInBtn = False
	if cbExBtn:
		excludeSet = getExcludeList(path, forceReload)
	result = []
	for obj in nodes:
		if cbInBtn:
			if obj not in includeSet:
				continue 
		if cbExBtn:
			if obj in excludeSet:
				continue
		if not isVisible(obj):
			continue
		result.append(obj)
	return result

def controls_set_func(cbInBtn,cbExBtn,path,forceReload=True):
	# Before query shape , isNotReference already start filter
	ctrlTransform = getTransformNode()
	ctrlFilter = filterVisibleNodes(cbInBtn,cbExBtn,ctrlTransform,path,forceReload)
	if ctrlFilter:
		ctrlSet = createSetFunction(setName='Controls_Set')
		cmds.sets(ctrlFilter,add=ctrlSet)
		cmds.select(ctrlFilter)
		mel.eval('print("\\REMINDER : [ {} ] controllers for < Controls_Set >\\n")'.format(len(ctrlFilter)))


