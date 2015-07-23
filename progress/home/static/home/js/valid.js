function errorMessage(element,text) {
	$(element).after(`<br><span class='error'>${text}</span>`)
}

function delErrorMessage(element) {
	$(element.next().remove()) //<br>
	$(element.next().remove())
}

function isAlpha(string) {
	return /^[a-zA-Zа-яА-ЯёЁ]+$/.test(string)
}

