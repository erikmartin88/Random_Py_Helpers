import arcpy
from arcpy.sa import *
sourceWorkspace = "K:\\Ogooue\\GIS_Data\\elevation\\SRTM_30m_2014.gdb\\"
outputWorksapce ="K:\\Congo_SoundaDam\\GIS_nonSync\\SRTM_30m_2014.gdb\\"
arcpy.env.workspace = sourceWorkspace

rasterList = arcpy.ListRasters()
for raster in rasterList:
    print("Reprojecting {}".format(raster))
    outRaster = outputWorksapce + raster
    projection = r"K:\Congo_SoundaDam\GIS\WGS 1984 UTM Zone 33S.prj" #"GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],METADATA['World',-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]"

    resampleType = "NEAREST"
    cellSize = 30
    geographicTransform = "" #"WGS_1984_(ITRF00)_To_NAD_1983"
    registrationPoint = ""
    inCoordSys = r"K:\Ogooue\GIS_Data\elevation\WGS 1984.prj" #"GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"

    arcpy.ProjectRaster_management(raster, outRaster, projection, resampleType, cellSize, geographicTransform, registrationPoint, inCoordSys)
