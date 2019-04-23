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
		self.GetVertexColorCheck = cmds.checkBox( label='showVertexColor', align='center',v = True,cc = self.swapMaterial);
		self.HighLightSelection = cmds.checkBox( label='HighLightSelection', align='center',v = True,cc = self.ToggleHightlight);
		self.PaintButton = cmds.button(l = 'StartPaint', c = self.assignVertexColor);
		
	def swapMaterial(self,*_):
		self.isDisplayVertexColor = not self.isDisplayVertexColor;
		if(self.isDisplayVertexColor):
			cmds.sets( e = True, forceElement = "initialShadingGroup");
		else:
			cmds.sets( e = True, forceElement = "ShaderfxShader1SG");
			
		print(self.isDisplayVertexColor);
	
	def ToggleHightlight(self,*_):
		self.isHightLight = not self.isHightLight
		print(self.isHightLight)
		
	def assignVertexColor(self,*_):
		cmds.PolygonApplyColor();
		cmds.polyColorPerVertex(rgb = (0.8,0.2,0.0));
		#cmds.artAttrColorPerVertexToolScript(4);
		#cmds.toolPropertyShow;
		mel.eval('PaintVertexColorTool;')
		print('color changed');
		
testWindow = myWindowClass();
testWindow._init_('FlowmapTool');
testWindow.create();
testWindow.AddLayout();