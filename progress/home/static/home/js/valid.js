function delMessageAfter(element) {

	nextElementClass = element.next().attr('class')

	if (nextElementClass == 'error'
		|| nextElementClass == 'success') {
		element.next().remove()
	}
}

function errorMessageAfter(element,text) {
	delMessageAfter(element)
	message = $(`<span class='error'>${text}</span>`)
	$(element).after(message)
}

function successMessageAfter(element) {
	delMessageAfter(element)
	$(element).after(`<span class='success'>&#10003;</span>`)
}

function validate(element,pattern,errorMessage){
	text = element.val()
	if (pattern.test(text)) {
		successMessageAfter(element)
		return true;
	}
	else {
		errorMessageAfter(element,errorMessage)
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
	firstPassword = $(`input[name=password][id=${id}`).val();
	return validate(element,RegExp('^'+firstPassword+'$'),'Пароли не совпадают')
}