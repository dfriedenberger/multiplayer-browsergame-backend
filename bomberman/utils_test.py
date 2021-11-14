


def test_load_area():
    from .utils import load_area
    area , player , goodies = load_area("data/bomberman/level1.txt")
    assert 11 == len(area)
    assert 30 == len(area[0])
    assert 4 == len(player)
    assert "2" == player[1]['key']
    assert 28 == player[1]['position']['x']
    assert 9 == player[1]['position']['y']
    assert 0 == len(goodies)

