import maya.cmds as cmds
import maya.mel as mel
import json
import os
#  ________________
#_/_ Controls_Set_/ #
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
def filterVisibleNodes(nodes):
	result = []
	for obj in nodes:
		if not isVisible(obj):
			continue
		result.append(obj)
	return result
def filterLoadedNodes():
	ctrlTransform = getTransformNode()
	ctrlFilter = filterVisibleNodes(ctrlTransform)
	return ctrlFilter if ctrlFilter else []