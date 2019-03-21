$(document).ready(function(){
	pseudoPlayer = $('.customMediaPlayer');
	dataSrc = pseudoPlayer.attr("data-music-src");
	player = document.getElementById('musicPlayerHtmlMain');
	pseudoPlayerButton = $('#musicPlayerIcon');
	pseudoProgressIndicator = $('.customMediaPlayer .progressPercent');
	pseudoVolumeSlider = $('.musicPlayerVolumeManager .musicPlayerVolumeSlider');

	$('.musicPlayerVolumeWrapper').click(function(event){
		var volume = sliderPercent(event, this);
		changeVolume(volume);
	});
	$('.customMediaPlayer .playerProgress').click(function(event){
		var newProgress =sliderPercent(event, this);
		changeProgress(newProgress);
	});
	player.onended = function(){musicEnded();};
	player.onvolumechange = function(){updateVolumeSlider();};
	updateVolumeSlider();
	updateProgressBar();
});

var pseudoPlayer;
var dataSrc;
var player;
var pseudoPlayerButton;
var pseudoProgressIndicator;
var pseudoElementSlider;

function playButtonToggle(){
	dataSrc = pseudoPlayer.attr("data-music-src");
	if (player.paused){
		musicPlayerPlay(dataSrc);
	} else {
		musicPlayerPause();
	}
}
function musicPlayerPlay(dataSrc){
	$(pseudoPlayerButton).html('&#xf04c;');
	if (player.getAttribute('src') != dataSrc){
		player.src = dataSrc;
		player.load();
	} else if (player.ended){
		player.load();
	}
	player.play();
}
function musicPlayerPause(){
	$(pseudoPlayerButton).html('&#xf04b;');
	player.pause();
}
function setDataSrc(dataSrc){
	pseudoPlayer.attr('data-music-src', dataSrc);
}
function musicPlayerRunProgress(event){
	var percent = getPlayerPercentComplete(event);
	$(pseudoProgressIndicator).css('width', percent+'%');
}
function getPlayerPercentComplete(event){
	var currentTime = event.currentTime;
	var totalTime = event.duration;
	return ((currentTime/totalTime)*100);
}
function detectPositionXInDiv(event, element){
	var offset = $(element).offset().left;
	var pageX = event.pageX;
    return pageX - offset;
}
function sliderPercent(event, element){
	var elWidth = $(element).width();
	var position = detectPositionXInDiv(event, element);
	return (parseInt((position/elWidth)*100));
}
function changeVolume(volume){
	$(pseudoVolumeSlider).css('width', volume+'%');
	player.volume = volume/100;
}
function getVolume(element){
	return $(element).width();
}
function musicEnded(){
	$(pseudoPlayerButton).html('&#xf04b;');
}
function updateVolumeSlider(){
	var volume = player.volume * 100;
	$(pseudoVolumeSlider).css('width', volume+'%');
}
function changeProgress(progress){
	$(pseudoProgressIndicator).css('width', progress+'%');
	var seconds = getDurationFromPercent(progress);
	player.currentTime = seconds;
}
function getDurationFromPercent(percent){
	var duration = player.duration;
	var actualSec = (percent/100)*duration;
	return actualSec;
}
function updateProgressBar(){
	var currentTime = player.currentTime;
	var duration = player.duration;
	var currentTimePercent = (currentTime/duration) * 100;
	pseudoProgressIndicator.css('width', currentTimePercent+'%');
}