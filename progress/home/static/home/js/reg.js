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

function formVisibilityToggle(){
    var input = $('input[name="who"]');
    input.change(function(){
        elem = $("input:radio:checked");
        switch (elem.val()){
            case 'student':
                $('form[id="student"]').show();
                $('form[id="teacher"]').hide();
                break;
            case 'teacher':
                $('form[id="teacher"]').show();
                $('form[id="student"]').hide();
                break;
            default:
                break;
        }
    })
}