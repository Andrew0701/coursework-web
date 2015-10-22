all_checking = {}

delMessageAfter = (element) ->
  if element.next().is('span')
    element.next().remove()
  return

errorMessageAfter = (element, text) ->
  delMessageAfter element
  $(element).parent('div').attr 'class', 'form-group has-error has-feedback'
  message = $('<span class=\'glyphicon glyphicon-remove form-control-feedback\' aria-hidden=\'true\'></span>')
  $(element).after message
  return

successMessageAfter = (element) ->
  delMessageAfter element
  $(element).parent('div').attr 'class', 'form-group has-success has-feedback'
  message = $('<span class=\'glyphicon glyphicon-ok form-control-feedback\' aria-hidden=\'true\'></span>')
  $(element).after message
  return

validate = (element, pattern, errorMessage) ->
  text = element.val()
  if pattern.test(text)
    successMessageAfter element
    all_checking[element.attr('name')] = true
    block_submit_student()
    true
  else
    errorMessageAfter element, errorMessage
    all_checking[element.attr('name')] = false
    block_submit_student()
    false

validateWord = (element) ->
  validate element, /^[а-яА-ЯёЁ]{3,30}$/, 'Только кириллица (3-30)'

validateLogin = (element) ->
  validate element, /^[a-zA-Z]{3,30}$/, 'Только латинница (3-30)'

validateEmail = (element) ->
  validate element, /^[a-z0-9\._-]+@[a-z-]+\.[a-z]+$/, 'Как обычно кароч'

validatePassword = (element) ->
  validate element, /^[a-zA-Z0-9_]{6,30}$/, 'Латинница, цифры, _ (6-30)'

validatePasswordConfirmation = (element, id) ->
  firstPassword = $('input[name=password][id=' + id).val()
  validate element, RegExp('^' + firstPassword + '$'), 'Пароли не совпадают'

block_submit_student = ->
  count_right_values = 0
  need_count_right = 7
  #Необходимое количество правильно заполненнных полей
  for val of all_checking
    if all_checking[val]
      count_right_values++
  if count_right_values >= need_count_right
    $('input[type=submit]').prop 'disabled', false
  else
    $('input[type=submit]').prop 'disabled', true
  return

listener_on_change = ->
  $('#reg_student').prop 'disabled', true
  $('#reg_student').mouseover give_the_massiv
  return

give_the_massiv = ->
  for val of all_checking
    console.log val
  console.log all_checking
  return
