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
    :param ax: if not given, make up one
    :param title: title for plot
    :return: populated ax
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


def fit_distribution(sample_data: np.array, distribution: stats.rv_discrete, bounds):
    r"""
    Fit a discrete distribution to your data
    :param sample_data: 1D data array
    :param distribution: scipy discrete distribution
    :param bounds: dict of bounds, what the dict keys are depends on the distribution
    :return: FitResult containing all the useful info and methods
    """
    res = stats.fit(distribution, sample_data, bounds)
    return res


def guess_bounds(sample_data: np.array):
    low = min(sample_data)
    high = max(sample_data)
    rough_bounds = {'uniform': {'low': low, 'high': high+1, 'loc': (low-1, high)},
              'betabinom': {'n': high-low, 'a': (0, high*10), 'b': (0, high*10), 'loc': (low-1, high)},
              'zipf': {'a': (-1, high*10), 'loc': (low-1, high)}
              }
    return rough_bounds


def set_plot(rows: int = 2, cols: int = 2):
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(15, 12))
    plt.subplots_adjust(hspace=0.5)
    plt.suptitle("Fitted discrete distributions", fontsize=18, y=0.95)
    return axes.ravel()


if __name__ == '__main__':
    data = read_file('test_data.txt')
    axs = set_plot()

    show_data(data, ax=axs[0], title='Input data')

    distributions = {'uniform': stats.randint, 'betabinom': stats.betabinom, 'zipf': stats.zipf}
    bounds = guess_bounds(data)

    for i, (key, dist) in enumerate(distributions.items()):
        result = fit_distribution(sample_data=data,
                                  distribution=dist,
                                  bounds=bounds[key])

        if result.success:
            result.plot(ax=axs[i + 1])

            print(f'Successfully fitted the {key} distribution:')
            print(f'    the fit parameters are: {result.params}')
            print(f'    the negative log likelihood is: {result.nllf()} \n')

        else:
            print(f'Failed to fit the {key} distribution. Check the bounds!')

    # show final plot
    plt.show()

