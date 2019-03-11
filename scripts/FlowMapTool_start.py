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
		print('initiated');
		
	def create(self):
		if cmds.window(self.windowName, exists = True):
			cmds.deleteUI(self.windowName,window = True)
		self.windowName = cmds.window(self.windowName,title = self.title,widthHeight = self.size);
		cmds.showWindow();
		
testWindow = myWindowClass();
testWindow._init_('FlowmapTool');
testWindow.create();
#testWindow.AddLayout();