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

function toggleStudentSubjectRecord(link,studentid,subjectid,teacherid,checked) {
	ajaxSetup();

	$.ajax({
		type: 'POST',
		url: link,
		data: {
			'studentid':studentid,
			'subjectid':subjectid,
			'teacherid':teacherid,
			'action': checked
				? 'student_add_subject'
				: 'student_delete_subject'
		},
		dataType: 'json'
	})
}

function toggleTeacherSubjectRecord(link,subjectid,checked) {
	ajaxSetup();

	$.ajax({
		type: 'POST',
		url: link,
		data: {
			'subjectid':subjectid,
			'action': checked
				? 'teacher_add_subject'
				: 'teacher_delete_subject'
		},
		dataType: 'json'
	})
}

function changeTeacher(link,studentid,subjectid,teacherid) {
	ajaxSetup();

	$.ajax({
		type: 'POST',
		url: link,
		data: {
			'studentid':studentid,
			'subjectid':subjectid,
			'teacherid':teacherid,
			'action':'student_change_teacher',
		},
		dataType: 'json'
	})
}

function addJob(link,subjectid,name) {
	ajaxSetup();
	$.ajax({
		type: 'POST',
		url: link,
		data: {
			'subjectid':subjectid,
			'name':name,
			'action':'add_job'
		},
		dataType: 'json',
		success: location.reload()
	})
}

function deleteJob(link,jobid,confirmationMessage) {

	if (!confirm(confirmationMessage)){
			return;
	}

	ajaxSetup();
	$.ajax({
		type: 'POST',
		url: link,
		data: {
			'jobid':jobid,
			'action':'delete_job'
		},
		dataType: 'json',
		success: location.reload()
	})
}

function editJob(link,jobid,promptText,defaultText) {

	newName = prompt(promptText,defaultText)

	if (newName == null) {
		return;
	}

	ajaxSetup();
	$.ajax({
		type: 'POST',
		url: link,
		data: {
			'jobid':jobid,
			'new_name':newName,
			'action':'edit_job'
		},
		dataType: 'json',
		success: location.reload()
	})
}