######################################################################
##	Script to sum values in a field if they = 1.
##
##	Erik Martin, emartin@tnc.org
##	June 20, 2012
##
##
######################################################################

import arcpy
fc=arcpy.GetParameterAsText(0)
#fc =r"C:\Users\emartin\Desktop\test.gdb\test"
#fieldNameList =["DSALEWIFE", "DSBLUEBACK", "DSAMSHAD", "DSHICKSHAD", "DSSHRTSTUR", "DSATLSTUR", "DSSTRBASS", "DSAMEEL"]
fieldNameList = [arcpy.GetParameterAsText(1), arcpy.GetParameterAsText(2), arcpy.GetParameterAsText(3), arcpy.GetParameterAsText(4), arcpy.GetParameterAsText(5), arcpy.GetParameterAsText(6), arcpy.GetParameterAsText(7), arcpy.GetParameterAsText(8)]
writeField = arcpy.GetParameterAsText(9)
arcpy.AddMessage(fieldNameList)
rows=arcpy.UpdateCursor(fc)

for row in rows:
	ValueList=[]
	for field in fieldNameList:
		FieldVal = int(row.getValue(field))
		if FieldVal == 1:
			ValueList.append(FieldVal)
	rowSum = sum(ValueList)
	row.setValue(writeField, int(rowSum))
	rows.updateRow(row)
	del ValueList
del row
del rows
del fieldNameList

arcpy.SetParameterAsText(10, True)