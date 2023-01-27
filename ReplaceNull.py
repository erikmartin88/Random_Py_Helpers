######################################################################
##    Script to replace all null values in a table (all fields).  Null
##    in numeric value fields are replaced with 0.  Nulls in text fields
##    are replaced with "".
##
##    Erik Martin, emartin@tnc.org
##    June 20, 2012
##  rev. July 2013 - made into a class
##
######################################################################
import arcpy
import sys
class ReplaceNulls:
    def __init__(self, FC):
        self.fc = FC

    def replace(self):
        try:
            fc = self.fc
            arcpy.AddMessage("Converting NULL values...")
            print("Converting NULL values...")

            smallIntFieldList = arcpy.ListFields(fc,"","SmallInteger")
            for field in smallIntFieldList:
                name = field.name
                arcpy.AddMessage("Replacing nulls in {}".format(name))
                select = "\"{}\" IS NULL".format(name)
                arcpy.MakeFeatureLayer_management(fc, "lyr", select)
                rowCount = int(arcpy.GetCount_management("lyr").getOutput(0))
                if rowCount == 0:
                    pass
                else:
                    with arcpy.da.UpdateCursor("lyr", name) as rows:
                        for row in rows:
                            row[0] = 0
                            rows.updateRow(row)


            intFieldList = arcpy.ListFields(fc,"","Integer")
            for field in intFieldList:
                name = field.name
                arcpy.AddMessage("Replacing nulls in {}".format(name))
                select = "\"{}\" IS NULL".format(name)
                arcpy.MakeFeatureLayer_management(fc, "lyr", select)
                rowCount = int(arcpy.GetCount_management("lyr").getOutput(0))
                if rowCount == 0:
                    pass
                else:
                    with arcpy.da.UpdateCursor("lyr", name) as rows:
                        for row in rows:
                            row[0] = 0
                            rows.updateRow(row)

            singleFieldList = arcpy.ListFields(fc,"","Single")
            for field in singleFieldList:
                name = field.name
                arcpy.AddMessage("Replacing nulls in {}".format(name))
                select = "\"{}\" IS NULL".format(name)
                arcpy.MakeFeatureLayer_management(fc, "lyr", select)
                rowCount = int(arcpy.GetCount_management("lyr").getOutput(0))
                if rowCount == 0:
                    pass
                else:
                    with arcpy.da.UpdateCursor("lyr", name) as rows:
                        for row in rows:
                            row[0] = 0

            doubleFieldList = arcpy.ListFields(fc,"","Double")
            for field in doubleFieldList:
                name = field.name
                arcpy.AddMessage("Replacing nulls in {}".format(name))
                select = "\"{}\" IS NULL".format(name)
                arcpy.MakeFeatureLayer_management(fc, "lyr", select)
                rowCount = int(arcpy.GetCount_management("lyr").getOutput(0))
                if rowCount == 0:
                    pass
                else:
                    with arcpy.da.UpdateCursor("lyr", name) as rows:
                        for row in rows:
                            row[0] = 0
                            rows.updateRow(row)

            stringFieldList = arcpy.ListFields(fc,"","String")
            for field in stringFieldList:

                exp = ""
                name = field.name
                arcpy.AddMessage("Replacing nulls in {}".format(name))
                select = "\"{}\" IS NULL".format(name)
                arcpy.MakeFeatureLayer_management(fc, "lyr", select)
                rowCount = int(arcpy.GetCount_management("lyr").getOutput(0))
                if rowCount == 0:
                    pass
                else:
                    with arcpy.da.UpdateCursor("lyr", name) as rows:
                        for row in rows:
                            row[0] = ""
                            rows.updateRow(row)

            print("Finished converting NULL values...")
            arcpy.AddMessage("Finished converting NULL values...")

        except Exception, e:
            tb = sys.exc_info()[2]
            print ("Problem converting nulls...")
            print "Line {}".format(tb.tb_lineno)
            print e.message

def main():
    layer = ReplaceNulls(arcpy.GetParameterAsText(0))
    layer.replace()

if __name__ == "__main__": main()