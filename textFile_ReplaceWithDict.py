import sys, codecs

inFile = r'C:\Users\emartin\Desktop\JSONEditing\dams.txt'
iterations = [0, 1, 2, 3, 4, 5, 6]

def main():
    # attributeAliasReplace()
    iterationReplace()

def iterationReplace():
    try:
        oldIteration = 2
        newIteration = 1
        sText = "s{}".format(oldIteration)
        prText = "PR{}".format(oldIteration)
        tierText = "Tier{}".format(oldIteration)

        newSText = "s{}".format(newIteration)
        newPRText = "PR{}".format(newIteration)
        newTierText = "Tier{}".format(newIteration)
        with codecs.open(inFile, 'r', 'utf-8-sig') as file:
            data = file.read()
            data = data.replace(sText, newSText)
            data = data.replace(prText, newPRText)
            data = data.replace(tierText, newTierText)

        with codecs.open(inFile, 'w', 'utf-8-sig') as file:
            file.write(data)
        print("Text replaced")

    except Exception as e:
        tb = sys.exc_info()[2]
        print("There was a problem editing text on line {} ".format(tb.tb_lineno))
        print(str(e))

def attributeAliasReplace():
    try:

        with codecs.open(inFile, 'r',  'utf-8-sig') as file:
            data = file.read()
            for search_text in replace_dict:
                # print(search_text)
                for iteration in iterations:
                    sText = '"label": "s{}{}",'.format(iteration, search_text)
                    prText = '"label": "PR{}{}",'.format(iteration, search_text)
                    newSText = '"label": "{}",'.format(replace_dict[search_text])
                    newPRText ='"label": "{} (% Rank)",'.format(replace_dict[search_text])
                    # print("{} replaced with {}".format(sText, newSText))
                    # print("{} replaced with {}".format(prText, newPRText))
                    data = data.replace(sText, newSText)
                    data = data.replace(prText, newPRText)

        with codecs.open(inFile, 'w',  'utf-8-sig') as file:
            file.write(data)


        print("Text replaced")



    except Exception as e:
        tb = sys.exc_info()[2]
        print("There was a problem editing text on line {} ".format(tb.tb_lineno))
        print(str(e))


if __name__ == '__main__':

    replace_dict = {
        "batFuncUS" : "Upstream functional network length",
        "batCountDS" : "Count of downstream barriers",
        "DSFalls" : "Count of natural barriers downstream",
        "DSHydro" : "Count of dams with hydropower facilities downstream",
        "dsPassabilityProduct" : "Product of all downstream barrier passability scores",
        "batAbs" : "​Absolute Gain (min of US and DS Func Networks)",
        "batTotUSDS" : "Total Functional Network (sum of US and DS Func Networks)",
        "batLenUS" : "Total upstream river length (ignoring all barriers)",
        "DA_PercFor" : "​% Forest cover in the total contributing watershed",
        "DA_PercNat" : "% Natural cover in the total contributing watershed",
        "DA_PercAg" : "% Agricultural cover in the total contributing watershed",
        "DA_PercImp" : "​% Impervious Surface in the total contributing watershed",
        "usForARA" : "% Forest cover in ARA of upstream functional network",
        "dsForARA" : "% Forest cover in ARA of downstream functional network",
        "usNatARA" : "% Natural cover in ARA of upstream functional network",
        "dsNatARA" : "% Natural cover in ARA of downstream functional network",
        "usAgARA" : "​% Agricultural cover in ARA of upstream functional network",
        "dsAgARA" : "% Agricultural cover in ARA of downstream functional network",
        "usImpARA" : "% Impervious Surface in ARA of upstream functional network",
        "dsImpARA" : "% Impervious Surface in ARA of downstream functional network",
        "onConsLand" : "Barrier is located on conservation land",
        "CumDistInd" : "NFHAP Cumulative Disturbance Index (by NHD Catchment)",
        "CumDistTXT" :"NFHAP Cumulative Disturbance Index (by NHD Catchment)",
        "QDSANAD" : "Presence of 1 or More Anadromous Species downstream of barrier",
        "QDSNUMANAD" : "# of anadromous species downstream of the barrier",
        "fishRich" : "# of Resident fish species in HUC8",
        "g123Fish" : "# of  rare (G1, G2, G3) fish species in HUC8",
        "CL_2016_effect16" : "Critical Linkages",
        "g123Mussel" : "# of  rare (G1, G2, G3) mussel species in HUC8",
        "g123Cray" : "# of  rare (G1, G2, G3) crayfish species in HUC8",
        "in_EBTJV_2012" : "​Barrier is within EBTJV Catchment with Trout",
        "in_deWeberTrout" : "Barrier is within a modeled catchment for Trout (DeWeber & Wagner)",
        "block_EBTJV_2012" : "Barrier blocks EBTJV 2012 trout catchments",
        "block_BT_DeWeber" : "Barrier blocks modeled trout catchments (DeWeber & Wagner)",
        "NESZCL_Int" : "Stream size class (raise headwaters in importance)",
        "TotNumSzCl" : "# of Size Classes in Total (US + DS) functional network",
        "usNumSzCl" : "# of Upstream Network size classes",
        "usSzClGn" : "Upstream Size Class Gain",
        "totMiCold" : "Miles of Cold water habitat in Total (US + DS) functional network",
        "totMiCC" : "Miles of Cold or Cool water habitat in Total (US + DS) functional network"
    }
    main()