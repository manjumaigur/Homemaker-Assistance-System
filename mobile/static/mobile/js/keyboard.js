var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById("keyboardBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
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

var phoneNumber='';

function buttonClicked(btn) {
	var screenClass = document.getElementById("keyboard-typed");
	if(btn=="clear") {
		phoneNumber=phoneNumber.slice(0, phoneNumber.length-1);
	}
	else{
		phoneNumber+=btn;
	}
	if (phoneNumber.length<=10) {
		screenClass.innerHTML = phoneNumber;
	}
}