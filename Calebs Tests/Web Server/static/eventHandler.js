var webSocket;

webSocket = new WebSocket("ws://localhost:8888/EventHandler");

Popouts = [];


webSocket.onmessage = function (e) {
    alert(e.data);
}


class Popout{
    
    constructor(Key,ID){
        this.key = Key;
        this.id = ID;
        this.dur = 5.0;
        
    }
    
    fire(value=null,duration=5.0){
        this.dur = duration;
        
        
    }
    
    animation(){
//        $(this.id).animate({
//            left: 0;
//        },
//        "slow"
//        )
    }
    /*Getters and Setters*/
    get id(){
        return this.id;
    }
    get key(){
        return this.key;
    }
    
}