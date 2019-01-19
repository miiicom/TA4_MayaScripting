print(jointGroup)
# parent those joints
for loopNum in range(0,JOINT_NUMBER-1):
	pm.parent(jointGroup[loopNum],jointGroup[loopNum+1])
	
#parent those curves
#for loopNum in range(0,JOINT_NUMBER-1):
#	pm.parent(curveGroup[loopNum][0],curveGroup[loopNum+1][0])

#parent group and curves
#for loopNum in range(0,JOINT_NUMBER-1):
#	pm.parent(grpGroup[loopNum],curveGroup[loopNum][0])
#	pm.parent(curveGroup[loopNum][0],grpGroup[loopNum+1])
	
#parent group and curves
for loopNum in range(0,JOINT_NUMBER-1):
	pm.parent(curveGroup[JOINT_NUMBER - 1 - loopNum][0],grpGroup[JOINT_NUMBER - 1 - loopNum])
	pm.parent(grpGroup[JOINT_NUMBER- loopNum-2],curveGroup[JOINT_NUMBER - 1 - loopNum][0])

pm.parent(curveGroup[0][0],grpGroup[0])

	
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