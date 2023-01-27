#-------------------------------------------------------------------------------
# Purpose:     Module to test for correlation between two fields in a FC.  Calcs
#              Pearson's, Spearman's, covariance, and plots the two datasets in a
#              scatterplt
#              Based on: https://machinelearningmastery.com/how-to-use-correlation-to-understand-the-relationship-between-variables/
#               and: https://stackoverflow.com/questions/7908636/is-it-possible-to-make-labels-appear-when-hovering-mouse-over-a-point-in-matplot
#
# Author:      emartin@tnc.org
#
# Created:     16/07/2021
#-------------------------------------------------------------------------------
import arcpy
from numpy import mean
from numpy import std
from numpy.random import randn
from numpy.random import seed
from numpy import cov
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from collections import defaultdict
import mpld3

fc = r"K:\FWResilience\Tool\intraFCN_Traversability_MergedBranches\intraFCNTraversability.gdb\fcns_2021_07_1920_59_12_081000" #r"K:\FWResilience\Tool\intraFCN_Traversability_MergedBranches\intraFCNTraversability.gdb\IntraFCNTrav_Results_2021_07_1617_35_22_060000" #r"C:\Users\emartin\Documents\ArcGIS\scratch\intraFCNMerged.gdb\fcns" #arcpy.GetParameterAsText(0) #r"K:\FWResilience\Tool\intraFCN_Traversability_MergedBranches\intraFCNTraversability.gdb\FunctionalNetworks2070_1_4"
field1 =  "intraFCNTravPerc" #arcpy.GetParameterAsText(1) #"intraFCNTravPerc"
field2 =  "p1kaor30" #arcpy.GetParameterAsText(2) #"pikaor30"
labelField = "funcNetID"
symbolField = "totalLength"
selection = "intraFCNTravPerc > 0.5 and intraFCNTravPerc <1 and p1kaor30 is not null and p1kaor30 <> 0" # #arcpy.GetParameterAsText(3) #"intraFCNTravPerc > 0.5 and intraFCNTravPerc <1 and pikaor30 is not null"
outputHTML = r"C:\Users\emartin\Desktop\{}_{}.html".format(field1, field2)
fcName = fc.split("\\")[-1]


def main():
    if symbolField != "":
        data1, data2, labels, s = getData(fc, field1, field2, selection, labelField, symbolField)
    else:
        data1, data2, labels, s = getData(fc, field1, field2, selection, labelField)

    covariance = calculateCovariance(data1, data2)
    pearsons = calculatePearsonsCorrelation(data1, data2)
    spearmans = calculateSpearmansCorrelation(data1, data2)
    plt = plotData(data1, data2, labels, s, covariance, pearsons, spearmans)
    savePlot(plt)

def savePlot(fig):
    html_str = mpld3.fig_to_html(fig)
    Html_file= open(outputHTML,"w")
    Html_file.write(html_str)
    Html_file.close()


def getData(fc, field1, field2, selection, labelField = "OBJECTID", symbolField = None):
    xDict = {}
    yDict= {}

    symbolDict = {}

    if symbolField != None:
        fields = (field1, field2, labelField, symbolField)
    else:
        fields = (field1, field2, labelField)
    with arcpy.da.SearchCursor(fc, fields, selection) as rows:
        for row in rows:
            xDict[row[2]] = row[0]
            yDict[row[2]] = row[1]
            if symbolField != None:
                symbolDict[row[2]] = row[3]
            else:
                symbolDict[row[2]] = 50

##    s = list(set([20*2**n for n in range(len(symbols))]))
    x = []
    y = []
    symbols = []
    labels = []

    for key in xDict:
        x.append(xDict[key])
        y.append(yDict[key])
        symbols.append(symbolDict[key])
        labels.append("{}={} \n{}={} \n{}={}".format(labelField, key, field1, round(xDict[key], 2), field2, round(yDict[key], 2)))

    if symbolField != None:
        s = [n/5 for n in range(len(symbols))]
    else:
        s = 50

    return x, y, labels, s


def plotData(x, y, labels, s, covariance, pearsons, spearmans):
    # generate related variables
    # summarize
    arcpy.AddMessage('Field 1: mean=%.3f stdv=%.3f' % (mean(x), std(x)))
    arcpy.AddMessage('Field 2: mean=%.3f stdv=%.3f' % (mean(y), std(y)))
    # plot
    fig,ax = plt.subplots()
    sc = plt.scatter(x, y, s=s, marker='o', linewidths=1,  c='b', edgecolors='r')
    plt.xlabel(field1)
    plt.ylabel(field2)

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    fig.canvas.mpl_connect("motion_notify_event", lambda event: hover(event, ax, sc, fig, annot, labels))
    plt.title('{} Correlation:  {}  &  {}\nPearsons={}  Spearmans={}\nPoints scaled by {}'.format(fcName, field1, field2,  round(pearsons, 2), round(spearmans, 2), symbolField), y=0.985, fontsize=10)

    plt.show()
    return fig

def calculateCovariance(data1, data2):
    # calculate the covariance between two variables
    # seed random number generator

    # calculate covariance matrix
    covariance = cov(data1, data2)
    arcpy.AddMessage("covarianc= {}".format(covariance))
    return covariance


def calculatePearsonsCorrelation(data1, data2):
    # calculate Pearson's correlation
    corr, _ = pearsonr(data1, data2)
    arcpy.AddMessage('Pearsons correlation: %.3f' % corr)
    return corr

def calculateSpearmansCorrelation(data1, data2):
    # calculate spearman's correlation
    corr, _ = spearmanr(data1, data2)
    arcpy.AddMessage('Spearmans correlation: %.3f' % corr)
    return corr

def update_annot(ind, sc, annot, labels):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
##    text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))),  " ".join([str(labels[n]) for n in ind["ind"]]))
    text = "{}".format([str(labels[n]) for n in ind["ind"]][0])
    annot.set_text(text)
##    annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.8)


def hover(event, ax, sc, fig, annot, labels):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind, sc, annot, labels)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

if __name__ == '__main__':
    main()
