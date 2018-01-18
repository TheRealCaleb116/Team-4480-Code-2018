var webSocket;

webSocket = new WebSocket("ws://localhost:8888/EventHandler")

Popouts = [];


webSocket.onmessage = function (e) {
    alert(e.data);
}


class Popout{
    
    constructor(Key,ID){
        this.key = Key;
        this.id = ID;
        
    }
    
}