$(document).ready(function(){
	var musicPlayer = document.getElementById('musicPlayer'); // the sticky music player
	var offset = getPositionFromTop(musicPlayer) + $('#musicPlayer').height()+15;
	var offsetRight = ($(window).width() - ($('#musicPlayer').offset().left + $('#musicPlayer').outerWidth()));

	// instantiating music player
	mainAudioPlayer = new Plyr('#mainAudioPlayer audio', {
		controls: ['play', 'progress',],
	});

	// volume change
	mainAudioPlayerVolume = $('#mainAudioPlayerVolume');
	mainAudioPlayerVolume.slider({
		orientation: "horizontal",
		range: "min",
		max: 1,
		value: mainAudioPlayer.volume,
		step:0.1,
		slide: refreshVolumeSlider,
		change: refreshVolumeSlider,
	});


	// music player position update
	$(window).on('resize', function(){
		offset = getPositionFromTop(musicPlayer) + $('#musicPlayer').height()+15;
		offsetRight = ($(window).width() - ($('#musicPlayer').offset().left + $('#musicPlayer').outerWidth()));
	});

	$(window).on('scroll', function(){
		makeSticky(offset, offsetRight);
	});

	// upload songs
	$('#songsInputField').change(function(){
		uploadSongs();
	});

	// when different cat is selected
	$('#dashboardWrapper').on('change','#sortbylist',function(e){
		updatePseudoItem(this);
	});
});

var uploading = false;
var mainAudioPlayer;
var mainAudioPlayerVolume;
var currentCategory;

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
  	$('#mainAudioPlayer .plyr').focus();
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
			$('#allSongsCatTitle').html('Recently Added');
			$('#sortbylist').val('0');
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
	  	var selectedCat = $('#sortbylist').val();
		var sortbyval;
		if (selectedCat == '0'){
			sortbyval = 'sn';
		} else if (selectedCat == '1') {
			sortbyval = 'popularity';
		} else if (selectedCat == '2') {
			sortbyval = 'alphabetically';
		}
		var url = '/dashboard/?sort=' + sortbyval;
		$('#musicsWrapper').load(url + ' #musicsWrapper div', function(response, status){
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
	$('#dashboardWrapper .row .col-sm-8').load('/settings/ #accountSettingWrapper', function(response, status, xhr){
		if (status=='success'){
			NProgress.done();
		}
	});
}

function navigateToMyMusics(e){
	e.preventDefault();
	NProgress.start();
	$('#dashboardWrapper .row .col-sm-8').load('/dashboard/ #dashboardWrapper .allMusicsHere',  function(response, status, xhr){
		if (status=='success'){
		  	NProgress.done();
		}
	});
}

function refreshVolumeSlider(){
  	mainAudioPlayer.volume = mainAudioPlayerVolume.slider("value");
}

function deleteIconClick(event){
	event.stopPropagation();
	$('#deleteConfirmationModal').modal('toggle');
}

function updatePseudoItem(_this){
	var value = $(_this).val();
	var cat;
	var sortbyval;
	if (value == '0'){
		cat = 'Recently Added';
		sortbyval = 'sn';
	} else if (value == '1') {
		cat = 'Most Played';
		sortbyval = 'popularity';
	} else if (value == '2') {
		cat = 'Alphabetically';
		sortbyval = 'alphabetically';
	}
	$('#allSongsCatTitle').html(cat);
	sortby(sortbyval);
}

function sortby(value){
	NProgress.start();
	var url = '/dashboard/?sort=' + value;
	$('#dashboardWrapper .row .col-sm-8 #musicsWrapper').load(url+' #musicsWrapper div',  function(response, status, xhr){
		if (status=='success'){
		  	NProgress.done();
		}
	});
}