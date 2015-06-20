
/**
 * AppEvent:
 * Global Events that occurs in the application
 */
var AppEvent = {
	/**
	 * Function called on document ready
	 */
	init: function() {
		// Toogle login box event
		if($("#login-form-modal").length === 1) {
			$(".show-login-form-modal").click(this.showLoginModal);
		}
	},
		
	/**
	 * Informations form submit:
	 * - _isSubmittingForm
	 * + initAjaxForm
	 * - _submitAjaxForm
	 */
	_isSubmittingForm: false,
	
	initAjaxForm: function(formId, buttonId, url) {
		url = url == undefined ? '' : url;
		$('#'+buttonId).click(this._submitAjaxForm.bind(this, formId, buttonId, url));
	}, 
		
	_submitAjaxForm: function(formId, buttonId, url) {
		if(!this._isSubmittingForm) {
			var that = this;
			
			$.ajax({
				url: url,
				type: "POST",
				data: $('#'+formId).serialize()
			}).done(function(data) {
				var formContent = $('#'+formId, data).html();
				$('#'+formId).html(formContent);
				AppEvent.initAjaxForm(formId, buttonId, url);
				that._isSubmittingForm = false;
			}).fail(function() {
				that._isSubmittingForm = false;
			});
						
			this._isSubmittingForm = true;
		}
	},
	
	/**
	 * Toogle the login box in the header
	 */
	showLoginModal: function(event) {
		event.preventDefault();
		$('#login-form-modal').modal('show');
	}
};

/**
 * RegisterForm:
 * Scripts used for the RegisterForm page
 */
var RegisterForm = {
	generateUsername: function() {
		var generated = "";
		var firstName = $.trim($('#id_first_name').val()), lastName = $.trim($('#id_last_name').val());
		var randomInt = Math.floor((Math.random() * 100) + 1);
		
		generated = (firstName!=="")? firstName + "." : "";
		generated += (lastName!=="")? lastName + "." : "";
		generated += randomInt;
		generated = generated.toLowerCase();
		
		$('#id_username').val(generated);
	}
};

$(document).ready(function() {
	AppEvent.init();
});
