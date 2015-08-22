// function confirm(message,subjectid){
// 	checkbox = $(`input[id=${subjectid}]`)
// 	x = checkbox.position().left
// 	y = checkbox.position().top

// 	$('body').append("<div class='confirmation'></div>")
// 	$('.confirmation').append(`<span>${message}</span><br>`)
// 	$('.confirmation').append(`<input name='yes'	type='button' value='Да'>&nbsp;`)
// 	$('.confirmation').append(`<input name='no'		type='button' value='Нет'>`)
// 	$('.confirmation').css(
// 		{
// 			left: x+'px',
// 			top: (y+30)+'px'
// 		}
// 	)

// 	$('input[name=yes]').on('click',function(){
// 		$('.confirmation').remove()
// 		return true;
// 	})
// 	$('input[name=no]').on('click',function(){
// 		$('.confirmation').remove()
// 		return false;
// 	})
// }

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