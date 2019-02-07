import pymel.core as pm
import maya.cmds as cmds
from functools import partial
from random import shuffle
import random


class myWindowClass:
	kind = 'UIWindow';
	windowName = 'defaultWindow';
	title = 'defaultTitle';
	size = (512,512);
	shaderList = [];
	shaderGroup = [];
	buttonList = [];
	colorList =[];
	# Always Generate Saturated Random Colors with the risk of heavy recursion
	def CreateSaturatedColor(self):
		RGB = [];
		
		RGB.append(int(random.random()*5)/5.0);
		RGB.append(int(random.random()*5)/5.0);
		RGB.append(int(random.random()*5)/5.0);
		
		RGB.sort();
		RGB[0] = 0.0;
		RGB[2] = 1.0;
		
		shuffle(RGB);
		if RGB in self.colorList:
			return self.CreateSaturatedColor()
		else:
			print(RGB);
			return RGB;
	def CleanUp(self,*args):
		for buttonpiece in self.buttonList:
			cmds.deleteUI(buttonpiece);
			self.buttonList = [];
		for colorpiece in self.colorList:
			##self.colorList.remove(colorpiece);
			self.colorList = [];
		for shaderpiece in self.shaderList:
			cmds.delete(shaderpiece);
			self.shaderList = [];
		for shaderGPpiece in self.shaderGroup:
			cmds.delete(shaderGPpiece);
			self.shaderGroup = [];
	
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
		tempFrameLayout = cmds.frameLayout( label='MaterialButtons', p = self.windowName);
		self.buttonUniformSize = (self.size[0] / 4,self.size[1] / 4);
		self.buttonLayout = cmds.gridLayout (ag = True, cellWidthHeight = self.buttonUniformSize, nc = 4,p = tempFrameLayout);
		self.ControlButton = cmds.button(label = 'Add color',width = self.buttonUniformSize[0], height  = self.buttonUniformSize[1],command = self.simpleMaterialCreate, p = self.buttonLayout);
		#tempButton = cmds.button(label = 'Material 1',bgc = [1.0,0.0,0.0]);
		#cmds.button(tempButton, e = True, command = partial(self.ClickAndAssign, tempButton));
		#self.buttonList.append(tempButton);
	#For each add color click, it creates corresponding shaders and add a button with dynamic callback
	def simpleMaterialCreate(self,*args):
		print('created a button and corresponding shaders');
		#create a random color set
		tempColor = self.CreateSaturatedColor();
		self.colorList.append(tempColor);
		self.shaderList.append(cmds.shadingNode('lambert', asShader=True));
		cmds.setAttr(self.shaderList[len(self.shaderList)-1]+'.color',tempColor[0],tempColor[1],tempColor[2]);
		self.shaderGroup.append(cmds.sets(renderable = True, noSurfaceShader = True,empty = True,name = 'LambertSG')); #SG for sahder group
		cmds.connectAttr(self.shaderList[len(self.shaderList)-1]+'.outColor',self.shaderGroup[len(self.shaderGroup)-1]+'.surfaceShader');
		tempButton = cmds.button(label = 'Material ' + str(len(self.buttonList)+1),bgc = tempColor,p = self.buttonLayout);
		#cmds.setAttr(tempButton + '.command',partial(self.ClickAndAssign, tempButton));
		cmds.button(tempButton, e = True, command = partial(self.ClickAndAssign, tempButton));
		self.buttonList.append(tempButton);
	
	def ClickAndAssign(self,myButton,*args):
		print('the button is' + myButton + '\n');
		print('it is slot ' + str(self.buttonList.index(myButton)));
		print(self.shaderGroup[self.buttonList.index(myButton)])
		cmds.sets( e = True, forceElement =  self.shaderGroup[self.buttonList.index(myButton)]);

	def AddBakeButton(self):
		tempFrameLayout = cmds.frameLayout( label='BakeButton', p = self.windowName ,cll = True)
		self.BakeLayout = cmds.gridLayout(ag = True, cellWidthHeight = (self.size[0],self.size[0]/10), nc = 1,p = tempFrameLayout);
		cmds.button(label = 'BakeIDMap',p = self.BakeLayout);
		cmds.button(label = 'Clear',p = self.BakeLayout, command = self.CleanUp);
		

		
testWindow = myWindowClass();
testWindow._init_('Material It Now!');
testWindow.create();
testWindow.AddBakeButton();
testWindow.AddButtons();


