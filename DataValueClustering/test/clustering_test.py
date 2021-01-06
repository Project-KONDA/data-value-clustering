from clustering.clustering import fancy_cluster_representation


def test_fancy_cluster_representation():
    values = ["a", "b", "c", "d", "e"]
    clusters = [0, 0, 1, 2, 0]
    assert fancy_cluster_representation(values, clusters) == [['a', 'b', 'e'], ['c'], ['d']]


test_fancy_cluster_representation()