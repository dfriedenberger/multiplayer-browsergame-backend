function GameController(config) {
    this._config = config;
    this._state = {};


    this._set_pressed = function(targetId,pressed)
    {
        if(!(targetId in this._state))
        {
            this._state[targetId] = {
                pressed: false
            }
        }
        this._state[targetId].pressed = pressed;
    }

    this._update_moving = function(targetId,tmout)
    {
        that = this;
        if(that._state[targetId].pressed)
        {
            that._config.callback(targetId);

            setTimeout(function() {
                that._update_moving(targetId,100);
            },tmout)
        }
    }
    this._log = function(obj,id)
    {
        //console.log("event",obj,"id",id)
    }
    this._init_area = function(areaId)
    {
        var that = this;
        var obj = $('#'+ areaId);

        $(obj).bind('touchstart', function(e) {
    
            var l = e.touches.length;
            for(var i = 0;i< l;i++)
            {
              var t = e.touches[i];
              var id = $(t.target).attr('id');
              that._log("touchstart "+i + " "+id,t);
              if(id != undefined)
              {
                that._set_pressed(id,true);
                that._update_moving(id,500);
              }
            }
        });
        
        $(obj).bind('touchend', function(ev) {

            that._log("touchend",ev.originalEvent);
            var e = ev.originalEvent;
            var l = e.changedTouches.length;
            for(var i = 0;i< l;i++)
            {
              var t = e.changedTouches[i];
              var id = $(t.target).attr('id');

              that._log("touchstart "+i + " "+id,t);
              if(id != undefined)
              {
                that._set_pressed(id,false);
              }
            }
        });
       

    };


    //init
    $(document).bind("contextmenu", function(e) {
        return false;
    });

    let l = this._config.areas.length;
    for(let i = 0;i < l;i++)
    {
        this._init_area(this._config.areas[i]);
    }

   
 

}