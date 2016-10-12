
import matplotlib


import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.table import Table

import numpy as np
import pandas as pd

mpl.rc('font', family='Arial')

class BatchResultTable(object):

    def __init__(self, data, cons, wgap=0.01, colors={}):

        # Assign default color values, if it is not defined.
        self._colors = dict(colors)
        self._set_default_color('cond_up_cell', 'blue')
        self._set_default_color('cond_dn_cell', 'white')
        self._set_default_color('result_up_cell', '#35FF50')  # Green
        self._set_default_color('result_dn_cell', '#FF0000')  # Red
        self._set_default_color('result_up_text', 'black')
        self._set_default_color('result_dn_text', 'white')


        self._dfc = data.df_ba  # DataFrame of condition cases
        self._dfe = data.df_exp  # DataFrame of experiment results

        # DataFrame of consensus between experiments and simulations
        self._dfr = cons


        fig, ax = plt.subplots()
        self._fig = fig
        self._fig.set_facecolor('white')

        self._ax = ax
        self._ax.set_frame_on(False)
        self._ax.invert_yaxis()

        self.tb = Table(self._ax, bbox=[0, 0, 1, 1])  # matplotlib's Table object
        self.tb.auto_set_font_size(False)

        self.n_conds = self._dfc.shape[0]  # the number of condition cases
        self.n_cond_cols = self._dfc.shape[1]  # the number of condition labels
        self.n_res_cols = self._dfr.shape[1]  # the number of result labels

        # The number of total rows and columns of Table
        self.nrows = self._dfc.shape[0]
        self.ncols = self._dfc.shape[1] + self._dfr.shape[1] + 1

        # The width of the sub-tables
        self.wgap = wgap

        # Calculate the width and height of a signle cell
        L = 1.0
        H = 1.0

        self.w_cell = (L - self.wgap) / (self.ncols - 1)
        self.h_cell = H / self.nrows

        # Create cells for table graphics
        self._add_vertical_gap()
        self._add_condition_subtable()
        self._add_result_subtable()

        # Set default values using properties
        self.table_fontsize = 4
        self.row_label_fontsize = 5
        self.column_label_fontsize = 5
        self.line_width = 0.5

        """
        Add labels using x and y axes. The above default values should be
        assigned before adding labels
        """
        self._add_row_labels()
        self._add_column_labels()



        # Add the table graphic object
        self._ax.add_table(self.tb)

    # end of def __init__

    def _add_condition_subtable(self):
        for (i, j), val in np.ndenumerate(self._dfc):
            if val != 0:
                fcolor = self.colors['cond_up_cell']
            else:
                fcolor = self.colors['cond_dn_cell']

            self.tb.add_cell(i, j,
                             self.w_cell, self.h_cell,
                             loc='center', facecolor=fcolor)
    # end of def

    def _add_result_subtable(self):
        """
        Agreement between the results of simulation and experiment
        """
        for (i, j), val_cons in np.ndenumerate(self._dfr):
            if val_cons == True:
                fcolor =  self.colors['result_up_cell']
            elif val_cons == False:
                fcolor = self.colors['result_dn_cell']
            else:
                raise ValueError("The value of result table element "
                                 "should be bool.")

            val_exp = self._dfe.iloc[i, j]
            if val_exp > 0:
                text_arrow = 'UP'
            elif val_exp < 0:
                text_arrow = 'DN'
            else:  # val_Exp == 0
                text_arrow = '─'

            self.tb.add_cell(i, self.n_cond_cols + 1 + j,
                             self.w_cell, self.h_cell,
                             text=text_arrow,
                             loc='center',
                             facecolor=fcolor)
        # end of for


        # Set colors of the result
        celld = self.tb.get_celld()
        for (i, j), val in np.ndenumerate(self._dfr):
            cell = celld[(i, self.n_cond_cols + 1 + j)]

            # Set colors
            if val > 0:
                tcolor = self.colors['result_up_text']
            else:
                tcolor = self.colors['result_dn_text']
            # end of if-else

            # Adjust text
            cell.set_text_props(color=tcolor,
                                weight='bold')
        # end of for

    # end of def

    def _add_vertical_gap(self):
        """
        Add a vertical gap between condition and result
        """

        for i in range(-1, self.n_conds):
            self.tb.add_cell(i, self.n_cond_cols, self.wgap, self.h_cell,
                        text='',
                        loc='center',
                        edgecolor='none',
                        facecolor='none')

        # end of for
    # end of def

    def _add_row_labels(self):
        """
        Add column labels using y-axis
        """
        ylabels = list(self._dfr.index)
        self._ax.yaxis.tick_left()

        yticks = [self.h_cell / 2.0,]  # The position of the first label
        # The row labels of condition subtable
        for j in range(1, self.n_conds):
            yticks.append(yticks[j-1] + self.h_cell)

        self._ax.set_yticks(yticks)
        self._ax.set_yticklabels(ylabels, minor=False)

        # Hide the small bars of ticks
        for tick in self._ax.yaxis.get_major_ticks():
            tick.tick1On = False
            tick.tick2On = False
    # end of def

    def _add_column_labels(self):
        """
        Add column labels using x-axis
        """
        xlabels = list(self._dfc.columns) + [''] + list(self._dfr.columns)
        self._ax.xaxis.tick_top()

        xticks = [self.w_cell / 2.0,]  # The position of the first label
        # The column labels of condition subtable
        for j in range(1, self.n_cond_cols):
            xticks.append(xticks[j - 1] + self.w_cell)

        # Position of the gap
        xticks.append(xticks[self.n_cond_cols-1] \
                      + self.w_cell/2.0 + self.wgap/2.0)

        # Position of the first label in the result table
        xticks.append(xticks[self.n_cond_cols] \
                      + self.w_cell/2.0 + self.wgap/2.0)

        # The columns of result subtable
        for j in range(1, self.n_res_cols):
            xticks.append(xticks[self.n_cond_cols + j] + self.w_cell)

        self._ax.set_xticks(xticks)
        self._ax.set_xticklabels(xlabels, rotation=90, minor=False)


        # Hide the small bars of ticks
        for tick in self._ax.xaxis.get_major_ticks():
            tick.tick1On = False
            tick.tick2On = False
    # end of def

    def _set_default_color(self, prop, defval):
        if prop not in self.colors:
            self.colors[prop] = defval
    # end of def

    # Properties
    @property
    def table_fontsize(self):
        return self._table_fontsize

    @table_fontsize.setter
    def table_fontsize(self, val):
        """
        Resize text fonts
        """
        self._table_fontsize = val
        self.tb.set_fontsize(val)

    @property
    def column_label_fontsize(self):
        return self._column_label_fontsize

    @column_label_fontsize.setter
    def column_label_fontsize(self, val):
        self._column_label_fontsize = val
        self._ax.tick_params(axis='x', which='major',
                            labelsize=self._column_label_fontsize)


    @property
    def row_label_fontsize(self):
        return self._row_label_fontsize

    @row_label_fontsize.setter
    def row_label_fontsize(self, val):
        self._row_label_fontsize = val
        self._ax.tick_params(axis='y', which='major',
                             labelsize=self._row_label_fontsize)

    @property
    def line_width(self):
        return self._column_label_fontsize

    @line_width.setter
    def line_width(self, val):
        """
        Adjust the width of table lines
        """
        self._line_width = val
        celld = self.tb.get_celld()
        for (i, j), cell in celld.items():
            cell.set_linewidth(self._line_width)

    @property
    def colors(self):
        return self._colors


    @property
    def figure(self):
        return self._fig

    @property
    def axis(self):
        return self._ax