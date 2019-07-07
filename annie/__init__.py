#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import deepcopy

import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def copy_dict(input_dict):
    return deepcopy(input_dict) if input_dict else dict()


class AnimatedGraph:
    def __init__(self, x, y, animate_from, plot_kwargs=None):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        self.animate_from = animate_from
        self.set_anim_params()

        self.plot_kwargs = copy_dict(plot_kwargs)

        if plot_kwargs:
            self.plot_kwargs = deepcopy(plot_kwargs)
            if 'data' in self.plot_kwargs:
                self.data_mode = True
                self.data = plot_kwargs.pop('data').copy()

                self.plot_kwargs['data'] = self.data

                self._x_plot = x + '_plot'
                self._y_plot = y + '_plot'
                print('ENGAGE DATA MODE')
            else:
                self.data_mode = False
                self.data = None

                self._x_plot = deepcopy(x)
                self._y_plot = deepcopy(y)

        self._x = x
        self._y = y

    def set_fig_size(self, fig_size):
        plt.close(self.fig)
        self.fig, self.ax = plt.subplots(figsize=fig_size)
        # self.fig has changed, so we need to re-declare self._ani
        self._ani = anim.FuncAnimation(
            self.fig, self._animate, frames=self.plot_frames
        )

    def set_anim_params(self, duration=5, start_wait=0, end_wait=2,
                        fps=60, bitrate=-1, smoothing_value=3, writer='ffmpeg'):
        self.start_frames = start_wait * fps
        self.plot_frames = duration * fps
        self.end_frames = end_wait * fps

        self.writer = anim.writers[writer](
            fps=fps, metadata=dict(artist='Me'), bitrate=bitrate
        )

        self._ani = anim.FuncAnimation(
            self.fig, self._animate,
            frames=self.start_frames + self.plot_frames + self.end_frames
        )

        mult = -1 if smoothing_value % 2 == 0 else 1

        self._frame_fractions = 1 + mult * np.arange(
            start=-1, stop=1/self.plot_frames, step=1 / self.plot_frames
        ) ** smoothing_value

    def _animate(self, i):
        pass

    def save(self, f_path):
        self._ani.save(f_path, self.writer)

    def _update_simple_position(self, i):
        if i <= self.start_frames:
            i = 0
        elif i <= self.start_frames + self.plot_frames:
            i -= self.start_frames
        else:
            i = self.plot_frames

        curr_frac = self._frame_fractions[i]
        if self.animate_from in ('x', 'origin'):
            if self.data_mode:
                self.data[self._y_plot] = self.data[self._y] * curr_frac
            else:
                self._y_plot = self._y * curr_frac

        if self.animate_from in ('y', 'origin'):
            if self.data_mode:
                self.data[self._x_plot] = self.data[self._x] * curr_frac
            else:
                self._x_plot = self._x * curr_frac


class AnimatedScatter(AnimatedGraph):
    def __init__(self, x, y, animate_from='x', x_lims=None, y_lims=None,
                 plot_kwargs=None, legend_kwargs = None):
        if animate_from not in ('x', 'y', 'origin'):
            raise ValueError(
                f'parameter animate_from should be one of x, y or origin '
                f'(current value "{animate_from}")'
            )

        self.animate_from = animate_from
        self.legend_kwargs = copy_dict(legend_kwargs)

        super().__init__(
            animate_from=animate_from, x=x, y=y, plot_kwargs=plot_kwargs
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
        # first let's do a simple grow from the x axis
        self.ax.clear()

        self._update_simple_position(i)

        sns.scatterplot(
            self._x_plot, self._y_plot, ax=self.ax, **self.plot_kwargs
        )
        self.ax.set_xlim(*self._x_lims)
        self.ax.set_ylim(*self._y_lims)

        if self.legend_kwargs:
            plt.legend(**self.legend_kwargs)


if __name__ == '__main__':
    import pandas as pd
    np.random.seed(1)

    df = pd.DataFrame(
        {'x': np.random.randint(0, 20, 20),
         'y': np.random.randint(0, 20, 20),
         'hue': np.random.choice(('A', 'B', 'C'), size=20)}
    )

    print(df)

    test_plot = AnimatedScatter(
        x='x', y='y', animate_from='origin',
        x_lims=(0, 20), y_lims=(0, 20),
        plot_kwargs=dict(data=df, hue='hue'), legend_kwargs=dict(loc='upper left')
    )
    test_plot.set_fig_size((10, 10))
    test_plot.set_anim_params(smoothing_value=5)
    # plt.show()
    test_plot.save('hue_origin.mp4')
