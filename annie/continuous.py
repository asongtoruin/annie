#!/usr/bin/env python
# -*- coding: utf-8 -*-
import seaborn as sns
from matplotlib import pyplot as plt

from . import AnimatedGraph, copy_dict


class AnimatedScatter(AnimatedGraph):
    def __init__(self, x, y, animate_from='x', x_lims=None, y_lims=None,
                 plot_kwargs=None, legend_kwargs=None):
        if animate_from not in ('x', 'y', 'origin'):
            raise ValueError(
                f'parameter animate_from should be one of x, y or origin '
                f'(current value "{animate_from}")'
            )

        super().__init__(
            animate_from=animate_from, x=x, y=y, func=sns.scatterplot,
            plot_kwargs=plot_kwargs, legend_kwargs=legend_kwargs
        )

        # Do an initial plot to get the axis limits for our final frame.
        if not (x_lims and y_lims):
            ax = sns.scatterplot(
                self._x_plot, self._y_plot, legend=False, **self.plot_kwargs
            )
            if not x_lims:
                x_lims = ax.get_xlim()
            if not y_lims:
                y_lims = ax.get_ylim()

        self._x_lims = x_lims
        self._y_lims = y_lims
        plt.close()

    def _animate(self, i):
        super()._animate(i)
        self.ax.set_xlim(*self._x_lims)
        self.ax.set_ylim(*self._y_lims)
