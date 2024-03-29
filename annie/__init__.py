#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import deepcopy

import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np


def copy_dict(input_dict):
    return deepcopy(input_dict) if input_dict else dict()


class AnimatedGraph:
    def __init__(self, x, y, func, animate_from, plot_kwargs=None,
                 legend_kwargs=None):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        self._func = func

        self.animate_from = animate_from
        self.set_anim_params()

        self.plot_kwargs = copy_dict(plot_kwargs)
        self.legend_kwargs = copy_dict(legend_kwargs)

        if plot_kwargs:
            self.plot_kwargs = deepcopy(plot_kwargs)
            if 'data' in self.plot_kwargs:
                self.data_mode = True
                self.data = plot_kwargs.pop('data').copy()

                self._x_plot = x + '_plot'
                self._y_plot = y + '_plot'

                self.data[self._x_plot] = self.data[x]
                self.data[self._y_plot] = self.data[y]

                self.plot_kwargs['data'] = self.data
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
        self.ax.clear()

        self._update_simple_position(i)

        self._func(
            self._x_plot, self._y_plot, ax=self.ax, **self.plot_kwargs
        )

        if self.legend_kwargs:
            plt.legend(**self.legend_kwargs)

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
