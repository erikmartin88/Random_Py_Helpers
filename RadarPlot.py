#-------------------------------------------------------------------------------
# Name:        Radar plot / spider diagram.  From:
#               http://stackoverflow.com/questions/24659005/radar-chart-with-multiple-scales-on-multiple-axes
# Purpose:
#
# Author:      emartin
#
# Created:     29/11/2016
# Copyright:   (c) emartin 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import numpy as np
import pylab as pl
import sys
import arcpy

class Radar(object):
    def __init__(self, fig, titles, labels, rect=None):
        try:
            if rect is None:
                rect = [0.05, 0.05, 0.95, 0.95]

            self.n = len(titles)
            self.angles = np.arange(90, 90+360, 360.0/self.n)
            self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i)
                             for i in range(self.n)]

            self.ax = self.axes[0]
            self.ax.set_thetagrids(self.angles, labels=titles, fontsize=14)

            for ax in self.axes[1:]:
                ax.patch.set_visible(False)
                ax.grid("off")
                ax.xaxis.set_visible(False)

            for ax, angle, label in zip(self.axes, self.angles, labels):
                ax.set_rgrids(range(1, 6), angle=angle, labels=label)
                ax.spines["polar"].set_visible(False)
                ax.set_ylim(0, 5)
        except Exception as e:
            tb = sys.exc_info()[2]
            arcpy.AddError("There was a problem defining the Radar class.  Failed on RP line {}. ".format(tb.tb_lineno) + e.message)
            print("There was a problem defining the Radar class.  Failed on RP line {}".format(tb.tb_lineno) + e.message)
            sys.exit()

    def plot(self, values, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)


