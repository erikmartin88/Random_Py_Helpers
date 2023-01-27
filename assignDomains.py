#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     30/06/2022
# Copyright:   (c) emartin 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os

##mxd = arcpy.mapping.MapDocument(r"CURRENT")
##df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
##layers = arcpy.mapping.ListLayers(mxd)

arcpy.env.workspace = r"K:\NRCS_CIG\GIS\WebMap\Aquatic_Prioritization\Aquatic_Prioritization.gdb\mapService"
layers = arcpy.ListFeatureClasses()
yesNoFields = ("usNatBar", "BT_1_4_MHVH", "BT_1_4_HVH", "BT_1_4_VH", "HeritagePondBarrier", "EBTJV_Patch", "usSmeltSite", "SeaRunBT", "Aquifer", "AquiferOrCoarseSed", "CalcModCalc", "bkt_curr_occ_gt50", "bkt_p20_occ_gt50", "bkt_p40_occ_gt50", "HUC10_CritSalmHab", "onConsLand", "InvasiveBarrier", "InvasiveBarrierConfirmed", "Tidal")

def main():
    errors = []
    for layer in layers:
        if "Prioritized" in layer:
            print(layer)
            count = arcpy.GetCount_management(layer)
            print(count[0])
            if int(count[0]) >0:
                fields = arcpy.ListFields(layer)
                for field in fields:
                    if field.name in yesNoFields:
                        print("...{}".format(field.name))
                        try:
                            arcpy.AssignDomainToField_management(in_table=layer, field_name=field.name, domain_name="YesNo", subtype_code="")
                        except:
                            errors.append("{} / {}".format(layer, field.name))
    print("Errors: {}".format(errors))

if __name__ == '__main__':
    main()
