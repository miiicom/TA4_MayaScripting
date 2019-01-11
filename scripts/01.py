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
JOINT_NUMBER = 5
locatorGroup = []
for loopNum in range(JOINT_NUMBER):
	locatorName = 'LegLocator' + str(loopNum)
	locatorGroup.append (createLocator(locatorName, 0, loopNum * 5, 0))
	pm.select(d=True)

legLocatorGroup = pm.group(locatorGroup, n='legLocatorGroup')
#should have a UI to let artist use locator around

# create 5 joint and snap them to the locator
jointGroup = []
for loopNum in range(JOINT_NUMBER):
	pm.select(d=True)
	jointName = 'legJoint' + str(loopNum)
	jointGroup.append(createAndBindJointToLoc(jointName,locatorGroup[loopNum]))

print(jointGroup)
# parent those joints
for loopNum in range(0,JOINT_NUMBER-1):
	pm.parent(jointGroup[loopNum],jointGroup[loopNum+1])