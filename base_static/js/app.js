
/**
 * AppEvent:
 * Global Events that occurs in the application
 */
var AppEvent = {
	_isSubmittingLoginForm: false,
	
	_selectors: {
		submitLoginForm: {
			user: $('#login-form input[name=user]'),
			pass: $('#login-form input[name=pass]')
		}
	},
		
	submitLoginForm: function() {
		if(!this._isSubmittingLoginForm) {
			$.ajax({
		        url: "/account/login/",
		        type: "POST",
		        data: {
		        	user: this._selectors.submitLoginForm.user.val(),
		        	pass : this._selectors.submitLoginForm.pass.val()
		        }
		    }).done(function(data) {
		    	console.log(data);
		    }).always(function() {
		    	this._isSubmittingLoginForm = false;
		    });
			
			this._isSubmittingLoginForm = true;
		}
		
		return false;
	}
};