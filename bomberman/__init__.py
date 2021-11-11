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
            print("cycle")

        if request['type'] == "position":
            print("position")
            responses.append(request)

        if request['type'] == "bomb":
            print("bomb")
            responses.append(request)


        return responses
