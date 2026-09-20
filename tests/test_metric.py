import sys
sys.path.insert(0, "src")

from metric import correlation_like_metric
from eigen import minimum_eigenvalue


def test_metric_dimension():
    g = correlation_like_metric(40)

    assert len(g) == 40
    assert minimum_eigenvalue(g) == 10**18