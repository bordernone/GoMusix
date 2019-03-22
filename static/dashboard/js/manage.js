$(document).ready(function(){
	var musicPlayer = document.getElementById('musicPlayer'); // the sticky music player
	var offset = getPositionFromTop(musicPlayer) + $('#musicPlayer').height()+15;
	var offsetRight = ($(window).width() - ($('#musicPlayer').offset().left + $('#musicPlayer').outerWidth()));


  mainAudioPlayer = new Plyr('#mainAudioPlayer audio', {
    controls: ['play', 'progress',],
  });
  mainAudioPlayer.volume = 1;

	$(window).on('scroll', function(){
		makeSticky(offset, offsetRight);
	});

  // upload songs
  $('#songsInputField').change(function(){
    uploadSongs();
  });
});

var uploading = false;
var mainAudioPlayer;

function getPositionFromTop(element) {
  var yPosition = 0;
  while(element) {
      yPosition += (element.offsetTop - element.scrollTop + element.clientTop);
      element = element.offsetParent;
  }
  return yPosition;
}
function getWindowSize() {
  var myWidth = 0, myHeight = 0;
  if( typeof( window.innerWidth ) == 'number' ) {
    //Non-IE
    myWidth = window.innerWidth;
    myHeight = window.innerHeight;
  } else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
    //IE 6+ in 'standards compliant mode'
    myWidth = document.documentElement.clientWidth;
    myHeight = document.documentElement.clientHeight;
  } else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
    //IE 4 compatible
    myWidth = document.body.clientWidth;
    myHeight = document.body.clientHeight;
  }
  return myHeight;
}
function makeSticky(offset, offsetRight){
	var musicPlayer = $('#musicPlayer');
	if (window.pageYOffset + getWindowSize() >= offset){
		musicPlayer.addClass('sticky');
		musicPlayer.css('right',offsetRight);
    $('#actionsWrapper').css('padding-bottom','400px');
	} else {
		musicPlayer.removeClass('sticky');
		musicPlayer.css('right','none');
    $('#actionsWrapper').css('padding-bottom','0px');
	}
}

function playThisSong(sn){
  $('#musicPlayer .albumImg img').attr('src', 'thumbnail/'+sn+'/');
  mainAudioPlayer.source = {
                            type: 'audio',
                            title: 'GoMusix',
                            sources: [
                                {
                                    src: 'play/'+sn,
                                    type: 'audio/mp3',
                                },
                            ],
                        };
  mainAudioPlayer.play();
}

function uploadSongs(){
  // starting the progressbar
  NProgress.set(0.0);

  hideNotificationPanel();
  var songs = document.getElementById('songsInputField').files;
  var csrftoken = getCookie('csrftoken');
  var form_data = new FormData();
  var len = songs.length;
  for (i=0; i < len; i++){
    form_data.append('file', songs[i]);
  }
  $.ajax({
    xhr: function() {
      var xhr = new window.XMLHttpRequest();
      xhr.upload.addEventListener("progress", function(evt) {
          if (evt.lengthComputable) {
            var percentComplete = evt.loaded / evt.total;
            NProgress.set(percentComplete);
          }
        }, false);
      return xhr;
    },
    url: "upload/",
    type: "POST",
    data: form_data,
    processData: false,
    contentType: false,
    async: true,
    enctype: 'multipart/form-data',
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    success: function(res) {
      $('#musicsWrapper').load('/dashboard/ #musicsWrapper div');
      if (res != ''){
        createCustomNotification(res, 'danger');
      } else {
        createCustomNotification('Upload successful', 'success');
      }
    },       
    error: function(res) {
      createCustomNotification(res, 'danger');
    }       
  });
}

function deleteThisSong(event,sn){
  event.stopPropagation();
  var csrftoken = getCookie('csrftoken');

  // running the progressbar
  NProgress.start();
  $.ajax({
    xhr: function(){
      var xhr = new window.XMLHttpRequest();
      return xhr;
    },
    url: 'delete/',
    type: "POST",
    async:true,
    data: {sn:sn},
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    success: function(res) {
      if (res != 'success'){
        createCustomNotification(res, 'danger');
        // stopping progressbar
        NProgress.done();
      } else {
        $('#musicsWrapper').load('/dashboard/ #musicsWrapper div', function(response, status){
          // stopping progressbar
          NProgress.done();

          // displaying message
          createCustomNotification('Deletion successful', 'success');
        });
      }
    },
  });
}

function navigateToSettings(e){
  e.preventDefault();
  NProgress.start();
  $('#musicsWrapper').load('/settings/ #accountSettingWrapper', function(response, status, xhr){
    if (status=='success'){
      NProgress.done();
    }
  });
}

function navigateToMyMusics(e){
  e.preventDefault();
  NProgress.start();
  $('#musicsWrapper').load('/dashboard/ #musicsWrapper div',  function(response, status, xhr){
    if (status=='success'){
      NProgress.done();
    }
  });
}