def load_area(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return lines

def simplify_area(area):
    narea = []
    for line in area:
        nline = ""
        for c in line:
            if 'A' <= c and c <= 'Z': c = '.'
            nline += c
        narea.append(nline)
    return narea

def find_position(area,start_nr):
    for y in range(len(area)):
        line = area[y]
        for x in range(len(line)):
            if line[x] == start_nr:
                return x , y
    raise Exception("Position not found for "+start_nr)



class Bomberman:
    def __init__(self):
        self.state = 0
        self.area = load_area("data/bomberman/level1.txt")
        self.player = dict()
        self.bombs = []

    def handle(self,request):
        responses = []
        if request['type'] == "init":
            
            player_id = request['id']
            if player_id not in self.player:
                start_nr =  len(self.player.keys())
                x , y = find_position(self.area,"ABCDEFGHIJKLMNOPQRSTUVW"[start_nr])
                self.player[player_id] = {
                    "x" : x,
                    "y" : y
                }
            responses.append({"type" : "area" ,"area" : simplify_area(self.area) })
            for player_id , value in self.player.items():
                responses.append({"type" : "position" ,"id" : player_id , "x" : value["x"] , "y" : value["y"]})

        if request['type'] == "cycle":
            cycle = request['cycle']
            field = simplify_area(self.area)
            explosion = set()
            for i in range(len(self.bombs)):
                self.bombs[i]['time'] -= cycle
                print(self.bombs[i])
                if self.bombs[i]['time'] <= 0:
                    explosion.add(i)
                    

            for i in sorted(explosion,reverse = True):
                self.bombs.pop(i)


        if request['type'] == "position":
            player_id = request['id']
            if player_id in self.player:
                self.player[player_id]['x'] = request['x']
                self.player[player_id]['y'] = request['y']
                value = self.player[player_id]
                responses.append({"type" : "position" ,"id" : player_id , "x" : value['x'] , "y" : value['y']})

        if request['type'] == "bomb":
            player_id = request['id']
            if player_id in self.player:
                value = self.player[player_id]
                self.bombs.append({"x" : value['x'] , "y" : value['y'],"time" : 2000, "range" : 1})
                responses.append({"type" : "bomb" ,"id" : player_id , "x" : value['x'] , "y" : value['y']})

        return responses
