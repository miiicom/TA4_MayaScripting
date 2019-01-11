import maya.cmds as cmds
import pymel.core as pm
def createLocator(name, x,y,z):
	locator = pm.spaceLocator(n = name)
	locator.t.set(x,y,z)
	return locator
	
def createAndBindJointToLoc(jointName, LocHandler):
	jointHandler = pm.joint(n = jointName)
	node = pm.pointConstraint(LocHandler,jointHandler,w = 1, offset = (0,0,0))
	pm.delete(node) 
	pm.select(d=True)
	return jointHandler

#create 5 locator
locatorGroup = []
for loopNum in range(5):
	locatorName = 'LegLocator' + str(loopNum)
	locatorGroup.append (createLocator(locatorName, 0, loopNum * 5, 0))

legLocatorGroup = pm.group(locatorGroup, n='legLocatorGroup')


for loopNum in range(5):
	jointName = 'legJoint' + str(loopNum)
	createAndBindJointToLoc?jointName,locatorGroup[loopNum])

