var r = document.getElementById('result');

var confirmDeletebtn = document.getElementById('confirmDeletebtn');
var cancelDeleteOperation = document.getElementById('cancelDeleteOperation');

function confirmDelete() {
  if('webkitSpeechRecognition' in window){
    var speechRecognizer = new webkitSpeechRecognition();
    speechRecognizer.continuous = true;
    speechRecognizer.lang = 'en-IN';
    speechRecognizer.start();

    var finalTranscripts = '';

    speechRecognizer.onresult = function(event){
      for(var i = event.resultIndex; i < event.results.length; i++){
        var transcript = event.results[i][0].transcript;
        transcript.replace("\n", "<br>");
        finalTranscripts = transcript;
      }

      console.log(finalTranscripts);

      finalTranscripts = finalTranscripts.toLowerCase();

      if ((finalTranscripts == "back") || (finalTranscripts== "go back")) {
        window.history.go(-1);
      }
      else if (finalTranscripts.startsWith("delete") || finalTranscripts.startsWith("remove")) {
        deleteBtn.click();
      }
      else if (finalTranscripts.startsWith("yes") || finalTranscripts.startsWith("sure") || finalTranscripts.startsWith("ok")) {
        confirmDeletebtn.click();
      }
      else if (finalTranscripts.startsWith("no") || finalTranscripts.startsWith("cancel") || finalTranscripts.startsWith("don't delete") || finalTranscripts.startsWith("not") || finalTranscripts.startsWith("do not")) {
        cancelDeleteOperation.click();
      }
      else {
        confirmDelete()
      }
    };
    speechRecognizer.onerror = function (event) {
    };
  }
  else {
    r.innerHTML = 'Your browser is not supported. If google chrome, please upgrade!';
  }
}

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
function redirectvoice(target){
  var jsondata = {
    'target':target
  }
  $.ajax({
    type: 'POST',
    url: "http://localhost:8000/audiosystem/voice-recognizer/",
    data: jsondata,
    dataType: "json",
    }).done(function (data) {
      if (data.success) {
        window.location.href = data.url;
      }   
      else {
        window.location.reload()
      }
  });
}