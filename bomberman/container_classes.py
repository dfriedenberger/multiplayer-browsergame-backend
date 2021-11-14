

class Players:

    def __init__(self):
        self.player = dict()

    def addPlayer(self,player_id,x,y):
        self.player[player_id] = {
            "x" : x,
            "y" : y
        }

    def hasPlayer(self,player_id):
        return player_id in self.player

    def size(self):
        return len(self.player.keys())

    def getPlayerIds(self):
        return self.player.keys()

    def setPosition(self,player_id,x,y):
        self.player[player_id]['x'] = x
        self.player[player_id]['y'] = y

    def getPosition(self,player_id):
        data = self.player[player_id]
        return data['x'] , data['y']

class Bombs:
    
    def __init__(self):
        self.bomb = dict()
        self.id = 0

    def addBomb(self,x,y,time,radius):
        self.id += 1
        self.bomb["#{}".format(self.id)] = {"x" : x , "y" : y,"time" : time, "radius" : radius}

    def getBomb(self,id):
        bomb = self.bomb[id]
        return bomb['x'] , bomb['y'] , bomb['time'] , bomb['radius'] , 

    def incrementTime(self,time):
        for bomb in self.bomb.values():
           bomb['time'] -= time

    def deleteBombs(self,ids):
        for id in ids:
            del self.bomb[id]

    def getBombsOnFire(self):
        onfire = set()
        for id, bomb in self.bomb.items():
            if bomb['time'] <= 0:
                onfire.add(id)
        return onfire

    def getBombsAtPosition(self,x,y):
        bombs = set()
        for id, bomb in self.bomb.items():
            if bomb['x'] == x and bomb['y'] == y:
                bombs.add(id)
        return bombs

    def getBombsPosition(self):
        positions = []
        for bomb in self.bomb.values():
            positions.append({ "x" : bomb['x'] , "y" : bomb['y']})
        return positions


class Goodies:

    def __init__(self):
        pass
