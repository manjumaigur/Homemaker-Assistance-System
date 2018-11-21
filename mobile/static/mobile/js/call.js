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
        incoming_call(data.contact_in_phonebook,data.contact_number,data.contact_name,data.contact_photo);
      }   
      else {
        check_incoming_call();
      }
  });
}

var modal = document.getElementById('callModal');
var userPic = document.getElementById('userPic');
var username = document.getElementById('user-name');
var declineBtn = document.getElementById('declineBtn');
var acceptBtn = document.getElementById('acceptBtn');
var abortBtn = document.getElementById('abortBtn');

function incoming_call(flag,number,name,photo) {
    modal.style.display = "block";
    abortBtn.style.display = "none";
    if (flag) {
      userPic.src = "http:localhost"+photo;
      username.innerHTML= name+": "+number;
    }
    else {
      userPic.src = "http://localhost:8000/media/default_avatar.png";
      username.innerHTML = number;
    }
    check_call_connection();
    $('#declineBtn').on('click', function(e) {
      abort_call();
      return e.preventDefault();
    });

    $('#abortBtn').on('click', function(e) {
      abort_call();
      return e.preventDefault();
    });

    $('#acceptBtn').on('click', function(e) {
      $('.call').toggleClass('is-accepted');
      receive_call();
      return e.preventDefault();
    });
    function receive_call(){
      $.ajax({
        type: 'GET',
        url: "http://localhost:8000/mobile/receive_call/",
        }).done(function (data) {
          if (data.success) {
            declineBtn.style.display = "none";
            acceptBtn.style.display = "none";
            abortBtn.style.display = "block";
            check_call_connection();
          }
          else {
            modal.style.display = "none";
            check_incoming_call();
          }
      });
    }

    function abort_call(){
      $.ajax({
        type: 'GET',
        url: "http://localhost:8000/mobile/abort_call/",
        }).done(function (data) {
          if (data.success) {
            modal.style.display = "none";
            abortBtn.style.display = "none";
            check_incoming_call();
          }
          else {
            check_incoming_call();
          }
      });
    }
    function check_call_connection(){
      $.ajax({
        type: 'GET',
        url: "http://localhost:8000/mobile/check_call_connection/",
        }).done(function (data) {
          if (data.connected) {
            check_call_connection(); 
          }
          else {
            modal.style.display = "none";
            abortBtn.style.display = "none";
            check_incoming_call();
          }
      });
    }
}
