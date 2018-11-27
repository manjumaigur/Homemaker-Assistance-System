var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

function remoteOperations(remoteSlug) {

	function buttonClicked(btn) {
		var screenClass = document.getElementById("remote-typed");
		screenClass.innerHTML = btn;
		sendBtn(btn)
	}

	function sendBtn(button){
	  var jsondata = {
	    'button':button,
	    'remoteSlug':remoteSlug
	  }
	  $.ajax({
	    type: 'POST',
	    url: "http://localhost:8000/television/send-ir-code",
	    data: jsondata,
	    dataType: "json",
	    });
	}
}