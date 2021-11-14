from .utils import load_area
from .explosion_class import Explosion
from .container_classes import Players
from .container_classes import Bombs
from .container_classes import Goodies

class Bomberman:
    def __init__(self):
        self.state = 0
        #todo player_position and goody_position as class
        self.area , self.player_position , self.goody_position = load_area("data/bomberman/level1.txt")
        self.players = Players()
        self.bombs = Bombs()
        self.goodies = Goodies()


    def handle(self,request):
        responses = []
        if request['type'] == "init":
            
            player_id = request['id']
            if not self.players.hasPlayer(player_id):
                #create
                start_nr =  self.players.size()
                #TODO check max count of players
                position = self.player_position[start_nr]['position']
                self.players.addPlayer(player_id,position["x"],position["y"])
            
            #Send whole state
            responses.append({"type" : "area" ,"area" : self.area })

            for player_id in self.players.getPlayerIds():
                x,y = self.players.getPosition(player_id);
                responses.append({"type" : "position" ,"id" : player_id , "x" : x , "y" : y})

        
        if request['type'] == "cycle":
            cycle = request['cycle']
            self.bombs.incrementTime(cycle)
            explosion = Explosion(self.area,self.bombs,self.players,self.goodies)
            explosion.trigger()
            exploded = explosion.getExploded()

            if len(exploded) > 0:
                self.bombs.deleteBombs(exploded)
                print("exploded",exploded,self.bombs.getBombsPosition())
                responses.append({"type" : "bombs" ,"bombs" : self.bombs.getBombsPosition() })
                responses.append({"type" : "explosion" , "explosion" : explosion.getArea()});
           
            #TODO 
            #send update of field after explosion
            #Check if al players alive



        if request['type'] == "position":
            player_id = request['id']
            if self.players.hasPlayer(player_id):
                self.players.setPosition(player_id,request['x'],request['y']);
                x,y = self.players.getPosition(player_id);
                responses.append({"type" : "position" ,"id" : player_id , "x" : x , "y" : y })

        if request['type'] == "bomb":
            player_id = request['id']
            if self.players.hasPlayer(player_id):
                x,y = self.players.getPosition(player_id);
                self.bombs.addBomb(x,y,time=2000,radius=2)
                responses.append({"type" : "bombs" ,"bombs" : self.bombs.getBombsPosition() })

        return responses
