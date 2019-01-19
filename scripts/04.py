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
	
def createGroup(grpName):
	grpHandler = pm.group(n = grpName)
	return grpHandler
	
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
FKjointGroup = []
for loopNum in range(JOINT_NUMBER):
	pm.select(d=True)
	jointName = 'FK_leg' + str(loopNum) + '_jnt'
	FKjointGroup.append(createAndBindJointToLoc(jointName,locatorGroup[loopNum]))
	pm.makeIdentity(FKjointGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)
	
# create 5 joint for the actualn binded jointand snap them to the locator
#ActualjointGroup = []
#for loopNum in range(JOINT_NUMBER):
#	pm.select(d=True)
#	jointName = 'FK_leg' + str(loopNum) + '_jnt'
#	jointGroup.append(createAndBindJointToLoc(jointName,locatorGroup[loopNum]))
#	pm.makeIdentity(jointGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)
	
	
#create 5 curves and snap them
FKcurveGroup = []
for loopNum in range(JOINT_NUMBER):
	pm.select(d=True)
	CurveName = 'FK_leg' + str(loopNum) + '_ctl'
	FKcurveGroup.append(createAndBindCurveToJoint(CurveName,FKjointGroup[loopNum]))
	pm.makeIdentity(FKcurveGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.translateX', lock = True)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.translateY', lock = True)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.translateZ', lock = True)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.scaleX', lock = True)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.scaleY', lock = True)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.scaleZ', lock = True)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.translateX', keyable=False)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.translateY', keyable=False)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.translateZ', keyable=False)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.scaleX', keyable=False)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.scaleY', keyable=False)
	pm.setAttr(FKcurveGroup[loopNum][0] + '.scaleZ', keyable=False)
#legCurveGroup = pm.group(curveGroup, n='legCurveGroup')
#legCurveGroup.zeroTransformPivots()

#create 5 group nodes
FKgrpGroup = []
for loopNum in range(JOINT_NUMBER):
	pm.select(d=True)
	grpName = 'FK_leg' + str(loopNum) + '_grp'
	grpHandler = createGroup(grpName)
	print(FKcurveGroup[loopNum][0])
	print(grpHandler)
	pm.setAttr(grpHandler + '.translate',[0,0,0])
	FKgrpGroup.append(grpHandler)
	node = pm.pointConstraint(FKcurveGroup[loopNum][0],FKgrpGroup[loopNum],w = 1, offset = (0,0,0),mo = False)
	pm.delete(node) 
	pm.select(d=True)
	pm.makeIdentity(FKgrpGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)

# parent those joints
for loopNum in range(0,JOINT_NUMBER-1):
	pm.parent(FKjointGroup[loopNum],FKjointGroup[loopNum+1])
	
#parent those curves
#for loopNum in range(0,JOINT_NUMBER-1):
#	pm.parent(curveGroup[loopNum][0],curveGroup[loopNum+1][0])

#parent group and curves
#for loopNum in range(0,JOINT_NUMBER-1):
#	pm.parent(grpGroup[loopNum],curveGroup[loopNum][0])
#	pm.parent(curveGroup[loopNum][0],grpGroup[loopNum+1])
	
#parent group and curves
for loopNum in range(0,JOINT_NUMBER-1):
	pm.parent(FKcurveGroup[JOINT_NUMBER - 1 - loopNum][0],FKgrpGroup[JOINT_NUMBER - 1 - loopNum])
	pm.parent(FKgrpGroup[JOINT_NUMBER- loopNum-2],FKcurveGroup[JOINT_NUMBER - 1 - loopNum][0])

pm.parent(FKcurveGroup[0][0],FKgrpGroup[0])

	
#orient the joint
for loopNum in range(0,JOINT_NUMBER):
	pm.select(d=True)
	pm.select(FKjointGroup[loopNum], r = True)
	pm.joint(zso=1,ch=1,e=1,oj='xyz',secondaryAxisOrient='yup')
	
#orient the toes joint IN A SMART WAY!
toeJointNameX = FKjointGroup[0] + ".jointOrientX"
toeJointNameY = FKjointGroup[0] + ".jointOrientY"
toeJointNameZ = FKjointGroup[0] + ".jointOrientZ"

cmds.setAttr(toeJointNameX,0)
cmds.setAttr(toeJointNameY,0)
cmds.setAttr(toeJointNameZ,0)

# give orient constrain

for loopNum in range(0,JOINT_NUMBER):
	pm.orientConstraint(FKcurveGroup[loopNum],FKjointGroup[loopNum], weight=1, mo = True)