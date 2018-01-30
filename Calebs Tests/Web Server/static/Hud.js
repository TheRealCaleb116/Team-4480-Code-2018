
$(document).ready(function(){
    
    NetworkTables.addWsConnectionListener(function(connected){
        console.log("Connected to websocket. DATA: " + connected);
    },true);
    
    NetworkTables.addRobotConnectionListener(function(connected){
       console.log("Robot Has connected to networktables. Data sent: " + connected); 
    },true);
    
    
    /*Global NT Listener*/
    NetworkTables.addGlobalListener(function(key,value, isNew){
        if (key == "Alliance"){
        console.log("Global Listener Call");
            UpdateValue(value,"allianceValue");
        }

        
        
    },true);
    
    
    
    function UpdateValue(value, ID){
        
        document.getElementById(ID).innerHTML = value;
    }
    
    

    
    
});
