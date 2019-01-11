#create 5 locators you can move for joints
import maya.cmds as cmds
import pymel.core as pm
locatorGroup = []
pm.group()

for loopNum in range(5):
	locatorGroup.append(pm.spaceLocator(p = [0,loopNum * 5,0]))
	cmds.CenterPivot();

#print locatorGroup;

#Create 5 joints and snap them into locator
jointGroup = []
for  in range(5):
	jointHandler = pm.joint()
	cmds.matchTransform(locatorGroup[loopNum].nodeName(),jointHandler.nodeName())
	pm.select(d=1)	
