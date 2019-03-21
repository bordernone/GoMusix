var notificationPanelWrapper = 'notificationWrapper';
var notificationPanel = 'notificationPanel';
var notificationBox = 'notificationPanelMessage';
function notificationDismiss() {
	$('#'+notificationPanelWrapper).hide('slow');
}
function createNotification(message){
	$('#'+notificationPanel).css('background-color', '#1c8adb');
	$('#'+notificationBox).html(message);
	showNotificationPanel();
}
function showNotificationPanel(){
	$('#'+notificationPanelWrapper).show();
}
function hideNotificationPanel(){
	$('#'+notificationPanelWrapper).hide();
}
function createCustomNotification(message, type){
	if (type == 'danger'){
		$('#'+notificationPanel).css('background-color', '#db1c1c');
		customNotificationMessage(message);
	} else if (type == 'info'){
		$('#'+notificationPanel).css('background-color', '#1c8adb');
		customNotificationMessage(message);
	} else if (type == 'success') {
		$('#'+notificationPanel).css('background-color', '#00ad51');
		customNotificationMessage(message);
	}
}
function customNotificationMessage(message){
	$('#'+notificationBox).html(message);
	showNotificationPanel()
}
