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
function check_incoming_call(){
  $.ajax({
    type: 'GET',
    url: "http://localhost:8000/mobile/check_incoming_call/",
    }).done(function (data) {
      if (data.call_coming) {
        incoming_call();
      }   
      else {
        check_incoming_call();
      }
  });
}

var modal = document.getElementById('callModal');

function incoming_call() {
    modal.style.display = "block";
}