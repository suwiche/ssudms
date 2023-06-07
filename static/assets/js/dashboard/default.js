// greeting
var today = new Date()
var curHr = today.getHours()

/*
if (curHr >= 0 && curHr < 4) {
    document.getElementById("greeting").innerHTML = 'Good Night';
} else if (curHr >= 4 && curHr < 12) {
    document.getElementById("greeting").innerHTML = 'Good Morning';
} else if (curHr >= 12 && curHr < 16) {
    document.getElementById("greeting").innerHTML = 'Good Afternoon';
} else {
    document.getElementById("greeting").innerHTML = 'Good Evening';
}
*/
// time 
function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    // var s = today.getSeconds();
    var ampm = h >= 12 ? 'PM' : 'AM';
    h = h % 12;
    h = h ? h : 12;
    m = checkTime(m);
    // s = checkTime(s);
    document.getElementById('txt').innerHTML =
        h + ":" + m + ' ' + ampm;
    var t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) { i = "0" + i };  // add zero in front of numbers < 10
    return i;
}
