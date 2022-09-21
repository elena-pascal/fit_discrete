# Tool to fit discrete distributions to a set of data


import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def read_file(file_name: str) -> np.array:
    return np.loadtxt(file_name, dtype=int)


def show_data(sample_data: np.array, ax: plt.Axes = None, title: str = None) -> plt.Axes:
    r"""
    Always a good idea to look at the data before doing anything to it
    :param sample_data:
    :param ax:
    :param title:
    :return:
    """
    if ax is None:
        _fig, ax = plt.subplots()

    # just count the unique integers and plot as bars
    labels, counts = np.unique(sample_data, return_counts=True)
    ax.bar(labels, counts, align='center', color='C1')

    if title:
        ax.set_title(title)

    # set axes labels
    ax.set_xlabel('data')
    ax.set_ylabel('frequency')

    # non integer ticks are useless here
    ax.xaxis.get_major_locator().set_params(integer=True)
    ax.yaxis.get_major_locator().set_params(integer=True)

    return ax


def fit_uniform(sample_data: np.array):
    """
    The discrete uniform distribution describes a random variable
    that has equal probabilities of being any integers in the
    half open range [a,b)

    :return:
    """
    uniform_dist = stats.randint

    res = stats.fit(uniform_dist, sample_data,
                    bounds={'low': (0, 4), 'high': (0, 4)})
    res.plot()
    plt.show()
    print(res.params)
    print(-np.sum(uniform_dist.logpmf(sample_data, *res.params)))

    return res


def fit_betabinom(sample_data: np.array):

    betabinom_dist = stats.betabinom

    res = stats.fit(betabinom_dist, sample_data, bounds={'n': (0, 4), 'a': (0, 4), 'b': (0, 4), 'loc': (0, 4)})

    res.plot()
    plt.show()
    print(res.params)
    print(-np.sum(betabinom_dist.logpmf(sample_data, *res.params)))


def fit_zipf(sample_data: np.array):

    zipf_dist = stats.zipf

    res = stats.fit(zipf_dist, sample_data, bounds={'a': (0, 4)})

    res.plot()
    plt.show()
    print(res.params)
    print(-np.sum(zipf_dist.logpmf(sample_data, *res.params)))


if __name__ == '__main__':
    data = read_file('test_data.txt')
    show_data(data)
    plt.show()

    fit_uniform(data)
    fit_betabinom(data)
    fit_zipf(data)
