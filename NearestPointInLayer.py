######################################################################
## Nearest Point in same FC
## Erik Martin, emartin@tnc.org, The Nature Conservancy, Eastern Division Conservation
## June 2013
##
## Finds the closest point in a feature class and writes the ID of that point
## along with distance and angle to it to a new FC
##
######################################################################

import arcpy


FC = arcpy.GetParameterAsText(0)
outFC = arcpy.GetParameterAsText(1)
uniqueIDField = arcpy.GetParameterAsText(2)
nearDist = arcpy.GetParameterAsText(3)
inclAngle = arcpy.GetParameter(4)
inclXY = arcpy.GetParameter(5)

arcpy.env.overwriteOutput = True


if inclXY == True:
	loc = "LOCATION"
else:
	loc = "NO_LOCATION"

if inclAngle == True:
	angle = "ANGLE"
else:
	angle = "NO_ANGLE"

fields = ("OBJECTID", uniqueIDField)
uniqueIDList = []
fidUniq = {}
with arcpy.da.SearchCursor(FC, fields) as rows:
	for row in rows:
		objectID = row[0]
		uniqID = row[1]
		uniqueIDList.append(uniqID)
		fidUniq.update({objectID:uniqID})
numRecords = len(uniqueIDList)
ptNameList = []
iterate = 1
for uniqueID in uniqueIDList:
	arcpy.AddMessage("Calculating point " + str(iterate) + " of " + str(numRecords))
	exp = '"{}" = \'{}\''.format(uniqueIDField, uniqueID)
	ptName = "{}/inPt{}".format("in_memory", iterate)
	arcpy.Select_analysis(FC, ptName, exp)
	otherPts = '"{}" <> \'{}\''.format(uniqueIDField, uniqueID)
	arcpy.MakeFeatureLayer_management(FC, "otherPts", otherPts)
	arcpy.Near_analysis(ptName, "otherPts", nearDist, loc, angle)
	ptNameList.append(ptName)
	iterate += 1

arcpy.Merge_management(ptNameList, outFC)
arcpy.AddField_management(outFC, "NEAR_UNIQID", "TEXT")

fields = ("NEAR_FID", "NEAR_UNIQID")
with arcpy.da.UpdateCursor(outFC, fields) as rows:
	for row in rows:
		if row[0] > -1:
			nearUniq = fidUniq[row[0]]
			row[1] = nearUniq
		else:
			row[1] = "None Found in Search Distance"
		rows.updateRow(row)

if inclAngle == True:
	arcpy.AddField_management(outFC, "NEAR_AZ_ANG", "DOUBLE")
	fields = ("NEAR_ANGLE", "NEAR_AZ_ANG", "NEAR_FID")
	with arcpy.da.UpdateCursor(outFC, fields) as rows:
		for row in rows:
			if row[2] != None:
				nearAngle = row[0]
				if (nearAngle <= 180) and (nearAngle >90):
					row[1] = (360.0 - (nearAngle - 90))
				else:
					row[1] = abs(nearAngle-90)
			else:
				pass
			rows.updateRow(row)