'''
Written By Caleb Mackey
4/17/2013
Calculates Median Statistics
'''
import arcpy, os, sys, traceback
# env settings
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False
def GetMedian(in_list):
    sorted_list = sorted(in_list)
    median = int(round(len(sorted_list) / 2))
    if len(sorted_list)%2==0:
        med_val = float(sorted_list[median-1]
                        + sorted_list[median]) / 2
    else:
        med_val = sorted_list[median]
    return med_val
def GetMedianValues(source_fc, new_table, case_field, value_field):

    ''' Generates a table with Median Values, summarized by case_field. If the
        goal is to get the median for the entire table, use a case field that has
        the same value for all records.
        source_fc - input feature class to compute median statistics for
        new_table - output table
        case_field - similar to dissolve field, computes stats based on unique values in this field
        value_field - field that contains the actual values for statistics; must be numeric
    '''

    # Get unique value list for query
    print ('starting cursor')
    with arcpy.da.SearchCursor(source_fc, [case_field]) as rows:
        un_vals = list(set(r[0] for r in rows))
    lyr = arcpy.MakeFeatureLayer_management(source_fc,'source_layer')
    values = {}
    # Get Median UseValue for each station name
    for st in un_vals:
        query = '"{0}" = \'{1}\''.format(case_field, st)
        arcpy.SelectLayerByAttribute_management(lyr, 'NEW_SELECTION', query)
        use_vals = []
        with arcpy.da.SearchCursor(lyr, [value_field]) as rows:
            for row in rows:
                if row[0] != None:
                    use_vals.append(row[0])
        if len(use_vals) > 0:
            median = GetMedian(use_vals)
            values[st] = [median, len(use_vals)]
    # Create new Summary Statistics table with median
    #
    if arcpy.Exists(new_table):
        arcpy.Delete_management(new_table)
    arcpy.CreateTable_management(os.path.split(new_table)[0],os.path.basename(new_table))
    # Get field names and types
    for field in arcpy.ListFields(source_fc):
        if field.name in [case_field, value_field]:
            ftype = field.type
            name = field.name
            length = field.length
            pres = field.precision
            scale = field.scale
            if name == value_field:
                if new_table.endswith('.dbf'):
                    name = 'MED_' + value_field[:6]
                else:
                    name = 'MED_' + value_field
                value_field2 = name
            arcpy.AddField_management(new_table,name,ftype,pres,scale,length)

    # Add frequency field
    arcpy.AddField_management(new_table,'FREQUENCY','LONG')
    # Insert rows
    with arcpy.da.InsertCursor(new_table, [case_field, value_field2, 'FREQUENCY']) as rows:
        for k,v in sorted(values.items()):
            rows.insertRow((k, v[0], v[1]))

    # report results
    print(('Created %s' %os.path.basename(new_table)))
    arcpy.AddMessage('Created %s' %os.path.basename(new_table))
    # .dbf's are automatically given a 'Field1' field...Clean this up
    try:
        if new_table.endswith('.dbf'):
            arcpy.DeleteField_management(new_table, 'Field1')
    except:
        pass
    print ('Done')
if __name__ == '__main__':
##    # testing
    source_fc = r'K:\PenobscotBlueprint\GIS\PenobscotBlueprintData.gdb\Hydrology\AllBarrierFroudeFinal'
    new_table = r'K:\PenobscotBlueprint\GIS\PenobscotBlueprintData.gdb\AllBarrierFroudeFinalMedian' #gdb test

    case_field = 'temp'
    value_field = 'ForMedian'

    # Script tool params
##    source_fc = arcpy.GetParameterAsText(0)
##    new_table = arcpy.GetParameterAsText(1)
##    case_field = arcpy.GetParameterAsText(2)
##    value_field = arcpy.GetParameterAsText(3)

    GetMedianValues(source_fc, new_table, case_field, value_field)