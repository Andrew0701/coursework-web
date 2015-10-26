
function botOrNot(){

    $.ajax({
        url: 'https://www.google.com/recaptcha/api/siteverify',
        type: "GET",
        data: {
            secret:"6LeqAQ8TAAAAAD-S6bEsThBycfpjMsf-ph0qYsXF",
            response:"g-recaptcha-response"
        },
        success: function(data){
            answer = $.parseJSON(data);
            alert(answer);
            return false;
        },
        async:true
    });
    return false;
}
