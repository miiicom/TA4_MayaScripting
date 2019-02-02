import pymel.core as pm
import maya.cmds as cmds

class myWindowClass:
	kind = 'UIWindow';
	windowName = 'defaultWindow';
	title = 'defaultTitle';
	size = (512,512);
	shaderList = [];
	shaderGroup = [];
	
	def _init_(self,name):
		self.windowName = 'myUIWindow';
		self.title = name;
		self.size = (512,512);
		self.shaderList = [];
		self.shaderGroup = [];
		print('initiated')
	def create(self):
		if cmds.window(self.windowName, exists = True):
			cmds.deleteUI(self.windowName,window = True)
		self.windowName = cmds.window(self.windowName,title = self.title,widthHeight = self.size);
		cmds.showWindow();
		
	def AddButtons(self):
		self.buttonUniformSize = (self.size[0] / 4,self.size[1] / 4);
		self.buttonLayout = cmds.gridLayout (ag = True, cellWidthHeight = self.buttonUniformSize, nc = 4);
		self.ControlButton = cmds.button(label = 'Add color',width = self.buttonUniformSize[0], height  = self.buttonUniformSize[1],command = self.simpleMaterialCreate);
		self.ControlButton = cmds.button(label = 'Mat1',bgc = [1.0,0.0,0.0]);

	
	def simpleMaterialCreate(self,*args):
		print('test');
		self.shaderList.append(cmds.shadingNode('lambert', asShader=True));
		cmds.setAttr(self.shaderList[len(self.shaderList)-1]+'.color',1.0,0.0,0.0);
		self.shaderGroup.append(cmds.sets(renderable = True, noSurfaceShader = True,empty = True,name = 'LambertSG')); #SG for sahder group
		cmds.connectAttr(self.shaderList[len(self.shaderList)-1]+'.outColor',self.shaderGroup[len(self.shaderGroup)-1]+'.surfaceShader');
		
testWindow = myWindowClass();
testWindow._init_('QuciMatAssignTool')
testWindow.create()
testWindow.AddButtons()