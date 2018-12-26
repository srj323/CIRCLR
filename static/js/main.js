window.onload = function () { startstick() };

function startstick() {
    window.onscroll = function () { stickyfunc() };
    var navbar = document.getElementById("navbar");
    var navbarcont = document.getElementById("navbarcont");
    var sticky = navbarcont.offsetTop;

    function stickyfunc() {
        if (window.pageYOffset >= sticky-50) {
            navbar.classList.add('sticky');
        }
        else {
            navbar.classList.remove('sticky');
        }
    }
}
function updatetime(){
    var timez = (new Date()).getTimezoneOffset()/60;
    timez = -timez;
    var hrs = document.getElementsByClassName("hr");
    var mins = document.getElementsByClassName("min");
    var ams = document.getElementsByClassName("am/pm");
    var def = " a.m.";
    for (i = 0; i < hrs.length; i++){
        ams[i].innerHTML = def;
        hrs[i].innerHTML = parseInt(hrs[i].innerHTML.split(':', 1)) + parseInt(timez) + ':';
        m = timez - parseInt(timez);
        mins[i].innerHTML = parseInt(mins[i].innerHTML) + m*60;
        if (parseInt(hrs[i].innerHTML.split(':', 1)) > 12) {
            hrs[i].innerHTML = parseInt(hrs[i].innerHTML.split(':', 1)) - 12 + ':';
            ams[i].innerHTML = " p.m.";
        }
        if(parseInt(mins[i].innerHTML) > 60){
            mins[i].innerHTML = parseInt(mins[i].innerHTML)-60
            hrs[i].innerHTML = parseInt(hrs[i].innerHTML.split(':', 1)) + 1 + ':';
        }
        if(parseInt(mins[i].innerHTML) < 10){
            mins[i].innerHTML = "0" + mins[i].innerHTML;
        }
    }
}