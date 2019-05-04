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


def createLocators():
	
	for loopNum in range(JOINT_NUMBER):
		locatorName = 'LegLocator' + str(loopNum)
		locatorGroup.append (createLocator(locatorName, 0, loopNum * 5, 0))
		pm.makeIdentity(locatorGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)
		pm.select(d=True)
	
	legLocatorGroup = pm.group(locatorGroup, n='legLocatorGroup')
	legLocatorGroup.zeroTransformPivots()
	
#should have a UI to let artist use locator around

def rigit():
# create 5 joint and snap them to the locator

	FKLayer = pm.createDisplayLayer(e = True,n = "FKLayer",nr = True);
	pm.setAttr(FKLayer + ".color", True)
	pm.setAttr(FKLayer + ".overrideRGBColors", True)
	pm.setAttr(FKLayer + ".overrideColorRGB", [1,0,0])
	for loopNum in range(JOINT_NUMBER):
		pm.select(d=True)
		jointName = 'FK_leg' + str(loopNum) + '_jnt'
		FKjointGroup.append(createAndBindJointToLoc(jointName,locatorGroup[loopNum]))	
		pm.makeIdentity(FKjointGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)
		pm.editDisplayLayerMembers(FKLayer,FKjointGroup[loopNum])
	
#create 5 joint for the actual binded joint and snap them to the locator

	BindLayer = pm.createDisplayLayer(e = True,n = "BindLayer",nr = True);
	pm.setAttr(BindLayer + ".color", True)
	pm.setAttr(BindLayer + ".overrideRGBColors", True)
	pm.setAttr(BindLayer + ".overrideColorRGB", [0,1,0])
	for loopNum in range(JOINT_NUMBER):
		pm.select(d=True)
		jointName = 'leg' + str(loopNum) + '_jnt'
		BindjointGroup.append(createAndBindJointToLoc(jointName,locatorGroup[loopNum]))
		pm.makeIdentity(BindjointGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)
		pm.editDisplayLayerMembers(BindLayer,BindjointGroup[loopNum])
	
	#create 5 joint for the IK and snap them to the locator
	
	IKLayer = pm.createDisplayLayer(e = True,n = "IKLayer",nr = True);
	pm.setAttr(IKLayer + ".color", True)
	pm.setAttr(IKLayer + ".overrideRGBColors", True)
	pm.setAttr(IKLayer + ".overrideColorRGB", [0,0,1])
	for loopNum in range(JOINT_NUMBER):
		pm.select(d=True)
		jointName = 'IK_leg' + str(loopNum) + '_jnt'
		IKjointGroup.append(createAndBindJointToLoc(jointName,locatorGroup[loopNum]))
		pm.makeIdentity(IKjointGroup[loopNum],apply=True,t=1,r=1,s=1,n=0,pn=1)
		pm.editDisplayLayerMembers(IKLayer,IKjointGroup[loopNum])
		
		
	#create 5 curves and snap them for FK
	
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
		pm.editDisplayLayerMembers(FKLayer,FKcurveGroup[loopNum][0])
		
	#Create 1 curve for FK, sanp it and group it
	
	pm.select(d=True)
	CurveName = 'IK_leg_ctl'
	IKCurveGroup.append(createAndBindCurveToJoint(CurveName,IKjointGroup[2]));
	pm.setAttr(IKCurveGroup[0][0] + '.scaleX', 2)
	pm.setAttr(IKCurveGroup[0][0] + '.scaleY', 2)
	pm.setAttr(IKCurveGroup[0][0] + '.scaleZ', 2)
	pm.setAttr(IKCurveGroup[0][0] + '.rotateX', 90)
	pm.makeIdentity(IKCurveGroup[0],apply=True,t=1,r=1,s=1,n=0,pn=1)
	pm.editDisplayLayerMembers(IKLayer,IKCurveGroup[0][0])
	
	
	grpName = 'IK_leg_grp'
	grpHandler = createGroup(grpName)
	pm.setAttr(grpHandler + '.translate',[0,0,0])
	IKgrpGroup.append(grpHandler)
	node = pm.pointConstraint(IKCurveGroup[0][0],IKgrpGroup[0],w = 1, offset = (0,0,0),mo = False)
	pm.delete(node) 
	pm.select(d=True)
	pm.makeIdentity(IKgrpGroup[0],apply=True,t=1,r=1,s=1,n=0,pn=1)
	pm.parent(IKCurveGroup[0][0],IKgrpGroup[0])
	
	#create 5 group nodes for FK
	
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
		
	for loopNum in range(0,JOINT_NUMBER-1):
		pm.parent(BindjointGroup[loopNum],BindjointGroup[loopNum+1])
		
	for loopNum in range(0,JOINT_NUMBER-1):
		pm.parent(IKjointGroup[loopNum],IKjointGroup[loopNum+1])
		
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
		
	# give POINT constrain
	IKHandler = pm.ikHandle( sj=IKjointGroup[4], ee=IKjointGroup[2], p=1, w=1 )
	
	pm.pointConstraint(IKCurveGroup[0][0],IKHandler[0],w = 1, offset = (0,0,0))
	#pm.parent(IKHandler[0],IKCurveGroup[0][0])
	
	ControlCurve = pm.circle(n = 'ControlCurver')
	pm.select(ControlCurve)
	pm.setAttr(ControlCurve[0] + '.translate',[10,10,0])
	pm.addAttr(longName='IKFKswitchIK', defaultValue=0.0, minValue=0.0, maxValue=10.0 )
	pm.setAttr(ControlCurve[0] + '.IKFKswitchIK',e = True, keyable = True)
	pm.addAttr(longName='IKFKswitchFK', defaultValue=0.0, minValue=0.0, maxValue=10.0 )
	pm.setAttr(ControlCurve[0] + '.IKFKswitchFK',e = True, keyable = True)
	
	#give skin joint chanin point constrain from IKCurveGroup
	for loopNum in range(0,JOINT_NUMBER):
		FKPointConstrainGroup.append(pm.pointConstraint(FKjointGroup[loopNum],BindjointGroup[loopNum],w = 0, offset = (0,0,0)))
		
	#give skin joint chanin point constrain from IKCurveGroup
	for loopNum in range(0,JOINT_NUMBER):
		IKPointConstrainGroup.append(pm.pointConstraint(IKjointGroup[loopNum],BindjointGroup[loopNum],w = 0, offset = (0,0,0)))
	
	#reference
	#for loopNUM in range(0,JOINT_NUMBER):
	#	pm.setAttr(FKPointConstrainGroup[loopNUM] + '.FK_leg'+str(loopNUM)+'_jntW0',10)
	#Actually I only need one PointConstrainGroup, IK constrain group and Fk constrain group are the same
	for loopNum in range(0,JOINT_NUMBER):
		pm.connectAttr(ControlCurve[0] + '.IKFKswitchFK', FKPointConstrainGroup[loopNum] + '.FK_leg'+str(loopNum)+'_jntW0'?
		pm.connectAttr( ControlCurve[0] +'.IKFKswitchIK', FKPointConstrainGroup[loopNum] + '.IK_leg'+str(loopNum)+'_jntW1')
	pm.expression( s= "ControlCurver.IKFKswitchFK = 1-ControlCurver.IKFKswitchIK",  ae=1, uc="all" )
	pm.setAttr(ControlCurve[0] + '.IKFKswitchFK', keyable = False,cb=False)
	print(ControlCurve)

JOINT_NUMBER = 5
locatorGroup = []
FKjointGroup = []
BindjointGroup = []
IKjointGroup = []
FKcurveGroup = []
IKCurveGroup = []
IKgrpGroup = []
FKgrpGroup = []
FKPointConstrainGroup = []
IKPointConstrainGroup = []
if(pm.window('mainWin', q=True, ex=True)):
    pm.deleteUI('mainWin')
pm.window('mainWin', t='IK FK rig')
pm.columnLayout('mainLayout', adj=True)
pm.text(l=' Click place locators first ', w=50, p = 'mainLayout')
pm.text(l=' Move your locators to form the joint shape ', w=50, p = 'mainLayout')
pm.text(l=' Once your are satisfied with the placement ', w=50, p = 'mainLayout')
pm.text(l=' Click rig it it will let you rig the leg automatically ', w=50, p = 'mainLayout')
pm.button( l = 'place locators',c='createLocators()',p = 'mainLayout')
pm.button( l = 'rig',c='rigit()',p = 'mainLayout')
pm.window('mainWin', e=1, w=400, h=100)
pm.showWindow()
	