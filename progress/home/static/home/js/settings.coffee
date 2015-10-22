#needed for safe POST requests
#details: https://docs.djangoproject.com/en/dev/ref/csrf/#ajax

ajaxSetup = ->
  csrftoken = Cookies.get('csrftoken')

  csrfSafeMethod = (method) ->
    # these HTTP methods do not require CSRF protection
    /^(GET|HEAD|OPTIONS|TRACE)$/.test method

  $.ajaxSetup beforeSend: (xhr, settings) ->
    if !csrfSafeMethod(settings.type) and !@crossDomain
      xhr.setRequestHeader 'X-CSRFToken', csrftoken
    return
  return

toggleStudentSubjectRecord = (link, studentid, subjectid, teacherid, checked) ->
  ajaxSetup()
  $.ajax
    type: 'POST'
    url: link
    data:
      'studentid': studentid
      'subjectid': subjectid
      'teacherid': teacherid
      'action': if checked then 'student_add_subject' else 'student_delete_subject'
    dataType: 'json'
  return

toggleTeacherSubjectRecord = (link, subjectid, checked) ->
  ajaxSetup()
  $.ajax
    type: 'POST'
    url: link
    data:
      'subjectid': subjectid
      'action': if checked then 'teacher_add_subject' else 'teacher_delete_subject'
    dataType: 'json'
  return

changeTeacher = (link, studentid, subjectid, teacherid) ->
  ajaxSetup()
  $.ajax
    type: 'POST'
    url: link
    data:
      'studentid': studentid
      'subjectid': subjectid
      'teacherid': teacherid
      'action': 'student_change_teacher'
    dataType: 'json'
  return

addJob = (link, subjectid, name, short_name) ->
  ajaxSetup()
  $.ajax
    type: 'POST'
    url: link
    data:
      'subjectid': subjectid
      'name': name
      'short_name': short_name
      'action': 'add_job'
    dataType: 'json'
    success: location.reload()
  return

deleteJob = (link, jobid, confirmationMessage) ->
  if !confirm(confirmationMessage)
    return
  ajaxSetup()
  $.ajax
    type: 'POST'
    url: link
    data:
      'jobid': jobid
      'action': 'delete_job'
    dataType: 'json'
    success: location.reload()
  return

editJobName = (link, jobid, promptText, defaultText) ->
  newName = prompt(promptText, defaultText)
  if newName == null
    return
  ajaxSetup()
  $.ajax
    type: 'POST'
    url: link
    data:
      'jobid': jobid
      'new_name': newName
      'action': 'edit_job_name'
    dataType: 'json'
    success: location.reload()
  return

editJobShortName = (link, jobid, promptText, defaultText) ->
  newShortName = prompt(promptText, defaultText)
  if newShortName == null
    return
  ajaxSetup()
  $.ajax
    type: 'POST'
    url: link
    data:
      'jobid': jobid
      'new_short_name': newShortName
      'action': 'edit_job_short_name'
    dataType: 'json'
    success: location.reload()
  return

toggleLogRecord = (link, studentid, jobid, checked) ->
  ajaxSetup()
  $.ajax
    type: 'POST'
    url: link
    data:
      'studentid': studentid
      'jobid': jobid
      'action': if checked then 'add_log_entry' else 'delete_log_entry'
  return
