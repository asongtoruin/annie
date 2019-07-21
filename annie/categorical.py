#!/usr/bin/env python
# -*- coding: utf-8 -*-
import seaborn as sns
from matplotlib import pyplot as plt

from . import AnimatedGraph, copy_dict


class AnimatedBar(AnimatedGraph):
    def __init__(self, x, y, y_lims=None,
                 plot_kwargs=None, legend_kwargs=None):
        orient = plot_kwargs.get('orient', 'v') if plot_kwargs else 'v'

        if orient == 'v':
            animate_from = 'x'
        else:
            animate_from = 'y'

        super().__init__(
            animate_from=animate_from, x=x, y=y, func=sns.barplot,
            plot_kwargs=plot_kwargs, legend_kwargs=legend_kwargs
        )

        # Do an initial plot to get the axis limits for our final frame.
        if not y_lims:
            ax = sns.barplot(
                self._x_plot, self._y_plot, legend=False, **self.plot_kwargs
            )
            if not y_lims:
                y_lims = ax.get_ylim()

        self._y_lims = y_lims
        plt.close()

    def _animate(self, i):
        super()._animate(i)
        self.ax.set_ylim(*self._y_lims)
