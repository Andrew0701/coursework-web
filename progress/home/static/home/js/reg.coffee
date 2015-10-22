makeGroupSelect = (groups) ->
  $('#group').empty()
  for i of groups
    `i = i`
    $('#group').append '<option value="' + groups[i] + '">' + groups[i] + '</option>'
  return

loadGroupsFrom = (link) ->
  year = $('#year').val()
  $.ajax
    type: 'GET'
    url: link
    data: 'year': year
    dataType: 'json'
    success: makeGroupSelect
  return

formVisibilityToggle = ->
  input = $('input[name="who"]')
  input.change ->
    elem = $('input:radio:checked')
    switch elem.val()
      when 'student'
        $('form#student').show()
        $('form#teacher').hide()
      when 'teacher'
        $('form#teacher').show()
        $('form#student').hide()
      else
        break
    return
  return
