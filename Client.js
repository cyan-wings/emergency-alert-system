// connects socket.io to local host
var socket = io.connect('http://' + document.domain + ':' + location.port);

// gets the id from client.html
var EmergencyStatus = document.getElementById("status");
var SafeStatus = document.getElementById("safe");
var AlarmStatus = document.getElementById("alarm");

// Get the modal id from client.html
var modal = document.getElementById('myModal');
var ModalStatus = document.getElementById("modal_status");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


// gets data from server to change the emergency status (fire, robbery, no emergency)
socket.on('event', function(data) {
    if (data == "Fire") {
        EmergencyStatus.innerHTML = data.fontcolor("red");
    }
    else if (data == "Robbery") {
        EmergencyStatus.innerHTML = data.fontcolor("orange");
    }

    else {
        EmergencyStatus.innerHTML = data;
    }
    modal.style.display = "block";  //displays the modal when the emergency status changes
    ModalStatus.innerHTML = data;
});

// gets data from server to change the status of the safe (Locked, Unlocked)
socket.on('safe_status',function(data){
    SafeStatus.innerHTML = data;
});

// gets data from the server to change the status of the alarm (Enabled, Disabled)
socket.on('alarm_status', function(data){
    AlarmStatus.innerHTML = data;
});

// when "Lock Safe" button is clicked
// if safe is not locked, sends data to the server to lock the safe
// then pop-up appears to inform response team that the safe is locked
function lockSafe() {
    if (SafeStatus.innerHTML == "Locked") {
        alert("Safe is already locked.");
    }
    else {
        socket.emit('safe','lock');
        alert("Safe Locked.");
    }
}

// when "Unlock Safe" button is clicked
// if safe is locked, sends data to the server to unlock the safe
// then pop-up appears to inform response team that the safe is unlocked
function unlockSafe() {
    if (SafeStatus.innerHTML == "Unlocked") {
        alert("Safe is already unlocked.");
    }
    else {
        socket.emit('safe','unlock');
        alert("Safe Unlocked.");
    }   
}

// when "Enable Alarm" button is clicked
// if alarm is disabled, sends data to the server to enable the alarm
// then pop-up appears to inform response team that the alarm is enabled
function enableAlarm() {
    if (AlarmStatus.innerHTML == "Disabled") {
		socket.emit('alarm','enable');
        alert("Alarm Enabled.");
	}
	else {
		alert("Alarm is already enabled. Please disable the alarm first before enabling it again.");
    }   
}

// when "Disable Alarm" button is clicked
// if alarm is enabled, sends data to the server to disable the alarm
// then pop-up appears to inform response team that the alarm is disabled
function disableAlarm() {
    if (AlarmStatus.innerHTML == "Disabled") {
        alert("Alarm is already disabled.");
    }
    else {
        socket.emit('alarm','disable');
        alert("Alarm Disabled.");
    }
}

// when "Call Police" button is clicked
// pop-up appears to inform response team that the police has been called
function callPolice() {
    alert("Called the police!");
}

// when "Call Firefighter" button is clicked
// pop-up appears to inform response team that the firefighters have been called
function callFirefighter() {
    alert("Called the firefighters!");
}

// when "reset Status" button is clicked
// changes all the statuses to default
function resetStatus() {
    EmergencyStatus.innerHTML = "No Emergency";
    SafeStatus.innerHTML = "Unlocked";
    AlarmStatus.innerHTML = "Disabled";
    socket.emit('alarm','disable');
	socket.emit('safe','unlock');
    alert("All statuses have been reset.");
}

// when "enable alarm with duration" button is clicked
// if alarm is disabled, sends data to the server to enable the alarm and also the duration of the alarm
// countdown timer will appear at the "Status of Alarm" to show the duration left for alarm ring
function enableAlarmDuration() {
    if (AlarmStatus.innerHTML == "Disabled") {
        var AlarmDuration = document.getElementById("textbox").value;

        if ((AlarmDuration > 0) && (AlarmDuration <= 86400)) {

            socket.emit('duration',{'status':'enable', 'timer': AlarmDuration});
            
            var intervalID = setInterval(function() {
                if (AlarmStatus.innerHTML!="Stop") {
                    if (AlarmDuration > 0){
                        if (AlarmDuration == 1) {
                            AlarmStatus.innerHTML = AlarmDuration + " second left until the alarm stops ringing";
                            AlarmDuration --;
                        }
                        else {
                            AlarmStatus.innerHTML = AlarmDuration + " seconds left until the alarm stops ringing";
                            AlarmDuration --;
                        }
                        
                    }
                }
                else {

                    clearInterval(intervalID);
                    AlarmStatus.innerHTML = "Disabled";
                    return;
                    }  
                },1000);
        }
        else {
            alert("Alarm duration has to be in between 1 and 86400 seconds.");
        }
    }


    else {
		alert("Alarm is already enabled. Please disable the alarm first before enabling it again.");        
    }
    
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}