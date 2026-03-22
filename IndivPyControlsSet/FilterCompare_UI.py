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
import_and_reload("IndivPyControlsSet.FilterLoad")


class FilterCompare_UI(object):
	# Focus on maya2020 first
	mayaVer = cmds.about(v=True)
	WINDOW = 'ControlSet_Compare_UI'
	INST_WINDOW = 'ControlSet_Compare_InstructionUI'
	JOB_NAME = 'ControlSet_UI_selSyncJob'

	def __init__(self,*args):
		self._lastPresetDir = None
		self.FilterCompare_Wind()
	
	def FilterCompare_Wind(self,*args):
		if (cmds.window(self.WINDOW,q=True,ex=True)):
			cmds.deleteUI(self.WINDOW,wnd=True)
		cmds.window(self.WINDOW,t=self.WINDOW,mb=True,wh=(400,400),s=True,rtf=True)
		cmds.menu(l=' Menu ')
		cmds.menuItem(l='-List',divider=True)
		cmds.menuItem(l='Tutorial_Path',i='SP_FileIcon.png',c=lambda x:self.filterCompareTutorialPath())
		cmds.menuItem(l='Log',i='fileNew.png',c=lambda x:self.filterCompareScriptLog())
		cmds.menuItem(l='-Save',divider=True)
		cmds.menuItem(l='Save As',i='fileSave.png',ver=self.mayaVer,c=lambda x:self.saveLoadedPresetList())
		cmds.menuItem(divider=True)
		cmds.menu(l=' Reload ')
		cmds.menuItem(l='-Load',divider=True)
		cmds.menuItem(l='ReloadUI',i='clockwise.png',c=lambda x:FilterCompare_UI())
		
		maintabs = cmds.tabLayout()
		mainForm = cmds.formLayout()
		# -- Path --
		pathForm = cmds.formLayout(p=mainForm)
		cmds.formLayout(mainForm, e=True, attachForm=[(pathForm,"left",5),(pathForm,"right",5),(pathForm,"top",0)])
		
		self.sourceTxtF = cmds.textField(pht='{}'.format(cmds.internalVar(userScriptDir=True)),h=20,ec=lambda x:self.grabFilePathCmd())
		sourceTxtPopOut = cmds.popupMenu(p=self.sourceTxtF)
		cmds.menuItem(l="- Load",d=True,p=sourceTxtPopOut)
		cmds.menuItem(l="Load JSON",i='search.png',p=sourceTxtPopOut,ver=self.mayaVer,c=lambda x:self.grabFilePathCmd())
		cmds.menuItem(l="- Preset",d=True,p=sourceTxtPopOut)
		cmds.menuItem(l="Location",i='SP_DirOpenIcon.png',p=sourceTxtPopOut,c=lambda x:self.presetLocationCmd())
		cmds.menuItem(d=True,p=sourceTxtPopOut)
		#
		sourceSep = cmds.separator(style='double',bgc=(0.20,0.20,0.20),h=3)
		cmds.formLayout(pathForm, e=True, attachControl=[(sourceSep,"top",5,self.sourceTxtF)],
											 attachForm=[(self.sourceTxtF,"left",0),(self.sourceTxtF,"right",0),(self.sourceTxtF,"top",5),
											 			 (sourceSep,"left",0),(sourceSep,"right",0)])

		cmds.tabLayout(maintabs,e=True,tabLabel=[mainForm,' Input ']) # Adding tab

		panelForm = cmds.formLayout(p=mainForm)
		cmds.formLayout(mainForm,e=True,attachControl=[(panelForm,"top",0,pathForm)],
										   attachForm=[(panelForm,"top",0),(panelForm,"left",5),(panelForm,"right",5),(panelForm,"bottom",100)])
	    # ----- Column 1 -----
		col1 = cmds.formLayout(p=panelForm,bgc=(0.25,0.30,0.30))
		t1 = cmds.text(l='Filter_From_Scene')
		self.tsl1 = cmds.textScrollList(ams=True,dcc=lambda:self.getSelected(self.tsl1))
		tsl1PM = cmds.popupMenu(p=self.tsl1)
		cmds.menuItem(l="- Function",d=True,p=tsl1PM)
		cmds.menuItem(l="List From Scene",i='timeplaySequencer.png',p=tsl1PM,c=lambda x:self.filterFromScene())
		cmds.menuItem(l="- Selection",d=True,p=tsl1PM)
		cmds.menuItem(l="Select All",i='aselect.png',p=tsl1PM,c=lambda x:self.filterSelectAll(self.tsl1))
		cmds.menuItem(l="Clear",p=tsl1PM,c=lambda x: self.clearTSLList(self.tsl1))
		cmds.menuItem(l="- Move To",d=True,p=tsl1PM)
		cmds.menuItem(l="Exclude",i='moveUVRight.png',p=tsl1PM,ver=self.mayaVer,c=lambda x:self.excludeMoveFunc(self.tsl1))
		cmds.menuItem(l="Final",i='UVTkArrowRight.png',p=tsl1PM,ver=self.mayaVer,c=lambda x:self.finalMoveFunc(self.tsl1))
		cmds.menuItem(l='-Filter',divider=True,p=tsl1PM)
		cmds.menuItem(l='isVisible',cb=True,en=False,p=tsl1PM)
		cmds.menuItem(l='isReference',cb=True,en=False,p=tsl1PM)
		cmds.menuItem(l='isConnections',cb=True,en=False,p=tsl1PM)
		
		cmds.menuItem(d=True,p=tsl1PM)
		self.FFSNumTxt = cmds.text(l='[ Items: 0/0 ]')
		cmds.formLayout(col1, e=True, attachControl=[(self.tsl1,"top",5,t1)],
										 attachForm=[(t1,"top",5),(t1,"left",5),(t1,"right",5),
										 			 (self.tsl1,"left",5),(self.tsl1,"right",0),(self.tsl1,"bottom",23),
										 			 (self.FFSNumTxt,"right",10),(self.FFSNumTxt,"bottom",5)])
	    # ----- Column 2 -----
		col2 = cmds.formLayout(p=panelForm,bgc=(0.35,0.30,0.30))
		t2 = cmds.text(l='Exclude_List')
		cmds.formLayout(col2, e=True,attachForm=[(t2,"top",0),(t2,"left",0),(t2,"right",0)])
		
		pane = cmds.paneLayout(cn='horizontal2',paneSize=[(1,20,20),(2,80,80)],parent=col2)
		cmds.formLayout(col2, e=True,attachForm=[(t2,"top",5),(t2,"left",5),(t2,"right",5),
                                        		 (pane,"left",0),(pane,"right",0),(pane,"bottom",22)],
                                  attachControl=[(pane,"top",5,t2)])
		self.tsl2Grp = cmds.textScrollList(ams=True,dcc=lambda:self.getSelected(self.tsl2Grp))
		self.tsl2 = cmds.textScrollList(ams=True,dcc=lambda:self.getSelected(self.tsl2))
		self.ELNumTxt = cmds.text(l='[ Items: 0/0 ]',p=col2)
		cmds.formLayout(col2, e=True, attachForm=[(self.ELNumTxt,"right",10),(self.ELNumTxt,"bottom",5)])
		
		# Popup menu
		tsl2GrpPM = cmds.popupMenu(p=self.tsl2Grp)
		cmds.menuItem(l="- Function", d=True, p=tsl2GrpPM)
		cmds.menuItem(l="List Null From Script", i='SP_FileDialogDetailedView.png', p=tsl2GrpPM,c=lambda *_: self.refreshExcludeList(self.tsl2Grp,key="excludeList"))
		cmds.menuItem(l="- Selection",d=True,p=tsl2GrpPM)
		cmds.menuItem(l="Select All",i='aselect.png',p=tsl2GrpPM,c=lambda x:self.filterSelectAll(self.tsl2Grp))
		cmds.menuItem(l="Add Selection",p=tsl2GrpPM,ver=self.mayaVer,c=lambda x:self.exludeNullSelFunc())
		cmds.menuItem(l="Remove Selection",i='QR_delete.png',p=tsl2GrpPM,c=lambda x:self.excludeNullRemoveFunc())
		cmds.menuItem(d=True,p=tsl2GrpPM)
		
		# Popup menu
		tsl2PM = cmds.popupMenu(p=self.tsl2)
		cmds.menuItem(l="- Function", d=True, p=tsl2PM)
		cmds.menuItem(l="Filter From Above", i='timeplaySequencer.png', p=tsl2PM,c=lambda *_: self.filterFromAbove())
		cmds.menuItem(l="List From Script", i='SP_FileDialogDetailedView.png', p=tsl2PM,c=lambda *_: self.refreshExcludeList(self.tsl2,key="excludeListItems"))
		cmds.menuItem(l="- Selection",d=True,p=tsl2PM)
		cmds.menuItem(l="Select All",i='aselect.png',p=tsl2PM,c=lambda x:self.filterSelectAll(self.tsl2))
		'''
		cmds.menuItem(l="- Move To", d=True, p=tsl2PM)
		cmds.menuItem(l="Include",i='moveUVLeft.png',p=tsl2PM,ver=self.mayaVer)
		cmds.menuItem(l="Final",i='UVTkArrowRight.png',p=tsl2PM,ver=self.mayaVer,c=lambda x:self.moveToFinalFunc())
		'''
		cmds.menuItem(d=True,p=tsl2PM)

	    # ----- Column 3 -----
		col3 = cmds.formLayout(p=panelForm)
		t3 = cmds.text(l='Final_List')
		self.FLNumTxt = cmds.text(l='[ Items: 0/0 ]')
		self.tsl3 = cmds.textScrollList(ams=True,dcc=lambda:self.getSelected(self.tsl3))
		tsl3PM = cmds.popupMenu(p=self.tsl3)
		cmds.menuItem(l="- Function",d=True,p=tsl3PM)
		cmds.menuItem(l="List Output",i='timeplaySequencer.png',p=tsl3PM,c=lambda x: self.filterFinalList())
		cmds.menuItem(l="Filter From Script",i='SP_FileDialogDetailedView.png',p=tsl3PM,c=lambda *_: self.refreshExcludeList(self.tsl3,key="includeListItems"))
		cmds.menuItem(l="- Selection",d=True,p=tsl3PM)
		cmds.menuItem(l="Select All",i='aselect.png',p=tsl3PM,c=lambda x:self.filterSelectAll(self.tsl3))
		cmds.menuItem(l="Clear",p=tsl3PM,c=lambda x: self.clearTSLList(self.tsl3))
		
		cmds.formLayout(col3, e=True, attachControl=[(self.tsl3,"top",5,t3)],
				  						 attachForm=[(t3,"top",5),(t3,"left",5),(t3,"right",5),
	                                            	 (self.tsl3,"left",0),(self.tsl3,"right",5),(self.tsl3,"bottom",23),
	                                            	 (self.FLNumTxt,"right",10),(self.FLNumTxt,"bottom",5)])
	    # ----- Attach columns proportionally ----- #
		cmds.formLayout(panelForm, e=True, attachForm=[(col1,"top",5),(col1,"bottom",5),
													(col2,"top",5),(col2,"bottom",5),
													(col3,"top",5),(col3,"bottom",5)],
									attachPosition=[(col1,"left",0,0),(col1,"right",0,33),
													(col2,"left",0,33),(col2,"right",0,66),
													(col3,"left",0,66),(col3,"right",0,100)])
		cmds.setParent('..')
		cmds.setParent('..')

		belowFL = cmds.formLayout()
		cmds.formLayout(mainForm, e=True,attachForm=[(belowFL,"left",5),(belowFL,"right",5)],
									  attachControl=[(belowFL,"top",0,panelForm)])
		
		btnSep = cmds.separator(style='double',bgc=(0.2,0.2,0.2),h=1)
		cmds.formLayout(belowFL, e=True,attachForm=[(btnSep,"left",0),(btnSep,"right",0)])
		
		# Filter_Scene_Exclude
		cmds.setParent('..')
		FSE_FL = cmds.formLayout(bgc=(0.1,0.1,0.1),p=belowFL)
		cmds.formLayout(belowFL, e=True,attachControl=[(FSE_FL,'top',10,btnSep)],
		                                   attachForm=[(FSE_FL,"left",5),(FSE_FL,"right",5)],
		                               attachPosition=[(FSE_FL,"left",0,1),(FSE_FL,"right",2,66)])
		FSEBtn = cmds.button(l=' -> Filter_Scene_Exclude_ ',bgc=(0.9,0.65,0.40),p=FSE_FL,c=lambda x:self.filterLoad())
		cmds.formLayout(FSE_FL,e=True,attachForm=[(FSEBtn,"top",2),(FSEBtn,"left",2),(FSEBtn,"right",2),(FSEBtn,"bottom",2)])

		CSBtn = cmds.button(l='Controls_Set_Output',p=belowFL,bgc=(0.7,0.7,0.4),c=lambda x:self.controlsSetFunc())
		cmds.formLayout(belowFL, e=True,attachControl=[(CSBtn,'top',12,btnSep)],
		                                   attachForm=[(CSBtn,"left",5),(CSBtn,"right",5)],
		                               attachPosition=[(CSBtn,"left",2,66),(CSBtn,"right",0,99)])
		sTabForm = cmds.formLayout(p=maintabs)
		cmds.tabLayout(maintabs,e=True,tabLabel=[sTabForm,' Compare ']) # Adding tab
		cmds.text(l='COMING SOON')
		# NumCount
		self.numRefreshFunc()
	    # ScriptJob
		self.create_selection_job()
		cmds.showWindow(self.WINDOW)
    
    # ----- MenuItem LIST ----- #
	def guideWindow(self,instructionNote):
		if (cmds.window(self.INST_WINDOW ,q=True, exists = True)):
			cmds.deleteUI(self.INST_WINDOW,window=True)
		instructW = self.INST_WINDOW
		insWindow = cmds.window(instructW ,t=instructW,widthHeight=(250,400))
		FLayout = cmds.formLayout(numberOfDivisions = 100)
		FPanel = cmds.paneLayout( configuration='horizontal4')
		cmds.formLayout(FLayout,edit=True,attachForm =[(FPanel,"top",10),(FPanel,"bottom",10),(FPanel,"left",10),(FPanel,"right",10)])
		cmds.scrollField( editable=False, wordWrap=True, text=instructionNote)
		cmds.showWindow(insWindow)
	def filterCompareScriptLog(self):
		script_dir = os.path.dirname(os.path.abspath(__file__))
		script_dir = script_dir.replace("IndivPyControlsSet","10_Log")
		file_pathQ = os.path.join(script_dir, "CompareUI_ScriptLog.py")
		print(file_pathQ)
		try:
			with open(file_pathQ, 'r') as file:
				QGuideText = file.read()
		except IOError:
			QGuideText = 'Error: Failed to load Q guide.'
		self.guideWindow(QGuideText)
	def filterCompareTutorialPath(self):
		script_dir = os.path.dirname(os.path.abspath(__file__))
		script_dir = script_dir.replace("IndivPyControlsSet","03_Tutorial")
		try:
			os.startfile(script_dir)
		except IOError:
			QGuideText = 'Error: Failed to load Q guide.'
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
		script_file = cmds.fileDialog2(
	        dialogStyle=2,
	        fileMode=1,
	        startingDirectory=startDir,
	        fileFilter="JSON Files (*.json)"
	    )
		if script_file:
			cmds.optionVar(sv=("FilterCompare_lastDir", os.path.dirname(script_file[0])))
			cmds.textField(txtFieldGrp,e=True,tx=script_file[0])
			mel.eval('print ("REMINDER : File selection  <COMPLETE> \\n")')
		else:
			cmds.warning("File selection cancelled.")
	
	def presetLocationCmd(self):
		script_dir = os.path.dirname(os.path.abspath(__file__))
		script_dir = script_dir.replace("IndivPyControlsSet","01_Preset")
		os.startfile(script_dir)
        
	def resolveSaveFolder(self): # Ensure path return True
		folderPath = cmds.textField(self.sourceTxtF, q=True, tx=True)
		if folderPath:
			if os.path.isdir(folderPath):
				return folderPath
		scenePath = cmds.file(q=True, sn=True)
		if scenePath:
			return os.path.dirname(scenePath)
		projectDir = cmds.workspace(q=True, rd=True)
		if projectDir:
			return projectDir
		return cmds.internalVar(userScriptDir=True)
	
	def excludeListSaveFunc(self):
		items = cmds.textScrollList(self.tsl2Grp,q=True,ai=True) or []
		return {"excludeList":items}
	def excludeListItemsSaveFunc(self):
		items = cmds.textScrollList(self.tsl2,q=True,ai=True) or []
		return {"excludeListItems":items}
	def includeListItemsSaveFunc(self):
		items = cmds.textScrollList(self.tsl3,q=True,ai=True) or []
		return {"includeListItems":items}

	def saveLoadedPresetList(self):
		try:
			txtFieldGrp = self.sourceTxtF
			rawPath = cmds.textField(txtFieldGrp, q=True, tx=True)
			startDir = ""
			if rawPath:
				if os.path.isdir(rawPath):
					startDir = rawPath
				elif os.path.isdir(os.path.dirname(rawPath)):
					startDir = os.path.dirname(rawPath)
			if not startDir and cmds.optionVar(exists="FilterCompare_lastDir"):
				lastDir = cmds.optionVar(q="FilterCompare_lastDir")
				if os.path.isdir(lastDir):
					startDir = lastDir
			if not startDir:
				startDir = cmds.internalVar(userWorkspaceDir=True)
			startDir = os.path.normpath(startDir) + os.sep
			result = cmds.fileDialog2(
                				dialogStyle=2,
                				fileMode=0,
                				caption="Save Preset",
                				startingDirectory=startDir,
                				fileFilter="JSON Files (*.json)")
			if not result:
				cmds.warning("Save As cancelled")
				return
			fullPath = os.path.normpath(result[0]).replace('\\', '/')
			if not fullPath.lower().endswith(".json"):
				fullPath += ".json"
			cmds.optionVar(sv=("FilterCompare_lastDir", os.path.dirname(fullPath)))

			if os.path.exists(fullPath):
				confirm = cmds.confirmDialog(
					title="Confirm Overwrite",
					message="A preset already exists. Do you want to replace it?",
					button=["Yes", "No"],
					defaultButton="No",
					cancelButton="No",
					dismissString="No"
				)
				if confirm != "Yes":
					cmds.warning("File not overwritten")
					return

			listDataExport = {}
			listDataExport.update(self.excludeListItemsSaveFunc())
			listDataExport.update(self.includeListItemsSaveFunc())
			listDataExport.update(self.excludeListSaveFunc())
			with open(fullPath, "w") as f:
				json.dump(listDataExport, f, indent=4)
			mel.eval('print ("REMINDER : Save Preset <COMPLETE>\\n")')
		except OSError as e:
			print("Error:", e)
			cmds.warning("Failed to create PresetList.")
		
		
		def saveAsPresetList(self,listDataExport):
			folderPath = cmds.textField(self.sourceTxtF,q=True,tx=True)
			try:
				folderPath = self.resolveSaveFolder()
				if not os.path.exists(folderPath):
					cmds.warning("[ {} ] <DOESN'T EXIST> , check the folderPath.".format(folderPath))
					return
				result = cmds.fileDialog2(
					fileMode=0,
					caption="Save Preset As",
					startingDirectory=folderPath,
					fileFilter="JSON (*.json)"
				)
				if not result:
					cmds.warning("Save As cancelled")
					return
				fullData = result[0]
				fullData = os.path.normpath(fullData).replace('\\', '/')
				if not fullData.lower().endswith(".json"):
					fullData += ".json"
				if os.path.exists(fullData):
					if f.read().strip():
						confirm = cmds.confirmDialog(
							title="Confirm Overwrite",
							message="A preset already exists. Do you want to replace it?",
							button=["Yes", "No"],
							defaultButton="No",
							cancelButton="No",
							dismissString="No"
						)
						if confirm == "No":
							cmds.warning("File not overwritten")
							return
				with open(fullData, "w") as f:
					json.dump(listDataExport, f, indent=4)
				mel.eval('print ("REMINDER : Save Preset <COMPLETE> \\n")')
			except OSError as e:
				print("Error:", e)
				cmds.warning("Failed to create PresetList.")
	# ----- MenuItem LIST END----- #

	# ----- ScriptJob ----- #
	def sync_tsl_with_scene(self,*args):
		sel = cmds.ls(sl=True) or []
		if not sel:
			return
		tslList = [self.tsl1,self.tsl2Grp,self.tsl2,self.tsl3]
		for tsl in tslList:
			if not cmds.textScrollList(tsl,q=True,ex=True):
				return
			items = cmds.textScrollList(tsl,q=True,ai=True) or []
			match = [obj for obj in sel if obj in items]
			cmds.textScrollList(tsl,e=True,da=True)
			if match:
				cmds.textScrollList(tsl,e=True,si=match)
	def create_selection_job(self):
		for j in cmds.scriptJob(lj=True): # Kill existing job (important!)
			if self.JOB_NAME in j:
				cmds.scriptJob(k=int(j.split(':')[0]), f=True)
		cmds.scriptJob(e=["SelectionChanged",self.sync_tsl_with_scene],protected=True,p=self.WINDOW)
	def getSelected(self,textScroll):
		exist = []
		missing = []
		tslSel = cmds.textScrollList(textScroll,query=True,selectItem=True)
		for obj in tslSel:
			if cmds.objExists(obj):
				exist.append(obj)
			else:
				missing.append(obj)
		if exist:
			cmds.select(exist, r=True)
		else:
			cmds.warning("No existing objects selected")
		return exist, missing
	
	# ----- ScriptJob END ----- #
	
	def refreshExcludeList(self,TSL,key="excludeList"):
		cmds.textScrollList(TSL,e=True,ra=True)
		path = cmds.textField(self.sourceTxtF,q=True,tx=True)
		if not os.path.exists(path):
			cmds.warning("JSON file not found")
			return
		try:
			with open(path,'r')as f:
				data = json.load(f)
		except Exception as e:
			cmds.warning("Failed to read JSON: {}".format(e))
			return
		excludeList = data.get(key,[])
		if excludeList:
			for item in excludeList:
				cmds.textScrollList(TSL,e=True,a=item)
		self.numRefreshFunc()
		mel.eval('print ("REMINDER : Refresh List <COMPLETE> \\n")')

	# ----- TextField Function ----- #
	# -- LoadData To TextField -- #
	def numRefreshFunc(self):
		txtLists = [self.tsl1,self.tsl2,self.tsl3]
		txtLabels = [self.FFSNumTxt,self.ELNumTxt,self.FLNumTxt]
		for tsl,txt in zip(txtLists,txtLabels):
			allItems = cmds.textScrollList(tsl,q=True,ai=True) or []
			num = len(allItems)
			cmds.text(txt,e=True,l='[ Items: {}/{} ]'.format(num,num))
	
	def filterSelectAll(self,TSL):
		items = cmds.textScrollList(TSL, q=True, ai=True) or []
		if not items:
			return [],[]
		exist = []
		missing = []
		for obj in items:
			if cmds.objExists(obj):
				exist.append(obj)
			else:
				missing.append(obj)
		cmds.textScrollList(TSL, e=True, si=items)
		if exist:
			cmds.select(exist, r=True)
			if missing:
				cmds.warning("{} item(s) do not exist and were ignored".format(len(missing)))
		else:
			cmds.warning("No existing objects selected")
		return exist, missing

	def filterFromScene(self):
		filterList = FilterLoad.filterLoadedNodes() or []
		cmds.textScrollList(self.tsl1,e=True,ra=True)
		for fl in filterList:
			cmds.textScrollList(self.tsl1,e=True,append=fl)
		self.numRefreshFunc()
		mel.eval('print("\\REMINDER : Filter from scene < COMPLETE >\\n")')
	
	def filterFromAbove(self):
		nullList = cmds.textScrollList(self.tsl2Grp,q=True,ai=True) or []
		prntList = set()
		cmds.textScrollList(self.tsl2, e=True, ra=True)
		if not nullList:
			return
		for null in nullList:
			if not cmds.objExists(null):
				continue
			child = cmds.listRelatives(null,ad=True,typ='nurbsCurve')
			if child:
				for ch in child:
					prnt = cmds.listRelatives(ch,p=True)
					prntList.add(prnt[0])
		prntList = sorted(prntList)
		cmds.textScrollList(self.tsl2,e=True,ra=True)
		if prntList:
			for pnt in prntList:
				cmds.textScrollList(self.tsl2,e=True,a=pnt)
		self.numRefreshFunc()
		mel.eval('print("\\REMINDER : Filter from above < COMPLETE >\\n")')
	
	def exludeNullSelFunc(self):
		nullList = set(cmds.textScrollList(self.tsl2Grp,q=True,ai=True) or [])
		selection = cmds.ls(sl=True)
		if not selection:
			return
		for sel in selection:
			if sel not in nullList:
				cmds.textScrollList(self.tsl2Grp,e=True,a=sel)
				nullList.add(sel)
		self.numRefreshFunc()
		mel.eval('print ("REMINDER : Add selection <COMPLETE> \\n")')

	def excludeNullRemoveFunc(self):
		selectedItems = cmds.textScrollList(self.tsl2Grp, q=True, si=True) or []
		if not selectedItems:
			cmds.warning("No items selected in list")
			return
		for item in selectedItems:
			cmds.textScrollList(self.tsl2Grp, e=True, ri=item)
		self.numRefreshFunc()
		mel.eval('print ("REMINDER : Remove selection <COMPLETE> \\n")')

	def filterLoad(self):
		self.filterFromScene()
		self.refreshExcludeList(self.tsl2Grp,key="excludeList")
		self.filterFromAbove()
		self.finalMoveFunc(self.tsl1)
		self.numRefreshFunc()
		
	def excludeMoveFunc(self,txtScroll):
		txSel = cmds.textScrollList(txtScroll,q=True,si=True) or []
		txExclude = set(cmds.textScrollList(self.tsl2,q=True,ai=True) or [])
		if not txSel:
			return
		for tx in txSel:
			if tx not in txExclude:
				cmds.textScrollList(self.tsl2,e=True,a=tx)
				cmds.textScrollList(txtScroll,e=True,ri=tx)
				txExclude.add(tx)
				txSel.remove(tx)
		self.numRefreshFunc()
		mel.eval('print ("REMINDER : Exclude move <COMPLETE> \\n")')
	 
	def finalMoveFunc(self,txtScroll):
		txSel = cmds.textScrollList(txtScroll,q=True,si=True) or []
		txExclude =  set(cmds.textScrollList(self.tsl2,q=True,ai=True) or [])
		txFinal = set(cmds.textScrollList(self.tsl3,q=True,ai=True) or [])		
		if not txSel:
			return
		# Filter Exclude Out From List
		txFilter = set()
		for tx in txSel:
			if tx not in txExclude:
				txFilter.add(tx)
		# Input to Final List
		for txF in sorted(txFilter):
			if txF not in txFinal:
				cmds.textScrollList(self.tsl3,e=True,a=txF)
				cmds.textScrollList(txtScroll,e=True,ri=txF)
				txFinal.add(txF)
				txSel.remove(txF)
			else:
				cmds.textScrollList(txtScroll,e=True,ri=txF)
				txSel.remove(txF)
		self.numRefreshFunc()
		mel.eval('print ("REMINDER : Exclude move <COMPLETE> \\n")')
	
	def filterFinalList(self):
		self.numRefreshFunc()   # refresh first
		cmds.textScrollList(self.tsl3, e=True, ra=True)
		fromScene = cmds.textScrollList(self.tsl1, q=True, ai=True) or []
		fromAbove = cmds.textScrollList(self.tsl2, q=True, ai=True) or []
		diff = set(fromScene) - set(fromAbove)
		for item in diff:
			cmds.textScrollList(self.tsl3, e=True, a=item)
		self.numRefreshFunc()
		mel.eval('print ("REMINDER : Final List filter <COMPLETE> \\n")')
        
	def clearTSLList(self,TSL):
		cmds.textScrollList(TSL,e=True,ra=True)
		
	def controlsSetFunc(self):
		ctrlSet = 'Controls_Set'
		if cmds.objExists(ctrlSet):
			cmds.delete(ctrlSet)
		newSet = ControlsSet_Func.createSetFunction()
		finalList = list(cmds.textScrollList(self.tsl3,q=True,ai=True) or [])
		if finalList:
			cmds.sets(finalList,add=newSet)
		cmds.select(finalList)
		mel.eval('print("REMINDER : Controls_Set updated with {} objects\\n")'.format(len(finalList)))
   
if __name__== '__main__' :
  try:
    FilterCompare_UI()
  except:
      pass
