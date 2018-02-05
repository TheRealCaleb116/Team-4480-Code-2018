var webSocket;

webSocket = new WebSocket("ws://localhost:8888/EventHandler");

Popouts = [];


webSocket.onmessage = function (e) {
    console.log("we got msgs: " + e);
    msg = e.split(":");
    
    for (i=0;i< Popouts.size();i++){
        
        if (Popouts[i].key == msg[0]){
            Popouts[i].fire(msg[1]);
        }
    }
}


function createPopup(Key,ID){
    temp = new Popout(Key,ID);
    Popouts.push(temp);
}

class Popout{
    
    constructor(Key,ID){
        this.key = Key;
        this.id = ID;
        
        this.state = false;
        
    }
    
    fire(value){
        if (value == "True"){
            this.state = false;
            alert("Toggle off for " + this.key);
            
        }else if (value == "False"){
            this.state = true;
            alert("Toggle on for " + this.key);
            
        }
        
    }
    
    animation(){
//        $(this.id).animate({
//            left: 0;
//        },
//        "slow"
//        )
    }
/*    Getters and Setters
    get id(){
        return this.id;
    }
    get key(){
        return this.key;
    }
    set key(val){
        this.key = val;
    }
    set id(val){
        this.id = val;
    }*/
    
}



/*Calls for the individual webpage*/
createPopup("GamePeriod","RandomId");