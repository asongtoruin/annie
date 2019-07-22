#!/usr/bin/env python
# -*- coding: utf-8 -*-
import seaborn as sns
from matplotlib import pyplot as plt

from . import AnimatedGraph, copy_dict


class AnimatedBar(AnimatedGraph):
    def __init__(self, categories, values, orient='v', value_lims=None,
                 plot_kwargs=None, legend_kwargs=None):
        temp_p_kws = copy_dict(plot_kwargs) if plot_kwargs else dict()

        if orient == 'v':
            animate_from = 'x'
            x_vals = categories
            y_vals = values
            self._value_ax = 'y'
        elif orient == 'h':
            animate_from = 'y'
            x_vals = values
            y_vals = categories
            self._value_ax = 'x'
        else:
            raise ValueError

        temp_p_kws['orient'] = orient

        super().__init__(
            animate_from=animate_from, x=x_vals, y=y_vals, func=sns.barplot,
            plot_kwargs=plot_kwargs, legend_kwargs=legend_kwargs
        )

        # Do an initial plot to get the axis limits for our final frame.
        if not value_lims:
            ax = sns.barplot(
                self._x_plot, self._y_plot, **self.plot_kwargs
            )
            print('finished initial plot')
            if self._value_ax == 'x':
                value_lims = ax.get_xlim()
            else:
                value_lims = ax.get_ylim()

        self._value_lims = value_lims
        plt.close()

    def _animate(self, i):
        super()._animate(i)
        if self._value_ax == 'x':
            self.ax.set_xlim(*self._value_lims)
        else:
            self.ax.set_ylim(*self._value_lims)
