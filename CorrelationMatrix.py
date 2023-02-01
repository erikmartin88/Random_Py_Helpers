import pandas as pd
import arcpy, sys

in_fgdb_table = "K:/Chesapeake_v3/GIS/xChesFPP.gdb/ChesapeakeDams_current"
fields = ["DA_SqMi", "MAXSTOR", "HEIGHT"]
where = "1=1"
out_excel = "C:/Users/emartin/Desktop/CorrMatrix.xlsx"

def main():
    try:
        df = table_to_data_frame(in_fgdb_table, fields, where)
        print("Running correlation...")
        corr_matrix = df.corr().style.background_gradient(cmap='RdYlBu').format(precision=2).to_excel(out_excel, engine="openpyxl")

    except Exception as e:
        tb = sys.exc_info()[2]
        arcpy.AddMessage ("Problem in summarize US values line {} at. {}".format(tb.tb_lineno, e))
        arcpy.AddError(str(e))
        sys.exit()


def table_to_data_frame(in_table, input_fields=None, where_clause=None):
    # adopted from https://gist.github.com/d-wasserman/e9c98be1d0caebc2935afecf0ba239a0
    """Function will convert an arcgis table into a pandas dataframe with an object ID index, and the selected
    input fields using an arcpy.da.SearchCursor."""
    
    print("Converting table to datafrme...")
    OIDFieldName = arcpy.Describe(in_table).OIDFieldName
    if input_fields:
        final_fields = [OIDFieldName] + input_fields
    else:
        final_fields = [field.name for field in arcpy.ListFields(in_table)]
    data = [row for row in arcpy.da.SearchCursor(in_table, final_fields, where_clause=where_clause)]
    fc_dataframe = pd.DataFrame(data, columns=final_fields)
    fc_dataframe = fc_dataframe.set_index(OIDFieldName, drop=True)
    return fc_dataframe



if __name__ == '__main__':
    main()