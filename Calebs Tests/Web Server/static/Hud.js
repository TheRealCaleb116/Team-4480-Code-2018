$(document).ready(function () {
    attachSelectToSendableChooser("#AutonomousSelector", "/SmartDashboard/Autonomous Mode");
    
    NetworkTables.addWsConnectionListener(function (connected) {
        /*
                console.log("Connected to websocket. DATA: " + connected);
        */
    }, true);

    NetworkTables.addRobotConnectionListener(function (connected) {
        /*
               console.log("Robot Has connected to networktables. Data sent: " + connected); 
        */
    }, true);


    basePath = "/SmartDashboard/Data/";
    period = "Disabled";
    
    /*Global NT Listener*/
    NetworkTables.addGlobalListener(function (key, value, isNew) {
        /*
                console.log("Key Triggered ----  " + key);
        */
        

        if (key == basePath + "Alliance") {
            UpdateAlliance(value);

        } else if (key == basePath + "GamePeriod") {
            period = value;
            UpdateValue(value, "periodValue");

        } else if (key == basePath + "AproxMatchTime") {
            
            if (period == "Teleop"){
                num = value.toFixed(2);
                UpdateValue(num, "timerValue");
            }else{
                UpdateValue("Null", "timerValue");
            }
        }



    }, true);



    function UpdateValue(value, ID) {

        document.getElementById(ID).innerHTML = value;
    }

    function UpdateAlliance(value) {
        if (value == "Red") {

            document.getElementById("allianceValue").innerHTML = value;
            document.getElementById("team").style.backgroundColor = "Red";

        } else {

            document.getElementById("allianceValue").innerHTML = value;
            document.getElementById("team").style.backgroundColor = "Blue";
        }
    }




});
