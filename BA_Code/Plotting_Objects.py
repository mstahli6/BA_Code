import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
import scipy
import scipy.odr as odr
import numpy as np
import glob
import matplotlib.dates as mdates
from Common_Functions import *
from statistics import mean

class GeneralBoxPlot():
    """
    takes data stored in df x_column as a df[column] y_column as a df[column] and hue_column used to bin the data as
    a df[column] and makes a box plot object

    Parameters
    ----------
    df : object
        pandas data frame object with your data
    x_column : object
        pandas data frame column (EX: df['time'])
    y_column : object
        pandas data frame column (EX: df['ethane'])
    hue_column : object
        pandas data frame column (EX: df['site'])
    """
    def __init__(self, df, x_column, y_column, hue_column):
        self.df = df
        self.x = x_column
        self.y = y_column
        self.hue = hue_column

    def plotting_func(self, x_label='xlabel', y_label='ylabel', title='title', style='darkgrid', font_scale=4,

                      palette=None, showmeans=True, showfliers=False, legend=True, hue_order=None):
        """
        take self parameters from when class was instantiated and produces a boxplot

        Parameters
        ----------
        x_label : str
            string used as x label
        y_label : str
            string used as x label
        title : str
            string used as title
        style : str
            string specifying how the plot looks default = 'darkgrid' look up Seaborn styles for more options
        font_scale : int or float
            font size parameter default 4
        palette : list of str
            list of hex codes specifying color (normally use site colors)
        showmeans : bool
            True or False adds white circle showing means to box plot default = True
        showfliers : bool
            True or False adds points all above 95th percentile to box plot default = False
        legend : bool
            True or False adds or hides legend from the figure
        hue_order : list of str
            The order in which the hue column boxes are ordered

        Returns
        _______
        None
            makes a boxplot figure
        """
        sns.set(style=style, font_scale=font_scale)
        if palette is not None:
            sns.set_palette(palette=palette) #creat palette in list ex. ['#0CF215']
        ax1 = sns.boxplot(x=self.x, y=self.y, data=self.df, hue=self.hue, whis=[5, 95], showmeans=showmeans,
                          showfliers=showfliers,
                          hue_order=hue_order,
                          meanprops={"marker": "o",
                                     "markerfacecolor": "white",
                                     "markeredgecolor": "black",
                                     "markersize": "15"})
        ax1.set_xlabel(x_label, labelpad=20)
        ax1.set_ylabel(y_label, labelpad=20)
        ax1.set_title(title)
        if legend is True:
            plt.subplots_adjust(right=0.84)
            ax1.legend(bbox_to_anchor=(1.225, 1.029))
        else:
            ax1.get_legend().remove()
        plt.show()