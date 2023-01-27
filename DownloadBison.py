#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emartin
#
# Created:     12/09/2013
# Copyright:   (c) emartin 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


def main():
    import arcpy
    import os
    import sys
    import urllib
    import urllib2
    import json
    import re

    saveDir = r"K:\SEACAP\GIS_Data\Biological\BISON"

    #get the current directory and change to the save directory
    curDir = os.getcwd()
    os.chdir (saveDir)
    sppDict = {}
    header = "Name, OccurenceID, LatDD, LongDD, year, collector, resource"

    sppList = set(["Etheostoma%20colorosum","Etheostoma%20whipplei","Etheostoma%20blennioides","Etheostoma%20kanawhae","Etheostoma%20ramseyi","Etheostoma%20serrifer","Etheostoma%20rufilineatum","Etheostoma%20jordani","Etheostoma%20tennesseense","Etheostoma%20jessiae","Etheostoma%20asprigene","Etheostoma%20chlorobranchium","Etheostoma%20whipplei%20artesiae","Etheostoma%20meridianum","Etheostoma%20acuticeps","Etheostoma%20hopkinsi","Etheostoma%20crossopterum","Etheostoma%20proeliare","Etheostoma%20fricksium","Etheostoma%20trisella","Etheostoma%20fusiforme","Etheostoma%20caeruleum","Etheostoma%20parvipinne","Etheostoma%20chlorosomum","Etheostoma%20vitreum","Etheostoma%20lachneri","Etheostoma%20tallapoosae","Etheostoma%20duryi","Etheostoma%20nigripinne","Etheostoma%20brevirostrum","Etheostoma%20flabellare","Etheostoma%20Edwini","Etheostoma%20davisoni","Etheostoma%20histrio","Lepomis%20macrochirus%20x%20Lepomis%20miniatus","Lepomis%20miniatus","Lepomis%20auritus","Lepomis%20marginatus","Lepomis%20cyanellus","Lepomis%20humilis","Lepomis%20punctatus","Lepomis%20megalotis","Lepomis%20gibbosus","Lepomis%20symmetricus", "Lepomis%20macrochirus"])

##    sppList = set(["Ambloplites%20cavifrons", "Ammocrypta%20beanii" , "Ammocrypta%20bifascia", "Ammocrypta%20meridiana", "Ammocrypta%20vivax", "Campostoma%20anomalum", "Campostoma%20oligolepis", "Campostoma%20pauciradii", "Campostoma%20pullum", "Campostoma%20oligolepis", "Campostoma%20pauciradii", "Carassius%20auratus", "Clinostomus%20funduloides", "Crystallaria%20asprella", "Ctenopharyngodon%20idella", "Cyprinella%20analostana", "Cyprinella%20caerulea", "Cyprinella%20callisema", "Cyprinella%20callistia", "Cyprinella%20callitaenia", "Cyprinella%20camura", "Cyprinella%20chloristia", "Cyprinella%20galactura", "Cyprinella%20gibbsi", "Cyprinella%20labrosa", "Cyprinella%20leedsi", "Cyprinella%20lutrensis", "Cyprinella%20nivea", "Cyprinella%20spiloptera", "Cyprinella%20spp.", "Cyprinella%20trichroistia", "Cyprinella%20venusta", "Cyprinella%20whipplei", "Cyprinella%20xaenura", "Cyprinella%20analostana", "Cyprinella%20caerulea", "Cyprinella%20callisema", "Cyprinella%20callistia", "Cyprinella%20callitaenia", "Cyprinella%20camura", "Cyprinella%20cercostigma", "Cyprinella%20chloristia", "Cyprinella%20galactura", "Cyprinella%20gibbsi", "Cyprinella%20hybrid", "Cyprinella%20labrosa", "Cyprinella%20leedsi", "Cyprinella%20nivea", "Cyprinella%20pyrrhomelas", "Cyprinella%20sp.%201", "Cyprinella%20spiloptera", "Cyprinella%20stigmatura", "Cyprinella%20trichroistia", "Cyprinella%20venusta", "Cyprinella%20whipplei", "Cyprinella%20xaenura", "Cyprinella%20zanema", "Cyprinus%20carpio", "Ericymba%20amplamala", "Erimystax%20cahni", "Erimystax%20dissimilis", "Erimystax%20insignis", "Erimyzon%20oblongus", "Erimyzon%20tenuis", "Exoglossum%20laurae", "Exoglossum%20maxillingua", "Gobiomorus%20dormitor", "Gobionellus%20hastatus", "Gobionellus%20spp.", "Gobionellus%20oceanicus", "Gobiosoma%20bosc", "Gobiosoma%20robustum", "Hemitremia%20flammea", "Hybognathus%20hayi", "Hybognathus%20nuchalis", "Hybognathus%20placitus", "Hybognathus%20regius", "Hybognathus%20spp.", "Hybognathus%20hayi", "Hybognathus%20nuchalis", "Hybognathus%20regius", "Hybopsis%20amblops", "Hybopsis%20amnis", "Hybopsis%20lineapunctata", "Hybopsis%20rubrifrons", "Hybopsis%20sp%20cf%20winchelli", "Hybopsis%20spp.", "Hybopsis%20winchelli", "Hybopsis%20zanema", "Hybopsis%20hypsinotus", "Hybopsis%20labrosa", "Hybopsis%20lineapunctata", "Hybopsis%20rubrifrons", "Hybopsis%20sp.%209", "Hybopsis%20winchelli", "Hypentelium%20etowanum", "Hypentelium%20nigricans", "Hypentelium%20roanokense", "Hypophthalmichthys%20molitrix", "Hypophthalmichthys%20nobilis", "Luxilus%20albeolus", "Luxilus%20cerasinus", "Luxilus%20chrysocephalus", "Luxilus%20coccogenis", "Luxilus%20cornutus", "Luxilus%20zonistius", "Luxilus%20albeolus", "Luxilus%20cerasinus", "Luxilus%20chrysocephalus", "Luxilus%20chrysocephalus%20chrysocephalus", "Luxilus%20chrysocephalus%20isolepis", "Luxilus%20coccogenis", "Luxilus%20zonistius", "Lythrurus%20ardens", "Lythrurus%20atrapiculus", "Lythrurus%20bellus", "Lythrurus%20fasciolaris", "Lythrurus%20fumeus", "Lythrurus%20lirus", "Lythrurus%20matutinus", "Lythrurus%20roseipinnis", "Lythrurus%20spp.", "Lythrurus%20umbratilis", "Lythrurus%20alegnotus", "Lythrurus%20ardens", "Lythrurus%20atrapiculus", "Lythrurus%20bellus", "Lythrurus%20fasciolaris", "Lythrurus%20lirus", "Lythrurus%20matutinus", "Lythrurus%20roseipinnis", "Macrhybopsis%20aestivalis", "Macrhybopsis%20meeki", "Macrhybopsis%20spp.", "Macrhybopsis%20storeriana", "Macrhybopsis%20hyostoma", "Macrhybopsis%20sp.%201", "Macrhybopsis%20sp.%202", "Macrhybopsis%20storeriana", "Margariscus%20margarita", "Micropterus%20cataractae", "Micropterus%20coosae", "Micropterus%20notius", "Micropterus%20punctulatus", "Moxostoma%20anisurum", "Moxostoma%20breviceps", "Moxostoma%20carinatum", "Moxostoma%20cervinum", "Moxostoma%20collapsum", "Moxostoma%20erythrurum", "Moxostoma%20lachneri", "Moxostoma%20macrolepidotum", "Moxostoma%20poecilurum", "Moxostoma%20robustum", "Moxostoma%20rupiscartes", "Moxostoma%20spp.", "Moxostoma%20anisurum", "Moxostoma%20ariommum", "Moxostoma%20carinatum", "Moxostoma%20cervinum", "Moxostoma%20collapsum", "Moxostoma%20duquesnei", "Moxostoma%20duquesnii", "Moxostoma%20erythrurum", "Moxostoma%20lachneri", "Moxostoma%20macrolepidotum", "Moxostoma%20n.%20sp.%20cf%20poecilurum", "Moxostoma%20pappillosum", "Moxostoma%20poecilurum", "Moxostoma%20robustum", "Moxostoma%20rupiscartes", "Moxostoma%20sp.%201", "Moxostoma%20sp.%203", "Moxostoma%20sp.%204", "Moxostoma%20sp.%20apalachicola%20redhorse", "Moxostoma%20sp.%20cf.%20erythrurum", "Moxostoma%20sp.%20cf.%20lachneri", "Nocomis%20effusus", "Nocomis%20leptocephalus", "Nocomis%20micropogon", "Nocomis%20platyrhynchus", "Nocomis%20raneyi", "Nocomis%20spp.", "Nocomis%20leptocephalus", "Nocomis%20leptocephalus%20bellicus", "Nocomis%20micropogon", "Nocomis%20raneyi", "Notemigonus%20crysoleucas", "Notropis%20ammophilus", "Notropis%20amoenus", "Notropis%20amplamala", "Notropis%20ariommus", "Notropis%20asperifrons", "Notropis%20atherinoides", "Notropis%20baileyi", "Notropis%20blennius", "Notropis%20boops", "Notropis%20buccatus", "Notropis%20buchanani", "Notropis%20candidus", "Notropis%20chalybaeus", "Notropis%20chlorocephalus", "Notropis%20chrosomus", "Notropis%20cummingsae", "Notropis%20harperi", "Notropis%20hudsonius", "Notropis%20hypsilepis", "Notropis%20leuciodus", "Notropis%20longirostris", "Notropis%20lutipinnis", "Notropis%20maculatus", "Notropis%20micropteryx", "Notropis%20petersoni", "Notropis%20photogenis", "Notropis%20procne", "Notropis%20rubellus", "Notropis%20rubricroceus", "Notropis%20rupestris", "Notropis%20sabinae", "Notropis%20scabriceps", "Notropis%20scepticus", "Notropis%20semperasper", "Notropis%20shumardi", "Notropis%20spectrunculus", "Notropis%20spp.", "Notropis%20stilbius", "Notropis%20stramineus", "Notropis%20telescopus", "Notropis%20texanus", "Notropis%20volucellus", "Notropis%20wickliffi", "Notropis%20xaenocephalus", "Notropis%20alborus", "Notropis%20altipinnis", "Notropis%20ammophilus", "Notropis%20amoenus", "Notropis%20amplamala", "Notropis%20asperifrons", "Notropis%20atherinoides", "Notropis%20baileyi", "Notropis%20bifrenatus", "Notropis%20cahabae", "Notropis%20candidus", "Notropis%20chalybaeus", "Notropis%20chiliticus", "Notropis%20chlorocephalus", "Notropis%20chrosomus", "Notropis%20cummingsae", "Notropis%20edwardraneyi", "Notropis%20harperi", "Notropis%20hudsonius", "Notropis%20hybrid", "Notropis%20hypsilepis", "Notropis%20leuciodus", "Notropis%20longirostris", "Notropis%20lutipinnis", "Notropis%20maculatus", "Notropis%20mekistocholas", "Notropis%20melanostomus", "Notropis%20petersoni", "Notropis%20procne", "Notropis%20rafinesquei", "Notropis%20rubricroceus", "Notropis%20scepticus", "Notropis%20shumardi", "Notropis%20sp.%20(cf.%20N.%20sabinae)", "Notropis%20sp.%20cf.%20chlorocephalus", "Notropis%20sp.%20cf.%20rubellus", "Notropis%20spectrunculus", "Notropis%20stilbius", "Notropis%20telescopus", "Notropis%20texanus", "Notropis%20uranoscopus", "Notropis%20volucellus", "Notropis%20xaenocephalus", "Opsopoeodus%20emiliae", "Percina%20aurantiaca", "Percina%20austroperca", "Percina%20burtoni", "Percina%20caprodes", "Percina%20copelandi", "Percina%20evides", "Percina%20gymnocephala", "Percina%20kathae", "Percina%20kusha", "Percina%20lenticula", "Percina%20macrocephala", "Percina%20maculata", "Percina%20nevisense", "Percina%20nigrofasciata", "Percina%20oxyrhynchus", "Percina%20palmaris", "Percina%20peltata", "Percina%20roanoka", "Percina%20sciera", "Percina%20shumardi", "Percina%20smithvanizi", "Percina%20squamata", "Percina%20vigil", "Percina%20antesella", "Percina%20aurolineata", "Percina%20aurora", "Percina%20austroperca", "Percina%20brevicauda", "Percina%20caprodes", "Percina%20caprodes%20caprodes", "Percina%20crassa", "Percina%20jenkinsi", "Percina%20kathae", "Percina%20kusha", "Percina%20lenticula", "Percina%20maculata", "Percina%20nevisense", "Percina%20nigrofasciata", "Percina%20notogramma", "Percina%20palmaris", "Percina%20rex", "Percina%20roanoka", "Percina%20sciera", "Percina%20shumardi", "Percina%20sipsi", "Percina%20smithvanizi", "Percina%20sp.%20muscadine%20darter", "Percina%20suttkusi", "Percina%20vigil", "Phenacobius%20catostomus", "Phenacobius%20crassilabrum", "Phenacobius%20mirabilis", "Phenacobius%20teretulus", "Phenacobius%20uranops", "Phenacobius%20catostomus", "Phoxinus%20cumberlandensis", "Phoxinus%20erythrogaster", "Phoxinus%20oreas", "Phoxinus%20tennesseensis", "Phoxinus%20oreas", "Pimephales%20notatus", "Pimephales%20promelas", "Pimephales%20spp.", "Pimephales%20vigilax", "Pimephales%20notatus", "Pimephales%20promelas", "Pimephales%20vigilax", "Pimephales%20vigilax%20perspicuus", "Pteronotropis%20euryzonus", "Pteronotropis%20grandipinnis", "Pteronotropis%20hypselopterus", "Pteronotropis%20merlini", "Pteronotropis%20signipinnis", "Pteronotropis%20stonei", "Pteronotropis%20welaka", "Pteronotropis%20euryzonus", "Pteronotropis%20grandipinnis", "Pteronotropis%20hypselopterus", "Pteronotropis%20merlini", "Pteronotropis%20metallicus", "Pteronotropis%20signipinnis", "Pteronotropis%20stonei", "Pteronotropis%20welaka", "Rhinichthys%20atratulus", "Rhinichthys%20cataractae", "Rhinichthys%20obtusus", "Rhinichthys%20atratulus", "Rhinichthys%20cataractae", "Rhinichthys%20obtusus", "Salvelinus%20fontinalis", "Semotilus%20atromaculatus", "Semotilus%20corporalis", "Semotilus%20thoreauianus", "Semotilus%20atromaculatus", "Semotilus%20corporalis", "Semotilus%20lumbee", "Semotilus%20thoreauianus", "Thoburnia%20hamiltoni", "Thoburnia%20rhothoeca"])


    finalSpp = ""
    finalDict = {}
    failedList = []
    with open("BISONDownload.txt", "w") as text_file:
        text_file.write(header)
    with open("BISONDownload_Fails.txt", "a") as text_file:
        text_file.write("These species failed to download from BISON:")
    for spp in sppList:
        print("Running {}...".format(spp))
        url ="http://bisonapi.usgs.ornl.gov/solr/occurrences/select/?q=scientificName:%22" + spp + "%22&rows=2000000&wt=json&json.wrf=BISONObject"
        req= urllib2.Request(url)
        opener = urllib2.build_opener()
        f = opener.open(req)
        spText =  f.read()
        finalSpp = spText
        finalSpp= finalSpp.replace("BISONObject", "")
        finalSpp=finalSpp.replace("(", "")
        finalSpp=finalSpp.replace(")", "")
        finalSpp=finalSpp.replace("}}", "}")
        finalSpp=finalSpp.replace('{"responseHeader":{', "%")
        finalSpp=finalSpp.replace('},"response":', '%"{}":'.format(spp))
        finalSpp = re.sub(r'\%.*?\%', '', finalSpp)
        finalSpp = "{" + finalSpp + "}"
        try:
            sppDict = json.loads(finalSpp)
            finalDict = sppDict#= dict(finalDict.items() + sppDict.items())
            data = ""


            numRecs = finalDict[spp]["numFound"]
            print("Writing {}.  {} records.".format(spp, numRecs))
            counter = 0
            while counter < numRecs:
                try:
                    try:
                        name = finalDict[spp]["docs"][counter]["scientificName"]
                    except:
                        name = "No Name"
                    try:
                        occurrenceID = finalDict[spp]["docs"][counter]["occurrenceID"]
                    except:
                        occurenceID = "-999"
                    try:
                        latDD = finalDict[spp]["docs"][counter]["decimalLatitude"]
                    except:
                        latDD = "-999"
                    try:
                        longDD = finalDict[spp]["docs"][counter]["decimalLongitude"]
                    except:
                        longDD = "-999"
                    try:
                        year = finalDict[spp]["docs"][counter]["year"]
                    except:
                        year = "-999"
                    try:
                        collector = finalDict[spp]["docs"][counter]["collector"]
                    except:
                        collector = "No Collector Given"
                    try:
                        resource = finalDict[spp]["docs"][counter]["BISONResourceID"]
                    except:
                        resource = "-999"
                    data = data + "\n"+ name  + "," + str(occurrenceID) + "," + str(latDD) + "," + str(longDD) + "," + str(year) + "," + str(collector) + "," + str(resource)
                except Exception as e:
                        tb = sys.exc_info()[2]
                        print("Error on {} on record {}.  Failed on line {}. ".format(spp, counter, tb.tb_lineno) + e.message)
                counter +=1
                finalData = data

            with open("BISONDownload.txt", "a") as text_file:
                text_file.write(finalData)

        except:
            print ("{} failed".format(spp))
            with open("BISONDownload_Fails.txt", "a") as text_file:
                text_file.write("\n{}.".format(spp))
            failedList.append(spp)
            continue

    os.chdir(curDir)
if __name__ == '__main__':
    main()
