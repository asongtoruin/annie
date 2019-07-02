#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class AnimatedGraph:
    def __init__(self, animate_from, x_vals, y_vals):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        self.animate_from = animate_from
        self.set_anim_params()

        # Set up x values and y values
        self._x_vals = x_vals
        self._y_vals = y_vals

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

    def _get_simple_position(self, i):
        if i <= self.start_frames:
            i = 0
        elif i <= self.start_frames + self.plot_frames:
            i -= self.start_frames
        else:
            i = self.plot_frames

        curr_frac = self._frame_fractions[i]
        if self.animate_from in ('x', 'origin'):
            y_pos = self._y_vals * curr_frac
        else:
            y_pos = self._y_vals

        if self.animate_from in ('y', 'origin'):
            x_pos = self._x_vals * curr_frac
        else:
            x_pos = self._x_vals

        return x_pos, y_pos


class AnimatedScatter(AnimatedGraph):
    def __init__(self, x, y, data, animate_from='x', x_lims=None, y_lims=None,
                 plot_kwargs=None):
        if animate_from not in ('x', 'y', 'origin'):
            raise ValueError(
                f'parameter animate_from should be one of x, y or origin '
                f'(current value "{animate_from}")'
            )

        x_vals = data[x]
        y_vals = data[y]

        self.animate_from = animate_from

        # Do an initial plot to get the axis limits for our final frame.
        if not (x_lims and y_lims):
            ax = sns.scatterplot(x_vals, y_vals)
            if not x_lims:
                x_lims = ax.get_xlim()
            if not y_lims:
                y_lims = ax.get_ylim()
        self._x_lims = x_lims
        self._y_lims = y_lims
        plt.close()

        super().__init__(
            animate_from=animate_from, x_vals=x_vals, y_vals=y_vals
        )

    def _animate(self, i):
        # first let's do a simple grow from the x axis
        self.ax.clear()

        sns.scatterplot(*self._get_simple_position(i), ax=self.ax)
        self.ax.set_xlim(*self._x_lims)
        self.ax.set_ylim(*self._y_lims)


if __name__ == '__main__':
    import pandas as pd
    np.random.seed(1)

    df = pd.DataFrame(
        {'x': np.random.randint(0, 20, 20),
         'y': np.random.randint(0, 20, 20)}
    )

    print(df)

    test_plot = AnimatedScatter(
        data=df, x='x', y='y', animate_from='origin',
        x_lims=(0, 20), y_lims=(0, 20)
    )
    test_plot.set_fig_size((10, 10))
    test_plot.set_anim_params(smoothing_value=5)
    # plt.show()
    test_plot.save('from_origin.mp4')
