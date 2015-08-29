function delMessageAfter(element) {

	nextElementClass = element.next().attr('class')

	if (nextElementClass == 'error'
		|| nextElementClass == 'success') {
		element.next().remove()
	}
}

function errorMessageAfter(element,text) {
	delMessageAfter(element)
	message = $("<span class='error'>" + text + "</span>");
	$(element).after(message)
}

function successMessageAfter(element) {
	delMessageAfter(element)
	$(element).after("<span class='success'>&#10003;</span>");
}

function validate(element,pattern,errorMessage){
	text = element.val()
	if (pattern.test(text)) {
		successMessageAfter(element)
        all_checking[element.attr('name')] = true;
        block_submit_student();
		return true;
	}
	else {
		errorMessageAfter(element,errorMessage);
        all_checking[element.attr('name')] = false;
		block_submit_student();
        return false;
	}
}

function validateWord(element) {
	return validate(element,/^[а-яА-ЯёЁ]{3,30}$/,'Только кириллица (3-30)')
}

function validateLogin(element) {
	return validate(element,/^[a-zA-Z]{3,30}$/,'Только латинница (3-30)')
}

function validateEmail(element) {
	return validate(element,/^[a-z0-9\._-]+@[a-z-]+\.[a-z]+$/,'Как обычно кароч')
}

function validatePassword(element) {
	return validate(element,/^[a-zA-Z0-9_]{6,30}$/,'Латинница, цифры, _ (6-30)')
}

function validatePasswordConfirmation(element,id) {
	firstPassword = $("input[name=password][id=" + id).val();
	return validate(element,RegExp('^'+firstPassword+'$'),'Пароли не совпадают')
}

var all_checking = {};

function block_submit_student(){
    
    var count_right_values = 0;
    var need_count_right = 7;   //Необходимое количество правильно заполненнных полей
    for (var val in all_checking){
        if (all_checking[val]) {
            count_right_values++;
        }
    }
    if (count_right_values >= need_count_right){ 
        $('input[type=submit]').prop('disabled',false);
    }else{
        $('input[type=submit]').prop('disabled',true);
    }
}

function listener_on_change(){
    $('#reg_student').prop('disabled',true);
    $('#reg_student').mouseover(give_the_massiv);
    
}

function give_the_massiv(){
    for (var val in all_checking){
        console.log(val);
    }
    console.log(all_checking);
}