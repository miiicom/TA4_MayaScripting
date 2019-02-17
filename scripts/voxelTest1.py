import maya.cmds as cmds
import math, random

class myWindowClass:
	kind = 'UIWindow';
	windowName = 'defaultWindow';
	title = 'defaultTitle';
	size = (256,256);
	
	sampleRate = 1; #Default to 1
	RemeshLength = 5;
	
	def _init_(self,name):
		self.windowName = 'myUIWindow';
		self.title = name;
		self.size = (256,256);
		print('initiated')
		
	def create(self):
		self.VoxelMeshGroup = cmds.group( em=True, name='VoxelMeshs');
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
		
	def calculateDistanceBetweenVerts(self,v1, v2):
		Location1 = cmds.xform(v1, q=True, t=True);
		Location2 = cmds.xform(v2, q=True, t=True);
    	
		return math.sqrt((Location2[0]-Location1[0])**2 + (Location2[1]-Location1[1])**2 + (Location2[2]-Location1[2])**2);
    	
	def calculateAvgEdgeLRN(self,mesh):
		
		edgeGrp = self.getMeshEdges(mesh);
		average = 0;
		count = 1;
		
		for x in range(int(len(edgeGrp) * self.sampleRate)):
			sampleEdge = random.choice(edgeGrp);
			edgeGrp.remove(sampleEdge);
			cmds.select(sampleEdge);
			cmds.ConvertSelectionToVertices();
			sampleVerts = cmds.ls(sl=True, fl=True);
			distance = self.calculateDistanceBetweenVerts(sampleVerts[0],sampleVerts[1]);
			average = ((count-1)*average + distance)/count
			count += 1;
		return average;
		
	def DoRemesh(self,mesh):
		cmds.select(mesh);
		cmds.polyRemesh(tsb = True,rft = self.RemeshLength);
		
	def CalculateAndVoxelize(self,mesh):
		if not (cmds.objExists('VoxelMeshs')):
			self.VoxelMeshGroup = cmds.group( em=True, name='VoxelMeshs');
		selected = cmds.ls(sl=True)[0];
		AveLen = self.calculateAvgEdgeLRN(selected);
		self.DoRemesh(selected);
		self.voxelize(selected,AveLen);
		
	def TypeFunction(self,*_):
		value = cmds.floatSliderGrp(self.RemeshLengthSlder,q=True, v=True)
		print('Type value is' + str(value));
		self.RemeshLength = value;
		
	def DragFunction(self,*_): 
		value = cmds.floatSliderGrp(self.RemeshLengthSlder,q=True, v=True)
		print('Drag value is' + str(value));
		self.RemeshLength = value;
	
	def AddLayout(self):
		self.tempFrameLayout = cmds.frameLayout( label='Sliders', p = self.windowName);
		self.RemeshLengthSlder = cmds.floatSliderGrp(l= 'RemeshEdgeLength',field = True, min=1, max=10, value=5, step=0.1 ,p = self.tempFrameLayout, dc = self.DragFunction, cc = self.TypeFunction);
		self.VoxelizeButton = cmds.button(l = 'Voxelize',p = self.tempFrameLayout, c = self.CalculateAndVoxelize);
		
	def voxelize(self,mesh,avgLength):
		voxel = [];
		voxelMap = {};
		vertexGrp = self.getMeshVertices(mesh);
		vertexNum = len(vertexGrp);
		i = 0
		mesh
		
		for x in vertexGrp:
			cmds.select(x);
			color = cmds.polyColorPerVertex(q = True,rgb = True);
			location = cmds.xform(x, q=True, t=True);
			location = [int(location[0]), int(location[1]), int(location[2])]; #round to int
			print(location)
			key = str(location[0])+","+str(location[1])+","+str(location[2]); #store voxelized position
			if not key in voxelMap:
				temp = cmds.polyCube();
				cmds.scale(1.5*avgLength,1.5*avgLength,1.5*avgLength,temp);
				cmds.polyColorPerVertex(temp, rgb = color);
				cmds.parent( temp, self.VoxelMeshGroup );
				cmds.setAttr(temp[0]+'.displayColors',  1);
				cmds.xform(temp[0], t=location);
				voxel += [temp]
				voxelMap[key] = True
				i += 1
		
testWindow = myWindowClass();
testWindow._init_('Voxelizer');
testWindow.create();
testWindow.AddLayout();

#selected = cmds.ls(sl=True)[0];
#print(cmds.objectType(selected,))
#testWindow.DoRemesh(selected);
#avgLength = testWindow.calculateAvgEdgeLRN(selected);
#print(avgLength);
#testWindow.voxelize(selected,avgLength);