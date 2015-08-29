function makeGroupSelect(groups) {
	$('#group').empty()

	for (i in groups){
		$('#group').append(
            '<option value="' + groups[i] + '">'
                + groups[i] +
            '</option>'
        )
	}
}

function loadGroupsFrom(link) {
	year = $('#year').val()
	$.ajax({
		type: 'GET',
		url: link,
		data: { 'year':year },
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
                $('form#student').show();
                $('form#teacher').hide();
                break;
            case 'teacher':
                $('form#teacher').show();
                $('form#student').hide();
                break;
            default:
                break;
        }
    })
}