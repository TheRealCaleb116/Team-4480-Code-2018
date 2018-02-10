
//====================================
//======= API STARTS BELOW ===========
//====================================

//Open web socket to server
var webSocket;
webSocket = new WebSocket("ws://localhost:8888/EventHandler");

//List of instanciated popouts
Popouts = new Array();


//Gets parses and passes msgs from the server
webSocket.onmessage = function (e) {
    var msg = e.data;
    var msg = msg.split(":");
    
    for (var i=0;i< Popouts.length;i++){
        
        if (Popouts[i].key == msg[0]){
            Popouts[i].fire(msg[1]);
        }
    }
}

//Api method to create a popup
function createPopup(Key,ID){
    temp = new Popout(Key,ID);
    Popouts.push(temp);
}


//The class that represents a popout
class Popout{
    
    constructor(Key,ID){
        this.key = Key;
        this.id = ID;
        
        this.index =0;
        
        this.element = document.getElementById(this.id);
        
        this.height = $("#"+this.id).outerHeight();
        
        this.state = false;
        
        Popout.down = Array(5);
    }
    
    fire(value){        
        if (value == "True" && this.state == false ){
            this.state = true;
            
            this.slideOut();    
        }
        else if (value == "False" && this.state == true){
            this.state = false;
            
            this.slideIn();            
        }
    }
    
    slideIn(){

        
        //Animate slide out
        $("#"+this.id).animate({right: '-350px'},500);
        
        //Remove itself from array
        this.removeFSlot();

    }
    slideOut(){
        //Get index of popout
        this.index = this.putFSlot();
        
        //get how far from the top we should slide out by counting the height of popouts above
        var topValue = 50;
        for (var i = 0; i < this.index ;i++){
            topValue = topValue + Popout.down[i].height + 10;
        }
        
        //set height 
        $("#"+this.id).css("top", topValue + "px" );
        
        
        //Slides the popout Out
        $("#"+this.id).animate({right: '0px'},500);
    }
    
    putFSlot(){
        for (var i=0; i< Popout.down.length; i++){            
            if (Popout.down[i] == null){
                Popout.down[i] = this;
                return (i);
            }
        }
        
        alert("To many popups trying to pop up. If i ever see this then i need to add a queue system");
        
    }
    removeFSlot(){
        Popout.down[this.index] = null;
        
    }
}



//Utility method to force a call to the fire method of a popout
//This is in here for testing purposes
//function trigger(num,msg){
//    Popouts[num].fire(msg);
//}

//===========================================
//======          Api Ends         ==========
//===========================================

//These are the calls to the actual API


createPopup("AutonomousPopup","autoPopup");






