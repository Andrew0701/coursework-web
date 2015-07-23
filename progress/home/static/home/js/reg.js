function makeGroupSelect(groups) {
	$('#group').empty()

	for (i in groups){
		$('#group').append(`<option value="${groups[i]}">${groups[i]}</option>`)
	}
}

function loadGroupsFrom(link) {
	course = $('#course').val()
	$.ajax({
		type: 'GET',
		url: link,
		data: { 'course':course },
		dataType: 'json',
		success: makeGroupSelect
	})
}