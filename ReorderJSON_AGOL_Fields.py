#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     01/07/2022
# Copyright:   (c) emartin 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import json
orig = "C:\\Users\\emartin\\Desktop\\config.json"
new = "C:\\Users\\emartin\\Desktop\\new_config.json"
sortedFieldList = ["OBJECTID", "Shape", "SiteID", "BasicStructureType", "BarrierClass", "SiteStatus", "Stream", "RoadClass", "Type", "DamName", "Fishway", "CurrentUse", "Structure_Type", "Survey_Date", "Passability", "PassabilitySource", "PassabilityComment", "batUSNetID", "batDSNetID", "batFuncUS", "batFuncDS", "batTotUSDS", "batAbs", "batLenUS", "batUSDnsty", "batCountDS", "dsPassabilityProduct", "DSFalls", "DSFishways", "DSHydro", "usAlewifeAcres", "HUC10_CritSalmHab", "US_SalmHabUnits", "US_SalmParrProd", "HUC10_Habitat_Units", "onDMRSalmonPriority", "cumulativeUSNet", "cumulativeSalmHabUnits", "usNatBar", "Aquifer", "AquiferOrCoarseSed", "CalcModCalc", "MilesUS_HATPlus1m", "MilesUS_HATPlus6ft", "MilesUS_HATcurrent", "onConsLand", "HUC4", "HUC4_Name", "HUC6", "HUC6_Name", "HUC8", "HUC8_Name", "HUC10", "HUC10_Name", "HUC12", "HUC12_Name", "NESZCL", "DA_PercFor", "floodplain_US_Perc_nlcd_2016_cultivatedCrops", "floodplain_DS_Perc_nlcd_2016_cultivatedCrops", "floodplain_Tot_Perc_nlcd_2016_cultivatedCrops", "floodplain_US_Perc_nlcd_2016_pastureHay", "floodplain_DS_Perc_nlcd_2016_pastureHay", "floodplain_Tot_Perc_nlcd_2016_pastureHay", "floodplain_US_Perc_nlcd_2016_developedMedHigh", "floodplain_DS_Perc_nlcd_2016_developedMedHigh", "floodplain_Tot_Perc_nlcd_2016_developedMedHigh", "buff100_US_Perc_nlcd_2016_cultivatedCrops", "buff100_DS_Perc_nlcd_2016_cultivatedCrops", "buff100_Tot_Perc_nlcd_2016_cultivatedCrops", "buff100_US_Perc_nlcd_2016_pastureHay", "buff100_DS_Perc_nlcd_2016_pastureHay", "buff100_Tot_Perc_nlcd_2016_pastureHay", "buff100_US_Perc_nlcd_2016_developedMedHigh", "buff100_DS_Perc_nlcd_2016_developedMedHigh", "buff100_Tot_Perc_nlcd_2016_developedMedHigh", "occ_current", "occ_temp7p40", "occ_temp7p20", "bkt_curr_occ_gt50", "bkt_p20_occ_gt50", "bkt_p40_occ_gt50", "HeritagePondBarrier", "MilesBT_MHVH_USonly", "MilesBT_MHVH", "BT_1_4_MHVH", "BT_1_4_HVH", "BT_1_4_VH", "EBTJV_Patch", "usSmeltSite", "Tidal", "SeaRunBT", "InvasiveBarrier", "InvasiveBarrierConfirmed", "InvasiveBarrierConfNumSpp", "Tier", "Symbology3Class", "Symbology", "OverTopNum", "FloodRisk", "PRIWWH", "PRTWWH", "Aquifer_DS", "Aquifer_US", "AquiferOrCoarseSed_DS", "AquiferOrCoarseSed_US", "batCountUS", "batDis2Mth", "batRel", "Black_Crappie_Barrier"]
def main():

    #AGOL truncates field names at 31 chars, so trim these
    finalSortedFieldList = []
    for field in sortedFieldList:
        finalSortedFieldList.append(field[0:31])

    i = 8 #the first prioritized layer is the 11th in the json file
    with open(orig) as json_file:
        data = json.load(json_file)
        while i <= 129:
            fields = data["operationalLayers"][0]["layers"][i]["popupInfo"]["fieldInfos"]
            print(fields)
            newFields = sorted(fields, key=lambda x:finalSortedFieldList.index(x['fieldName']))
            data["operationalLayers"][0]["layers"][i]["popupInfo"]["fieldInfos"] = newFields
            i+=1


    with open(new, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':


    origText = ''
    replaceText = ""
    main()
