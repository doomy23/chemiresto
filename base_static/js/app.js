
/**
 * AppEvent:
 * Global Events that occurs in the application
 */
var AppEvent = {
	/**
	 * Function called on document ready
	 */
	init: function() {
		// Check content min size from window height
		this.checkContentMinHeight();
		$(window).resize(this.checkContentMinHeight); 
		
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
	
	initAjaxForm: function(formId, buttonId, url, callback) {
		url = url == undefined ? '' : url;
		$('#'+buttonId).click(this._submitAjaxForm.bind(this, formId, buttonId, url, callback));
	}, 
		
	_submitAjaxForm: function(formId, buttonId, url, callback) {
		if(!this._isSubmittingForm) {
			var that = this;
			
			$.ajax({
				url: url,
				type: "POST",
				data: $('#'+formId).serialize()
			}).done(function(data) {
				var formContent = $('#'+formId, data).html();
				$('#'+formId).html(formContent);
				AppEvent.initAjaxForm(formId, buttonId, url, callback);
				that._isSubmittingForm = false;
				
				if(typeof callback == "function") {
					callback();
				}
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
	},
	
	/**
	 * Check content min height from current window height
	 */
	checkContentMinHeight: function() {
		var wHeight = $(window).height();
		var diff = wHeight - 500;
		var minHeight = 265 + diff;
		if(minHeight>0) $('#page-content').css('min-height', minHeight);
	}
};

/**
 * RegionSelector:
 * Scripts used for replacing the text input by a select if necessary
 * for the region/state/province field to ensure same values for Canada
 */
var RegionSelector = {
	/**
	 * Function called on document ready
	 */
	init: function(countryFieldSel, regionFieldSel) {
		var that = this;
		
		$(countryFieldSel).change(function(){
			that.countryChanged(regionFieldSel, $(this).val());
		});
		
		this.countryChanged(regionFieldSel, $(countryFieldSel).val());
	},
	
	/**
	 * Function called when a country change
	 */
	countryChanged: function(regionFieldSel, country) {
		var fieldName = $(regionFieldSel).attr('name');
		var fieldId = $(regionFieldSel).attr('id');
		var isTextField = $(regionFieldSel).is('input');
		var listedCountry = Object.keys(this._regionsByCountries).indexOf(country) != -1;
		
		if(listedCountry) {
			var fieldValue = $(regionFieldSel).val();
			$(regionFieldSel).replaceWith('<select id="'+fieldId+'" class="lazyselect form-control" type="text" name="'+fieldName+'"></select>');
			
			$(regionFieldSel).append('<option value=""></option>');
			
			for(var i=0 ; i<Object.keys(this._regionsByCountries[country]).length ; i++) {
				var regionCode = Object.keys(this._regionsByCountries[country])[i];
				var regionName = this._regionsByCountries[country][regionCode];
				
				$(regionFieldSel).append('<option value="'+regionCode+'">'+regionName+'</option>');
			}
			
			$(regionFieldSel).val(fieldValue);
			
		} else if(!isTextField) {
			$(regionFieldSel).replaceWith('<input id="'+fieldId+'" class="textinput textInput form-control" type="text" maxlength="250" name="'+fieldName+'"/>');
		}
	},
	
	/**
	 * List of all regions by countries
	 */
	_regionsByCountries: {
		'CA': {
			'AB': 'Alberta',
			'BC': 'Colombie Britanique',
			'MB': 'Manitoba',
			'NB': 'Nouveau Brunswick',
			'NL': 'Terre-neuve',
			'NT': 'Territoires du Nord-Ouest',
			'NS': 'Nouvelle-Écosse',
			'NU': 'Nunavut',
			'ON': 'Ontario',
			'PE': 'Île-du-Prince-Édouard',
			'QC': 'Québec',
			'SK': 'Saskatchewan',
			'YT': 'Yukon'
		}
	}
};

/**
 * OUTDATED
 * RegisterForm:
 * Scripts used for the RegisterForm page
 */
/*var RegisterForm = {
	generateUsername: function() {
		var firstName = $.trim($('#id_first_name').val()), lastName = $.trim($('#id_last_name').val());
		
		if(!(firstName=="" && lastName=="")) {
			var generated = "";
			var randomInt = Math.floor((Math.random() * 100) + 1);
			
			generated = (firstName!=="")? firstName + "." : "";
			generated += (lastName!=="")? lastName + "." : "";
			generated += randomInt;
			generated = generated.toLowerCase();
			
			$('#id_username').val(generated);
		}
	}
};*/

$(document).ready(function() {
	AppEvent.init();
});
