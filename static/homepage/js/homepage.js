$(document).ready(function(){
    $('#registrationPreForm').submit(function(event){
        event.preventDefault();
        submitFormOnEnterRegisterPre();
    });
    $('#registrationPostForm').submit(function(event){
        event.preventDefault();
        submitFormOnEnterRegisterPost();
    });
    $('#loginForm').submit(function(event){
        event.preventDefault();
        submitFormOnEnterLogin();
    });

	$('#registerButtonPre').click(function(){
		var emailAddress = $('#registerEmailInput').val();
		verifyEmail(emailAddress);
	});

	$('#registerButtonPost').click(function(){
		var emailAddress = $('#registerEmailInput').val();
		var password = $('#registerPasswordInput').val();
		var username = $('#registerUsernameInput').val();
		completeRegistration(username, emailAddress, password);
	});

	$('#loginButton').click(function(){
		var username = $('#loginUsernameInput').val();
		var password = $('#loginPasswordInput').val();
		login(username,password);
	});
});


function verifyEmail(emailAddress){
    hideNotificationPanel();
    
    // disable elements
    var elementsId = ['registerButtonPre', 'registerEmailInput'];
    disableElements(elementsId);
    
    // starting progressbar
    NProgress.start();

	var csrftoken = getCookie('csrftoken');
	$.ajax({
        type: "POST",
        url: "register/email/",
        data: {
            'email':emailAddress,
        },
        beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    },
        success: function (data) {
            // stop progressbar
            NProgress.done();
            if (data=='Success'){
            	showRegisterFormPost();
            } else {
            	createCustomNotification(data, 'danger');
                enableElements(elementsId);
            }
        }
    });
}
function completeRegistration(username, email, password){
    hideNotificationPanel();

    // starting progressbar
    NProgress.start();

    // disabling elements
    var elementsId = ['registerButtonPost', 'registerUsernameInput', 'registerEmailInput', 'registerPasswordInput'];
    disableElements(elementsId);
	var csrftoken = getCookie('csrftoken');
	$.ajax({
        type: "POST",
        url: "register/",
        data: {
            'email':email,
            'username':username,
            'password':password
        },
        beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    },
        success: function (data) {
            if (data == 'Registration Complete'){
                createCustomNotification(data+', redirecting after 3 seconds ', 'success');
                window.setTimeout(function(){
                    notificationDismiss();
                    
                    // disabling progressbar
                    NProgress.done();

                    login(username, password);
                }, 3000);
            } else {
                enableElements(elementsId);
                createCustomNotification(data, 'danger');

                // disabling progressbar
                NProgress.done();
            }
        }
    });
}
function login(username, password){
    hideNotificationPanel();
    // disabling elements
    var elementsId = ['loginButton', 'loginUsernameInput', 'loginPasswordInput'];
    disableElements(elementsId);

    // starting progressbar
    NProgress.start();

	var csrftoken = getCookie('csrftoken');
	$.ajax({
        type: "POST",
        url: "login/",
        data: {
            'username':username,
            'password':password
        },
        beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    },
        success: function (data) {
            // disabling progressbar
            NProgress.done();

        	if (data=='Success'){
        		location.href='dashboard/';
        	} else {
                enableElements(elementsId);
        		createCustomNotification(data, 'danger');
        	}
        }
    });
}
function showLoginForm(){
    // progressbar
    NProgress.start();

    hideNotificationPanel();
	$('#registerWrapper').hide();
	$('#loginWrapper').slideDown('slow');

    // disabling progressbar
    NProgress.done();
}
function showRegisterForm(){
    // progressbar
    NProgress.start();

    hideNotificationPanel();
	$('#loginWrapper').hide();
	$('#registerWrapper').slideDown('slow');

    // disabling progressbar
    NProgress.done();
}
function showRegisterFormPost(){
    // progressbar
    NProgress.start();

    hideNotificationPanel();
	$('.formWrapperRegisterPre').hide();
	$('.formWrapperRegisterPost').slideDown('slow');

    // disabling progressbar
    NProgress.done();
}
function submitFormOnEnterLogin(){
    document.getElementById("loginButton").click();
}
function submitFormOnEnterRegisterPre(){
    document.getElementById("registerButtonPre").click();
}
function submitFormOnEnterRegisterPost(){
    document.getElementById("registerButtonPost").click(); 
}
