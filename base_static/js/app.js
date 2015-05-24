
/**
 * AppEvent:
 * Global Events that occurs in the application
 */
var AppEvent = {
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
	}
};