
from .container_classes import Players
from .container_classes import Bombs
from .container_classes import Goodies

def test_explosion_class():
    from .explosion_class import Explosion
    area = [
        "########",
        "#.**...#",
        "#.*....#",
        "########"
    ]
    bombs = Bombs()
    bombs.addBomb(1,1,time=0,radius=10)
    bombs.addBomb(1,2,time=1000,radius=5)
    bombs.addBomb(3,2,time=1000,radius=1)
    players = Players()
    goodies = Goodies()
    explosion = Explosion(area,bombs,players,goodies)
    explosion.trigger()
    exploded = explosion.getExploded()

    assert { "#1" , "#2" } == exploded
    assert '.' == area[1][2]
    assert '*' == area[1][3]
    assert '.' == area[2][2]

    explosionArea = explosion.getArea();
    assert len(explosionArea) == 4
    assert explosionArea[0]["fire"] == 'o'

