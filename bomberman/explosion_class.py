
class Explosion:

    def __init__(self, area,bombs,players,goodies):
        self.area = area
        self.bombs = bombs
        self.players = players
        self.goodies = goodies
        self.explodedBombs = set()
        self.explodedArea = dict()

    def _explodeBomb(self,bombId):
        #already exploded
        if bombId in self.explodedBombs:
            return 
        
        self.explodedBombs.add(bombId)
        x , y, _ , radius  = self.bombs.getBomb(bombId)
        print("_explodeBomb",bombId,x , y,  radius)

        self._explode(x,y,radius,'o')

    def _explode(self,x,y,radius,fire):

        if radius < 0: return
        if x < 0: return
        if len(self.area[0]) <= x: return
        if y < 0: return
        if len(self.area) <= y: return

        c = self.area[y][x]
        if c == "#": return

        xy = "{}/{}".format(x,y)
        if xy in self.explodedArea: return

        #chain reaction
        if 'o' != fire:
            bombIds = self.bombs.getBombsAtPosition(x,y)
            if len(bombIds) > 0:
                for bombId in bombIds:
                    self._explodeBomb(bombId)
                return

        #explosion

        self.explodedArea[xy] = { "x" : x , "y" : y ,"fire" : fire}

        if c == "*": 
            l = list(self.area[y])
            l[x] = '.'
            self.area[y] = "".join(l)

        if c == ".":
            if fire == 'o' or fire == '>':
                self._explode(x+1,y,radius -1,'>')
            if fire == 'o' or fire == '<':
                self._explode(x-1,y,radius -1,'<')
            if fire == 'o' or fire == 'V':
                self._explode(x,y+1,radius -1,'V')
            if fire == 'o' or fire == 'A':
                self._explode(x,y-1,radius -1,'A')

    def trigger(self):
        for onfire in self.bombs.getBombsOnFire():
            self._explodeBomb(onfire)

    def getExploded(self):
        return self.explodedBombs

    def getArea(self):
        return list(self.explodedArea.values())