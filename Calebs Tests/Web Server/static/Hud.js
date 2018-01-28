$(document).read(function(){
    
    NetworkTables.addWsConnectionListener(function(connected){
        console.log("Connected to websocket");
    },true);
    },true);
    
    
    
});
