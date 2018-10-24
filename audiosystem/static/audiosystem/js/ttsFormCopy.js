
var submitBtn = document.getElementById('submitBtn')

function startConvertingFormData () {
  if('webkitSpeechRecognition' in window){
    var speechRecognizer = new webkitSpeechRecognition();
    speechRecognizer.continuous = true;
    speechRecognizer.lang = 'en-IN';
    speechRecognizer.start();

    var finalTranscripts = '';
    var name="";
    var number="";
    var formFilled = false;

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
      else if (finalTranscripts.startsWith("name") || finalTranscripts.startsWith("number")) {
        finalTranscripts = finalTranscripts.split(" ");
        for (var i=0;i<finalTranscripts.length;i++) {
          if (finalTranscripts[i]=="name") {
            if(finalTranscripts[i+1]!='is') {
              name=finalTranscripts[i+1];
              i++;
              continue;
            }
            else {
              name=finalTranscripts[i+2];
              i=i+2;
              continue;
            }
          }
          else if(finalTranscripts[i]=="number") {
            if(finalTranscripts[i+1]!='is') {
              number=finalTranscripts[i+1];
              i++;
              continue;
            }
            else {
              number=finalTranscripts[i+2];
              i=i+2;
              continue;
            }
          }
        }
      else if (finalTranscripts.startsWith("number")) {
        finalTranscripts = finalTranscripts.split(" ");
        if (finalTranscripts[1]=="is") {
          number=finalTranscripts[2];
        }
      }
        console.log(name+number);
        var ipname = document.getElementById("id_name");
        var ipnumber = document.getElementById("id_phone_number");
        ipname.value = name;
        ipnumber.value = number;
        submitBtn.click();
      }
      else {
        redirectvoice(finalTranscripts);
      }
    };
    speechRecognizer.onerror = function (event) {
    };
  }else{
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