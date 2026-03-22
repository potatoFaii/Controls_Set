# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import json
import os
import importlib
import IndivPyControlsSet

try:
    from importlib import reload
except ImportError:
    pass
def safe_reload(module):
    try:
        reload(module)
    except Exception:
        try:
            import imp
            imp.reload(module)
        except Exception as e:
            print("Reload failed:", e)
def import_and_reload(module_path):
    try:
        mod = importlib.import_module(module_path)
        safe_reload(mod)
        short_name = module_path.split('.')[-1]
        globals()[short_name] = mod
        print("// {} loaded".format(module_path))
        return mod
    except Exception as e:
        print("// Failed to load {}: {}".format(module_path, e))
        return None
# LOAD SUBMODULES
import_and_reload("IndivPyControlsSet.ControlsSet_Func")
import_and_reload("IndivPyControlsSet.FilterCompare_UI")


class ControlsSet_UI(object):
    mayaVer = cmds.about(v=True)
    WINDOWUI = 'ControlSet_UI'
    
    def __init__(self,*args):
        self.controlSetWind()
    def controlSetWind(self,*args):
        if (cmds.window(self.WINDOWUI,q=True,ex=True)):
            cmds.deleteUI(self.WINDOWUI,wnd=True)
        cmds.window(self.WINDOWUI,t=self.WINDOWUI,mb=True,wh=(300,200),s=True,rtf=True)
        cmds.menu(l=' File ')
        cmds.menuItem(l='-List',d=True)
        cmds.menuItem(l='Tutorial',i='SP_FileIcon.png',c=lambda x:self.ControlsSetTutorialPath())
        cmds.menuItem(d=True)
        cmds.menu(l=' Reload ')
        cmds.menuItem(l='Reload',d=True)
        cmds.menuItem(l='-ReloadUI',i='QR_refresh.png',c=lambda x:ControlsSet_UI())
        cmds.menuItem(d=True)
        #
        mainFL = cmds.formLayout()
        titleFL = cmds.frameLayout(l="[ Controls_Set ]",la="center",cll=False,fn='boldLabelFont',bgc=(0.20,0.43,0.70),p=mainFL)
        cmds.formLayout(mainFL, e=True,attachForm=[(titleFL,'top',0),(titleFL,'left',5),(titleFL,'right',5)])
        #
        btnMainFL = cmds.formLayout()
        #btnFL = cmds.formLayout(bgc=(0.3,0.9,0.3)) # GREEN
        self.btnFL = cmds.formLayout(bgc=(0.9,0.3,0.3),p=btnMainFL) # RED
        cmds.formLayout(btnMainFL, e=True,attachForm=[(self.btnFL,'top',5),(self.btnFL,'left',0),(self.btnFL,'right',0)])
        btnFL2 = cmds.formLayout(bgc=(0.3,0.3,0.3))
        cmds.formLayout(self.btnFL, e=True,attachForm=[(btnFL2,'top',1),(btnFL2,'left',2),(btnFL2,'right',2),(btnFL2,'bottom',1)])
        alignSep = cmds.separator(style='in',hr=False,bgc=(1,1,1),h=10)
        sourceTxt = cmds.text(l='SourcePath :-')
        #
        self.sourceTxtF = cmds.textField(pht='{}'.format(cmds.internalVar(userScriptDir=True)),h=20)
        self.chaTxt = cmds.text(l='')
        jsonTxt = cmds.text(l='.json')
        sourcePopOut = cmds.popupMenu(p=self.btnFL)
        cmds.menuItem(l="- Load",d=True,p=sourcePopOut)
        cmds.menuItem(l="Grab JSON",i='search.png',p=sourcePopOut,ver=self.mayaVer,c=lambda x:self.grabFilePathCmd())
        cmds.menuItem(l="Empty",i='QR_refresh.png',p=sourcePopOut,c=lambda x:self.emptyFilePathCmd())
        cmds.menuItem(l="- Preset",d=True,p=sourcePopOut)
        cmds.menuItem(l="AdvancedSkeleton",i='ts-head3.png',p=sourcePopOut,c=lambda x:self.presetPathCmd('AdvancedSkeleton'))
        cmds.menuItem(l="NE_H74",i='ts-head2.png',p=sourcePopOut,c=lambda x:self.presetPathCmd('NE_H74'))
        sourceSep = cmds.separator(style='none')
        cmds.menuItem(l="- Json",d=True,p=sourcePopOut)
        cmds.menuItem(l="FilterSetup",i='navButtonBrowse.png',p=sourcePopOut,ver=self.mayaVer,c=lambda x:FilterCompare_UI.FilterCompare_UI())
        cmds.menuItem(d=True,p=sourcePopOut)

        cmds.formLayout(btnFL2, e=True,attachControl=[(sourceTxt,'left',5,alignSep),
                                                      (self.sourceTxtF,'top',3,sourceTxt),
                                                      (self.chaTxt,'top',3,self.sourceTxtF),
                                                      (jsonTxt,'top',3,self.sourceTxtF),
                                                      (self.chaTxt,'right',5,jsonTxt),
                                                      (sourceSep,'top',8,self.chaTxt)],
                                          attachForm=[(alignSep,'top',7),(alignSep,'left',8),
                                                      (sourceTxt,'top',5),(sourceTxt,'left',8),
                                                      (self.sourceTxtF,'top',0),(self.sourceTxtF,'left',5),(self.sourceTxtF,'right',5),
                                                      (jsonTxt,'right',10)])
        
        
        rmdFL = cmds.formLayout(p=btnMainFL)
        cmds.formLayout(btnMainFL, e=True,attachControl=[(rmdFL,'top',2,self.btnFL)],
                                             attachForm=[(rmdFL,'left',0),(rmdFL,'right',0)])
        rmdTxt = cmds.text(l='*Right Click To Function',en=False,fn='obliqueLabelFont')
        rmdSep = cmds.separator(style='double',bgc=(0,0,0),h=1)
        cmds.formLayout(rmdFL, e=True,attachControl=[(rmdSep,'top',5,rmdTxt)],
                                         attachForm=[(rmdTxt,'left',5),(rmdTxt,'right',5),
                                                     (rmdSep,'left',0),(rmdSep,'right',0)])
        
        # Button
        autoFL = cmds.formLayout(p=btnMainFL)
        cmds.formLayout(btnMainFL, e=True,attachControl=[(autoFL,'top',0,rmdFL)],
                                             attachForm=[(autoFL,'left',0),(autoFL,'right',0)])
        CSBtnFL = cmds.formLayout(bgc=(0.0,0.0,0.0))
        cmds.formLayout(autoFL, e=True,attachForm=[(CSBtnFL,'top',10),(CSBtnFL,'left',5),(CSBtnFL,'right',5)])
        CSBtn = cmds.button(l='Controls_Set',bgc=(1.0,0.65,0.20),c=lambda x:self.controls_set_func())
        cmds.formLayout(CSBtnFL, e=True,attachForm=[(CSBtn,'left',2),(CSBtn,'right',2),(CSBtn,'top',2),(CSBtn,'bottom',2)])
        cmds.setParent('..')
        
        self.CSCondCB = cmds.checkBox(l='Condition',v=False,cc=lambda x:self.CSCondToggleFunc())
        cmds.formLayout(autoFL, e=True,attachControl=[(self.CSCondCB,'top',2,CSBtnFL)],
                                          attachForm=[(self.CSCondCB,'left',10)])
        self.condFL = cmds.formLayout(bgc=(0.2,0.2,0.2),vis=False)
        cmds.formLayout(autoFL, e=True,attachControl=[(self.condFL,'top',2,self.CSCondCB)],
                                          attachForm=[(self.condFL,'left',5),(self.condFL,'right',5)])
        self.incCB = cmds.checkBox(l='Include',v=False)
        self.excCB = cmds.checkBox(l='Exclude',v=False)
        condSep = cmds.separator(style='none')
        cmds.formLayout(self.condFL, e=True,attachControl=[(self.excCB,'top',2,self.incCB),
                                                      (condSep,'top',5,self.excCB)],
                                          attachForm=[(self.incCB,'top',5),(self.incCB,'left',5),
                                                      (self.excCB,'left',5)])
        CSSep = cmds.separator(style='double',bgc=(0,0,0),h=1,p=autoFL)
        cmds.formLayout(autoFL, e=True,attachControl=[(CSSep,'top',15,self.condFL)],
                                          attachForm=[(CSSep,'left',0),(CSSep,'right',0)])
        EndSep = cmds.separator(style='none',p=btnMainFL)
        cmds.formLayout(btnMainFL, e=True,attachControl=[(EndSep,'top',20,autoFL)])
        # ShowWindow
        cmds.showWindow(self.WINDOWUI)

    def ControlsSetTutorialPath(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_dir = script_dir.replace("IndivPyControlsSet","03_Tutorial")
        try:
            os.startfile(script_dir)
        except IOError:
            QGuideText = 'Error: Failed to load Q guide.'
    def emptyFilePathCmd(self,*args):
        cmds.textField(self.sourceTxtF,e=True,tx='')
        cmds.text(self.chaTxt,e=True,l='')
        cmds.formLayout(self.btnFL,e=True,bgc=(0.9,0.3,0.3)) # RED
    
    def presetPathCmd(self,presetName):
        moduleDir = os.path.dirname(os.path.abspath(__file__))
        baseDir = os.path.dirname(moduleDir)
        presetDir = os.path.join(baseDir, "01_Preset")
        if not os.path.isdir(presetDir):
            os.makedirs(presetDir)
        presetPath = os.path.join(presetDir, presetName + ".json")
        presetPath = os.path.normpath(presetPath).replace('\\', '/')
        cmds.textField(self.sourceTxtF,e=True,tx=presetDir)
        cmds.text(self.chaTxt,e=True,l=presetName)
        cmds.formLayout(self.btnFL,e=True,bgc=(0.3,0.9,0.3)) # GREEN
        return presetPath

    def jsonPath(self):
        rawPath = cmds.textField(self.sourceTxtF,q=True,tx=True)
        jsonFile = cmds.text(self.chaTxt,q=True,l=True)
        if not rawPath or not jsonFile:
            return None
        fullPath = os.path.join(rawPath, jsonFile + ".json")
        fullPath = os.path.normpath(fullPath).replace('\\', '/')
        return fullPath

    def grabFilePathCmd(self,*args):
        txtFieldGrp = self.sourceTxtF
        rawPath = cmds.textField(txtFieldGrp,q=True,tx=True)
        startDir = ""
        if rawPath :
            if os.path.isdir(rawPath):
                startDir = rawPath
            elif os.path.isdir(os.path.dirname(rawPath)):
                startDir = os.path.dirname(rawPath)
		# FilterCompare_lastDir string key name for a Maya optionVar.
        if not startDir and cmds.optionVar(exists="FilterCompare_lastDir"):
            lastDir = cmds.optionVar(q="FilterCompare_lastDir")
            if os.path.isdir(lastDir):
                startDir = lastDir
        if not startDir:
            startDir = cmds.internalVar(userWorkspaceDir=True)
        startDir = os.path.normpath(startDir) + os.sep
        result  = cmds.fileDialog2(
                            dialogStyle=2,
                            fileMode=1,
                            startingDirectory=startDir,
                            fileFilter="JSON Files (*.json)"
                        )
        if not result:
            cmds.formLayout(self.btnFL,e=True,bgc=(0.9,0.3,0.3)) # RED
            cmds.text(self.chaTxt,e=True,l='')
            return
        filePath = os.path.normpath(result[0])
        sourcePath = os.path.dirname(filePath)
        jsonName = os.path.splitext(os.path.basename(filePath))[0]
        #
        cmds.text(self.chaTxt,e=True,l=jsonName)
        cmds.textField(txtFieldGrp,e=True,tx=sourcePath)
        cmds.formLayout(self.btnFL,e=True,bgc=(0.3,0.9,0.3)) # GREEN
        cmds.optionVar(sv=("FilterCompare_lastDir", sourcePath))
        mel.eval('print ("REMINDER : SourcePath  <COMPLETE> \\n")')
    
    def CSCondToggleFunc(self):
        CBCheck = cmds.checkBox(self.CSCondCB,q=True,v=True)
        cmds.formLayout(self.condFL,e=True,vis=CBCheck)
        mel.eval('print ("REMINDER : Condition <{}> \\n")'.format(CBCheck))
    
    def controls_set_func(self):
        path = self.jsonPath()
        if not path:
            return
        incCheck = cmds.checkBox(self.incCB,q=True,v=True)
        excCheck = cmds.checkBox(self.excCB,q=True,v=True)
        ControlsSet_Func.controls_set_func(incCheck,excCheck,path,forceReload=True)

if __name__== '__main__' :
  try:
    ControlsSet_UI()
  except:
      pass