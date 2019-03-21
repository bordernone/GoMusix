$(document).ready(function(){
	$( '#changePasswordButton' ).on('click',function(){
		changePassword();
	});
	
	$('#accountSettingChangePasswordForm').submit(function(e){
		e.preventDefault();
		submitFormOnEnterChangePassword();
	});

	// for one-page navigation
	$( '#dashboardWrapper' ).on('click', '#changePasswordButton', function(){
		changePassword();
	});
	$('#dashboardWrapper').on('submit', '#accountSettingChangePasswordForm', function(e){
		e.preventDefault();
		submitFormOnEnterChangePassword();
	});
});
function changePassword(){
	// disabling elements
	var elementsId = ['newpassword', 'confirmnewpassword', 'changePasswordButton'];
	disableElements(elementsId);

	var newPassword = $('#newpassword').val();
	var confirmPassword = $('#confirmnewpassword').val();
	if (newPassword != confirmPassword){
		createCustomNotification('Passwords do not match', 'danger');
		enableElements(elementsId);
	} else {
		// make ajax request
		var csrftoken = getCookie('csrftoken');
		$.ajax({
			type:'POST',
			url:'/settings/changepassword/',
			data:{ 'newpassword' : newPassword, },
			beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    },
		    success: function(data){
		    	if (data == 'success'){
		    		createCustomNotification('Password changed', 'success');
		    	} else {
		    		enableElements(elementsId);
		    		createCustomNotification(data, 'danger');
		    	}
		    }
		});
	}
}

function submitFormOnEnterChangePassword(){
	document.getElementById('changePasswordButton').click();
}