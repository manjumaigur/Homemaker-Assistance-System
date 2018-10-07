var r = document.getElementById('result');

function startConverting () {
  if('webkitSpeechRecognition' in window){
    var speechRecognizer = new webkitSpeechRecognition();
    speechRecognizer.continuous = true;
    speechRecognizer.lang = 'en-IN';
    speechRecognizer.start();

    var finalTranscripts = '';

    speechRecognizer.onresult = function(event){
      var interimTranscripts = '';
      for(var i = event.resultIndex; i < event.results.length; i++){
        var transcript = event.results[i][0].transcript;
        transcript.replace("\n", "<br>");
        finalTranscripts = transcript;
      /*  if(event.results[i].isFinal){
          finalTranscripts += transcript;
        }else{
          interimTranscripts += transcript;
        }*/
      }
      //r.innerHTML = finalTranscripts + '<span style="color:#999">' + interimTranscripts + '</span>';
      console.log(finalTranscripts);
      finalTranscripts = finalTranscripts.toLowerCase();
      if (finalTranscripts == 'open mobile') {
        finalTranscripts = finalTranscripts.split(" ");
        redirectvoice(finalTranscripts[1]);
      }
      else if (finalTranscripts == 'open tv') {
        finalTranscripts = finalTranscripts.split(" ");
        redirectvoice(finalTranscripts[1]);
      }
      else if (finalTranscripts.startsWith('call')) {
        redirectvoice(finalTranscripts);
      }
      else if (finalTranscripts == 'message') {

      }
      else if (finalTranscripts == 'open contacts') {
        finalTranscripts = finalTranscripts.split(" ");
        redirectvoice(finalTranscripts[1]);
      }
      else if (finalTranscripts == 'create contact') {
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
          url: "http://localhost:8000/accounts/voice-recognizer/",
          data: jsondata,
          dataType: "json",
       }).done(function (data) {
          if (data.success) {
              window.location.href = data.url;
          }    
      });
      }