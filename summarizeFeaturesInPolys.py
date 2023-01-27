#-------------------------------------------------------------------------------
# Name:        functions to summarize the area and length of polygons and linear features
#               respectively in a reservoir (or other polygon)
#
# Author:      emartin@tnc.org
#
# Created:     24/09/2019
#-------------------------------------------------------------------------------
import arcpy, sys, os
from collections import defaultdict
arcpy.env.overwriteOutput = True

gdb = r"C:\Users\emartin\Desktop\test.gdb" #Path to GDB workspace

def main():
    #these are examples for syntax
    polysInReservoirs(r"C:\Users\emartin\Desktop\test.gdb\reservoir", "resID",  [r"C:\Users\emartin\Desktop\test.gdb\agr",], "inundatedAgrLand")
    linearLengthInreservoir(r"C:\Users\emartin\Desktop\test.gdb\reservoir", "resID",  [r"C:\Users\emartin\Desktop\test.gdb\roads", r"C:\Users\emartin\Desktop\test.gdb\transLine"], "inundatedInfrastructure")

def polysInReservoirs(reservoirs, resID,  polyList, nameAbbrv):
    try:
        """
        reservoirs: the reservoir polygon layer
        resID: the unique ID for each reservoir
        polyList: a list of polygon feature classes that will be merged together.
                  The total area of these polygons in aech reservoir will be calculated
                  If a single layer, make as a list with with a trailing comma.
                  As in: ["agriculturalLand",]
        nameAbbrv: String. a short name that will be used for fields and intermediate feature classes.  e.g. "agriLand"

        """
        print(("...starting poly area in reservoir metric for {}...".format(nameAbbrv)))

        #delete old fields before intersecting, or they persist
        delFields = ("{}Area".format(nameAbbrv),)
        for field in delFields:
            try:
                arcpy.DeleteField_management(reservoirs, field)
            except:
                pass

        reservoirAreaDict = {}
        fields = (resID, "SHAPE_Area")
        with arcpy.da.SearchCursor(reservoirs, fields) as rows:
            for row in rows:
                reservoirAreaDict[row[0]] = row[1]

        if len(polyList) > 1:
            merged = os.path.join(gdb, "{}Merge".format(nameAbbrv))
            arcpy.Merge_management(polyList, merged)
        elif len(polyList) == 1:
            merged = polyList[0]
        else:
            print("There was a problem merging the polygon layers. Length of feature list...")
            sys.exit()

        intersectedReservoirs =  os.path.join(gdb, "{}Reservoirs".format(nameAbbrv))
        arcpy.Intersect_analysis([merged, reservoirs], intersectedReservoirs)

        featAreaDict = defaultdict(list)
        with arcpy.da.SearchCursor(intersectedReservoirs, fields) as rows:
            for row in rows:
                try:
                    featAreaDict[row[0]].append(row[1]) #there are some reservoirs with multiple sav/oys polys, so add to list and sum
                except:
                    featAreaDict[row[0]] = 0


        arcpy.AddField_management(reservoirs, "{}Area".format(nameAbbrv), "DOUBLE")
        fields = (resID, "{}Area".format(nameAbbrv))
        with arcpy.da.UpdateCursor(reservoirs, fields) as rows:
            for row in rows:
                try:
                    row[1] = sum(featAreaDict[row[0]])
                except:
                    row[1] = 0
                rows.updateRow(row)


    except Exception as e:
        tb = sys.exc_info()[2]
        msg = "Problem running poly area in reservoir metric for {} on line {} of Metrics. {}".format(nameAbbrv, tb.tb_lineno, e)
        print(msg)
        sys.exit()

def linearLengthInreservoir(reservoirs, resID,  linearFeatList, nameAbbrv):
    try:
        """
        reservoirs: the reservoir polygon layer
        resID: the unique ID for each reservoir
        linearFeatList: a list of line feature classes that will be merged together.  THe total length of these lines in each reservoir will be calculated
        nameAbbrv: string. a short name that will be used for fields and intermediate feature classes.  e.g. "savOys"
        numTiers: the number of 5% Tiers that will be assigned points.  e.g. 5 tiers if the top 25% will get points
        numPoints: the number of points taht will be assigend to those tiers
        """
        print(("...starting linear feature length in reservoir metric for {}...".format(nameAbbrv)))

        #delete old fields before intersecting, or they persist
        delFields = ("{}Length".format(nameAbbrv),)
        for field in delFields:
            try:
                arcpy.DeleteField_management(reservoirs, field)
            except:
                pass


        if len(linearFeatList) > 1:
            merged = os.path.join(gdb, "{}Merge".format(nameAbbrv))
            arcpy.Merge_management(linearFeatList, merged)
        elif len(linearFeatList) == 1:
            merged = linearFeatList[0]
        else:
            print("There was a problem merging the line layers.  Length of feature list...")
            sys.exit()

        intersectedReservoirs =  os.path.join(gdb, "{}Reservoirs".format(nameAbbrv))
        print("...intersecting...")
        arcpy.Intersect_analysis([merged, reservoirs], intersectedReservoirs)

        featLengthDict = defaultdict(list)
        fields =  (resID, "Shape_Length")
        with arcpy.da.SearchCursor(intersectedReservoirs, fields) as rows:
            for row in rows:
                try:
                    featLengthDict[row[0]].append(row[1]) #there are some reservoirs with multiple features, so add to list and sum
                except:
                    featLengthDict[row[0]] = 0


        arcpy.AddField_management(reservoirs, "{}Length".format(nameAbbrv), "DOUBLE")
        fields = (resID, "{}Length".format(nameAbbrv))
        with arcpy.da.UpdateCursor(reservoirs, fields) as rows:
            for row in rows:
                try:
                    row[1] = sum(featLengthDict[row[0]])
                except:
                    row[1] = 0
                rows.updateRow(row)


    except Exception as e:
        tb = sys.exc_info()[2]
        msg = "Problem running linear feature metrics for {} on line {} of Metrics. {}".format(nameAbbrv, tb.tb_lineno, e)
        print(msg)
        sys.exit()

if __name__ == '__main__':
    main()
