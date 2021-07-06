'''collection of different plots'''
import numpy as np
from matplotlib import pyplot as plt


def plot_box(condensed_matrix):
    plt.boxplot(condensed_matrix)
    plt.show()


def plot_histogram(condensed_matrix):
    n_bins = len(np.array(list(set(condensed_matrix))))
    plt.hist(condensed_matrix, bins=n_bins)
    plt.show()


def plot_image(matrix):
    plt.imshow(matrix)
    plt.colorbar()
    plt.show()


def plot_at_y(condensed_matrix):
    plt.plot(condensed_matrix, np.zeros_like(condensed_matrix), '.',)
    plt.show()