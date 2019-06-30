#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.animation as anim
import matplotlib.pyplot as plt
import seaborn as sns


class AnimatedGraph:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self._ani = anim.FuncAnimation(self.fig, self._animate)

        self.writer = anim.writers['ffmpeg'](
            fps=80, metadata=dict(artist='Me'), bitrate=3600
        )

    def set_fig_size(self, fig_size):
        plt.close(self.fig)
        self.fig, self.ax = plt.subplots(figsize=fig_size)
        # self.fig has changed, so we need to re-declare self._ani
        self._ani = anim.FuncAnimation(self.fig, self._animate)

    def _animate(self, i):
        pass

    def save(self, f_path):
        self._ani.save(f_path, self.writer)


class AnimatedScatter(AnimatedGraph):
    def __init__(self, x, y, data):
        self._x_vals = data[x]
        self._y_vals = data[y]

        # Do an initial plot to get the axis limits for our final frame.
        ax = sns.scatterplot(self._x_vals, self._y_vals)
        self._x_lims = ax.get_xlim()
        self._y_lims = ax.get_ylim()
        plt.close()

        super().__init__()

    def _animate(self, i):
        # first let's do a simple grow from the x axis
        self.ax.clear()
        step_size = 0.1

        current_val = step_size * i

        plot_x = self._x_vals
        plot_y = self._y_vals.where(
            self._y_vals < current_val, other=current_val
        )

        sns.scatterplot(x=plot_x, y=plot_y, ax=self.ax)
        self.ax.set_xlim(*self._x_lims)
        self.ax.set_ylim(*self._y_lims)


if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    np.random.seed(1)

    df = pd.DataFrame(
        {'x': range(10),
         'y': np.random.randint(1, 20, 10)}
    )

    print(df)

    test_plot = AnimatedScatter(data=df, x='x', y='y')
    test_plot.set_fig_size((10, 1))
    plt.show()
