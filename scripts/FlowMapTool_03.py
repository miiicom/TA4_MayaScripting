import maya.cmds as cmds
import math, random

class myWindowClass:
	kind = 'UIWindow';
	windowName = 'defaultWindow';
	title = 'defaultTitle';
	size = (256,256);
	
	def _init_(self,name):
		self.windowName = 'FlowmapTool';
		self.title = name;
		self.size = (256,256);
		self.isDisplayVertexColor = True;
		self.isHightLight = True;
		self.bakeTextureWidth = 256;
		self.bakeTextureHeight = 256;
		print('initiated');
		
	def create(self):
		if cmds.window(self.windowName, exists = True):
			cmds.deleteUI(self.windowName,window = True)
		self.windowName = cmds.window(self.windowName,title = self.title,widthHeight = self.size);
		cmds.showWindow();
		
	def AddLayout(self):
		tempColumnLayout = cmds.columnLayout( adjustableColumn=True );
		cmds.text( label='test' ,align='center');
		cmds.separator()
		self.GetVertexColorCheck = cmds.checkBox( label='showVertexColor', align='center',v = True,cc = self.swapMaterial,p = tempColumnLayout);
		self.HighLightSelection = cmds.checkBox( label='HighLightSelection', align='center',v = True,cc = self.ToggleHightlight,p = tempColumnLayout);
		self.PaintButton = cmds.button(l = 'StartPaint', c = self.assignVertexColor,p = tempColumnLayout);
		
		tempRowLayout = cmds.rowLayout(numberOfColumns = 2, adjustableColumn=2, columnAlign=(1, 'right'), columnWidth2=(80, 80),p = tempColumnLayout)
		cmds.text(label = "texture width:", p = tempRowLayout)
		self.tbField1 = cmds.textField(p = tempRowLayout?text = 256)
		tempRowLayout2 = cmds.rowLayout(numberOfColumns = 2, adjustableColumn=2, columnAlign=(1, 'right'), columnWidth2=(80, 80),p = tempColumnLayout)
		cmds.text(label = "texture width:", p = tempRowLayout2)
		self.tbField2 = cmds.textField(p = tempRowLayout2, text = 256)
		self.bakeButton = cmds.button(l = 'bakeTexture', c = self.ClickAndBake,p = tempColumnLayout);
		
		
	def swapMaterial(self,*_):
		self.isDisplayVertexColor = not self.isDisplayVertexColor;
		if(self.isDisplayVertexColor):
			cmds.sets( e = True, forceElement = "initialShadingGroup");
		else:
			cmds.sets( e = True, forceElement = "ShaderfxShader1SG");
			
		print(self.isDisplayVertexColor);
	
	def ToggleHightlight(self,*_):
		self.isHightLight = not self.isHightLight
		cmds.modelEditor( 'modelPanel4', e=True, sel=self.isHightLight )
		temp = cmds.textField(self.tbField1, q = True,text=1) #gets value from textfield
		print(temp)
		
	def assignVertexColor(self,*_):
		cmds.PolygonApplyColor();
		cmds.polyColorPerVertex(rgb = (0.8,0.2,0.0));
		#cmds.artAttrColorPerVertexToolScript(4);
		#cmds.toolPropertyShow;
		
		mel.eval('PaintVertexColorTool;')
		print('color changed');
		
	def ClickAndBake(self,*args):
		BakeObject = cmds.ls(sl=True,long=True);
		if(len(BakeObject) != 1):	
			cmds.error("More than 1 object selected for baking, bake failed, please make sure you only select the object you want to bake ID map");
		else:
			tempDuplicateObj = cmds.duplicate(rr = True);
			print('RenderPath is '+ cmds.workspace( q=True, dir=True));
			cmds.surfaceSampler( mapOutput='diffuseRGB', filename=cmds.workspace( q=True, dir=True) + 'IDMap', fileFormat='png', source=BakeObject[0], target= tempDuplicateObj, uv='map1',mapWidth = 256,mapHeight = 256);
			cmds.delete(tempDuplicateObj);
		
testWindow = myWindowClass();
testWindow._init_('FlowmapTool');
testWindow.create();
testWindow.AddLayout();