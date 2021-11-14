def load_area(filename):
    with open(filename) as file:
        area = []
        player = []
        goodies = []

        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for y in range(len(lines)):            
            row = ""
            line = lines[y]
            for x in range(len(line)):
                c = line[x]
                if '1' <= c and c <= '9': 
                    #player position
                    player.append({ 
                        "key" : c , 
                        "position" : {
                            "x" : x,
                            "y" : y
                        }
                    })
                    c = '.'
                if 'A' <= c and c <= 'Z': 
                    #bomb goody
                    goodies.append({ 
                        "key" : c , 
                        "position" : {
                            "x" : x,
                            "y" : y
                        }
                    })
                    c = '#'
                row += c
            area.append(row)
        return area , sorted(player, key=lambda d: d['key'])  , goodies  
