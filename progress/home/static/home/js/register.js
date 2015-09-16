//needed for safe POST requests
//details: https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function ajaxSetup() {
	var csrftoken = Cookies.get('csrftoken');
	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
}

function changeMark(link, student_id, job_id, new_mark) {
	ajaxSetup();

	$.ajax({
		type: 'POST',
		url: link,
		data: {
			'student_id': student_id,
			'job_id': job_id,
			'new_mark': new_mark,
			'action': 'change_mark'
		},
		dataType: 'json'
	})
}

function changeDate(link, student_id, job_id, new_date) {
	new_date = new_date.split('-')
	year = new_date[0]
	month = new_date[1]
	day = new_date[2]

	ajaxSetup();
	$.ajax({
		type: 'POST',
		url: link,
		data: {
			'student_id':student_id,
			'job_id':job_id,
			'year':year,
			'month':month,
			'day':day,
			'action':'change_date'
		},
		dataType:'json'
	})
}