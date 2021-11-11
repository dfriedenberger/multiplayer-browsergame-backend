function Pattern(url) {

    this.imageloaded = false;
    this.img = new Image();
    var that = this;
    this.img.onload = function() {
       that.imageloaded = true;
    };
    this.img.src = url; 

    this.draw = function(context,x,y,icon_size) {
        if(this.imageloaded)
        {
            context.drawImage(this.img,x,y,icon_size,icon_size);          
        }
    }
}

function PlayingArea(canvas) {

    this.canvas = canvas;
    this.area = [];
    this.pattern = {};
    this.players = {};
    this.bombs = [];

    this.set_area = function(area) {
        this.area = area;
    }

    this.is_possible = function(x,y) {
        var r = that.area.length;
        if(0 <= y && y < r)
        {
            var c = that.area[0].length;
            if(0 <= x && x < c)
            {
                var p = that.area[y].charAt(x);
                return p == "."
            }
        }
        return false;
    }

    this.set_pattern = function(pattern) {
        this.pattern = pattern;
    }

    this.set_position = function(player,x,y) {
        this.players[player] = { x : x , y : y }
    }

    this.set_bomb = function(x,y) {
        this.bombs.push({
            x : x,
            y : y
        })
    }

    this.get_position = function(player) {
        return [ this.players[player].x , this.players[player].y ]
    }

  

    var that = this;
    this._draw = function()
    {
        var context = that.canvas.getContext("2d");
        //var boundings = this.canvas.getBoundingClientRect();

       
        context.fillStyle = "#EEEEEE";
        context.fillRect(0,0,canvas.width,canvas.height);//for white background

        var r = that.area.length;
        if(r > 0)
        {
            var c = that.area[0].length;
            var icon_size = parseInt(that.canvas.width / c); 
            var xoffset = (that.canvas.width - icon_size * c) / 2;
    
            for(var y = 0;y < r;y++)
            {
                for(var x = 0;x < c;x++)
                {
                    var p = that.area[y].charAt(x);
                    context.fillStyle= p == "#" ? "#FF0000" : "#00FF00"
                    if (p == "*")
                        context.fillStyle="#0000FF"
                    context.fillRect(xoffset + x * icon_size, y * icon_size, icon_size, icon_size);//for red border
                }
            } 


            var l = that.bombs.length;
            for(var i = 0;i < l;i++)
            {
                var pattern = that.pattern['bomb'];
                var pos = that.bombs[i]
                pattern.draw(context,xoffset + pos.x * icon_size,pos.y * icon_size,icon_size); 
            }

            for (let [key, value] of Object.entries(that.players)) {

                var pattern = that.pattern['player'];
                pattern.draw(context,xoffset + value.x * icon_size,value.y * icon_size,icon_size);

            }

        }


       

        requestAnimationFrame(that._draw);

    }
    that._draw();

}