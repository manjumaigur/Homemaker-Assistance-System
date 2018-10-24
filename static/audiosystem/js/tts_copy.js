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
      if ((finalTranscripts == 'open home') || (finalTranscripts == 'home') || (finalTranscripts == 'go to home') || (finalTranscripts == 'go home') || (finalTranscripts == 'open homepage') || (finalTranscripts == 'homepage') || (finalTranscripts == 'go to homepage') || (finalTranscripts == 'go homepage')) {
        finalTranscripts = "home";
        redirectvoice(finalTranscripts);
      }
      else if ((finalTranscripts == "back") || (finalTranscripts== "go back")) {
        window.history.go(-1);
      }
      else if (finalTranscripts == 'open mobile') {
        finalTranscripts = finalTranscripts.split(" ");
        redirectvoice(finalTranscripts[1]);
      }
      else if ((finalTranscripts == 'open tv') || (finalTranscripts == 'open television')) {
        finalTranscripts = finalTranscripts.split(" ");
        redirectvoice(finalTranscripts[1]);
      }
      else if (finalTranscripts.startsWith('call')) {
        redirectvoice(finalTranscripts);
      }
      else if (finalTranscripts.startsWith('message')) {
        redirectvoice(finalTranscripts);
      }
      else if ((finalTranscripts == 'contacts') || (finalTranscripts == 'open contacts') || (finalTranscripts == 'show contacts') || (finalTranscripts == 'open contact') || (finalTranscripts == 'show contact')) {
        finalTranscripts = "contacts";
        redirectvoice(finalTranscripts);
      }
      else if ((finalTranscripts.includes("open")||finalTranscripts.includes("show")) && (finalTranscripts.includes("contacts")||finalTranscripts.includes("contact"))) {
        finalTranscripts = finalTranscripts.split(" ");
        for(var i=0;i<finalTranscripts.length;i++) {
          if((finalTranscripts[i]!="open")&&(finalTranscripts[i]!="show")&&(finalTranscripts[i]!="contact")&&(finalTranscripts[i]!="contacts")) {
            console.log(finalTranscripts[i]);
            redirectvoice("open " + "contact " + finalTranscripts[i]);
            break;
          }
        }
      }
      else if ((finalTranscripts == 'create contact') || (finalTranscripts == 'add contact')) {
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
      });
      }