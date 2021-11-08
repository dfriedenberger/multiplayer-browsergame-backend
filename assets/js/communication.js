

function Communicator(config) {

    this._config = config;
    this.wsurl = (window.location.protocol.startsWith("https") ? "wss://" : "ws://") + window.location.host;

    this.ws = new WebSocket(this.wsurl + "/ws/"+this._config.game+"/"+this._config.game_id);

    var _communicator = this;
    this.ws.onmessage = function(message) {
        _communicator._config.callback(JSON.parse(message.data));
    }

    this.send = function(data) {
        console.log("ws",this.ws.readyState)
        if (this.ws.readyState === 1) {
            this.ws.send(JSON.stringify(data))
        } else {
            var that = this;
            setTimeout(function () {
                that.send(data);
            }, 100);
        }
    }


  
}