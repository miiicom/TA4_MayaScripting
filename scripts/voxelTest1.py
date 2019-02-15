import maya.cmds as cmds
import math, random

class myWindowClass:
	kind = 'UIWindow';
	windowName = 'defaultWindow';
	title = 'defaultTitle';
	size = (512,512);
	
	def _init_(self,name):
		self.windowName = 'myUIWindow';
		self.title = name;
		self.size = (512,512);
		print('initiated')
		
	def create(self):
		if cmds.window(self.windowName, exists = True):
			cmds.deleteUI(self.windowName,window = True)
		self.windowName = cmds.window(self.windowName,title = self.title,widthHeight = self.size);
		cmds.showWindow();

	def getMeshVertices(self,mesh):
		vertexGrp = [];
		print(cmds.polyEvaluate(mesh, v = True));
		for x in range(cmds.polyEvaluate(mesh, v = True)):
			vertexGrp.append([mesh+".vtx[%s]"%x])
		return(vertexGrp);
	
	def getMeshFaces(self,mesh):

		FaceGrp = [];
		print(cmds.polyEvaluate(mesh, f = True));
		for x in range(cmds.polyEvaluate(mesh, f = True)):
			FaceGrp.append([mesh+".f[%s]"%x])
		return(FaceGrp);
	
	def getMeshEdges(self,mesh):	

		EdgeGrp = [];
		print(cmds.polyEvaluate(mesh, e = True));
		for x in range(cmds.polyEvaluate(mesh, e = True)):
			EdgeGrp.append([mesh+".e[%s]"%x])
		return(EdgeGrp);
		
testWindow = myWindowClass();
testWindow._init_('Material It Now!');
testWindow.create();
	
selected = cmds.ls(sl=True)[0];
print(testWindow.getMeshEdges(selected));