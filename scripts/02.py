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

def createAndBindCurveToJoint(curveName,jointHandler):
	curveHandler = pm.circle(n = curveName)
	node = pm.pointConstraint(jointHandler,curveHandler,w = 1, offset = (0,0,0))
	pm.delete(node) 
	pm.select(d=True)
	return curveHandler
	
def giveOrientConstrain(Giver, Taker):
    node = pm.orientConstraint(Taker, Giver, weight=1, offset=(0,0,0))
    pm.delete(node)
    pm.select(d=1)

#create 5 locator
JOINT_NUMBER = 5
locatorGroup = []
for loopNum in range(JOINT_NUMBER):
	locatorName = 'LegLocator' + str(loopNum)
	locatorGroup.append (createLocator(locatorName, 0, loopNum * 5, 0))
	pm.makeIdentity(locatorGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)
	pm.select(d=True)
	
legLocatorGroup = pm.group(locatorGroup, n='legLocatorGroup')
legLocatorGroup.zeroTransformPivots()

#should have a UI to let artist use locator around


# create 5 joint and snap them to the locator
jointGroup = []
for loopNum in range(JOINT_NUMBER):
	pm.select(d=True)
	jointName = 'legJoint' + str(loopNum)
	jointGroup.append(createAndBindJointToLoc(jointName,locatorGroup[loopNum]))
	pm.makeIdentity(jointGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)
	
	
#create 5 curves and snap them
curveGroup = []
for loopNum in range(JOINT_NUMBER):
	pm.select(d=True)
	CurveName = 'legCurve' + str(loopNum)
	curveGroup.append(createAndBindCurveToJoint(CurveName,jointGroup[loopNum]))
	pm.makeIdentity(curveGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)

#legCurveGroup = pm.group(curveGroup, n='legCurveGroup')
#legCurveGroup.zeroTransformPivots()

print(jointGroup)
# parent those joints
for loopNum in range(0,JOINT_NUMBER-1):
	pm.parent(jointGroup[loopNum],jointGroup[loopNum+1])
	
#parent those curves
for loopNum in range(0,JOINT_NUMBER-1):
	pm.parent(curveGroup[loopNum][0],curveGroup[loopNum+1][0])
	
#orient the joint
for loopNum in range(0,JOINT_NUMBER):
	pm.select(d=True)
	pm.select(jointGroup[loopNum], r = True)
	pm.joint(zso=1,ch=1,e=1,oj='xyz',secondaryAxisOrient='yup')
	
#orient the toes joint IN A SMART WAY!
toeJointNameX = jointGroup[0] + ".jointOrientX"
toeJointNameY = jointGroup[0] + ".jointOrientY"
toeJointNameZ = jointGroup[0] + ".jointOrientZ"

cmds.setAttr(toeJointNameX,0)
cmds.setAttr(toeJointNameY,0)
cmds.setAttr(toeJointNameZ,0)

# give orient constrain
print jointGroup
print curveGroup

for loopNum in range(0,JOINT_NUMBER):
	pm.orientConstraint(curveGroup[loopNum],jointGroup[loopNum], weight=1, mo = True)