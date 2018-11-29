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
function check_incoming_call_sms(){
  $.ajax({
    type: 'GET',
    url: "http://localhost:8000/mobile/check-incoming-call-sms/",
    }).done(function (data) {
      if (data.call_coming) {
        incoming_call(data.contact_in_phonebook,data.contact_number,data.contact_name,data.contact_photo);
      }   
      else if (data.message_coming) {
        incoming_sms(data.contact_in_phonebook,data.contact_number,data.contact_name,data.smsSlug)
      }
      else {
        check_incoming_call_sms();
      }
  });
}

var callModal = document.getElementById('callModal');
var smsModal = document.getElementById('smsModal');
var userPic = document.getElementById('userPic');
var username = document.getElementById('user-name');
var declineBtn = document.getElementById('declineBtn');
var acceptBtn = document.getElementById('acceptBtn');
var abortBtn = document.getElementById('abortBtn');
var sms_from = document.getElementById('sms_from');
var closeSMSbtn = document.getElementById('closeSMSbtn');
var chatroom_url = document.getElementById('chatroom_url');
var modal = document.getElementById('myModal');
var phoneNumber='';
smsModal.style.display="none";


function buttonClicked(btn) {
  var screenClass = document.getElementById("keyboard-typed");
  if(btn=="clear") {
    phoneNumber=phoneNumber.slice(0, phoneNumber.length-1);
  }
  else{
    phoneNumber+=btn;
    console.log(phoneNumber);
  }
  if (phoneNumber.length<=10) {
    screenClass.innerHTML = phoneNumber;
  }
}

function make_call() {
  console.log(phoneNumber);
  make_call_number(phoneNumber);
}

function make_call_number(phone_number) {
  console.log(phone_number);
  var jsondata = {
    'phone_number': phone_number
  }
   $.ajax({
    type: 'POST',
    url: "http://localhost:8000/mobile/make-call/",
    data: jsondata,
    dataType: "json",
    }).done(function (data) {
      if (data.call_going) {
        modal.style.display = "none";
        outgoing_call(data.contact_in_phonebook,data.contact_number,data.contact_name,data.contact_photo)
      }   
      else {
        window.location.reload()
      }
  });   
}

function incoming_call(flag,number,name,photo) {
    callModal.style.display = "block";
    declineBtn.style.display = "block";
    acceptBtn.style.display = "block";
    abortBtn.style.display = "none";
    if (flag) {
      userPic.src = "http://localhost:8000"+photo;
      username.innerHTML= name+": "+number;
    }
    else {
      userPic.src = "media/default_avatar.png";
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
}

function outgoing_call(flag,number,name,photo) {
  $('.call').toggleClass('is-accepted');
    callModal.style.display = "block";
    abortBtn.style.display = "block";
    declineBtn.style.display = "none";
    acceptBtn.style.display = "none";
    if (flag) {
      userPic.src = "http://localhost:8000"+photo;
      username.innerHTML= name+": "+number;
    }
    else {
      userPic.src = "media/default_avatar.png";
      username.innerHTML = number;
    }
    check_call_connection();

    $('#abortBtn').on('click', function(e) {
      abort_call();
      return e.preventDefault();
    });
}

function receive_call(){
  
  callModal.style.display = "block";
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
            callModal.style.display = "none";
            check_incoming_call_sms();
          }
      });
    }

  function abort_call(){
      $.ajax({
        type: 'GET',
        url: "http://localhost:8000/mobile/abort_call/",
        }).done(function (data) {
          if (data.success) {
            callModal.style.display = "none";
            abortBtn.style.display = "none";
            check_incoming_call_sms();
          }
          else {
            check_incoming_call_sms();
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
            callModal.style.display = "none";
            abortBtn.style.display = "none";
            check_incoming_call_sms();
          }
      });
    }

function incoming_sms(flag,number,name,slug) {
  smsModal.style.display = "block";
  if (flag) {
    sms_from.innerHTML = name + "::" +number;
    chatroom_url.href="http://localhost:8000/mobile/message/"+slug+"/"
  }
  else {
    sms_from.innerHTML = number
    chatroom_url.href="http://localhost:8000/mobile/message/"+slug+"/"
  }
}

closeSMSbtn.onclick = function() {
    smsModal.style.display = "none";
    check_incoming_call_sms();
}

$('#sendSMS').on('submit', function(event){
    event.preventDefault();
    sendSMS();
});

function sendSMS(){
  var textData = document.getElementById("id_text");
  var phone_number = document.getElementById("contact_number");
  textData = textData.value;
  phone_number = phone_number.innerHTML;
  var jsondata = {
    'text':textData,
    'phone_number': phone_number
  }
  console.log(jsondata)
  $.ajax({
    type: 'POST',
    url: "http://localhost:8000/mobile/send_sms/",
    data: jsondata,
    dataType: "json",
    }).done(function (data) {
      if (data.success) {
        window.location.reload()
      }   
      else {
        window.location.reload()
      }
  });
}

