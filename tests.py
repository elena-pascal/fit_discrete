import pytest
from scipy import stats
from fit_discrete import read_file, distributions, fit_distribution, guess_bounds


@pytest.mark.parametrize("key, expected", [('discrete uniform', 6.591673732008659),
                                           ('beta binomial', 6.068425588244196),
                                           ('zipfian', 7.86098064513523)])
def test_results(key, expected):
    data = read_file('test_data.txt')
    bounds = guess_bounds(data)

    res = fit_distribution(data, distributions[key], bounds[key])
    assert res.success
    assert pytest.approx(expected, res.nllf())


def test_bounds():
    data = stats.randint.rvs(low=0, high=10, size=100)
    bounds = guess_bounds(data)

    res = fit_distribution(data, stats.randint, bounds['discrete uniform'])
    assert res.success

    res = fit_distribution(data, stats.betabinom, bounds['beta binomial'])
    assert res.success

    res = fit_distribution(data, stats.zipf, bounds['zipfian'])
    assert res.success

