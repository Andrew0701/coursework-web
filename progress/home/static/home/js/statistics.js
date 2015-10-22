//needed for safe POST requests
//details: https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function ajaxSetup() {
	var csrftoken = Cookies.get('csrftoken');
	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
}

function buildChart(link,id) {
	var data = {
	    datasets: [
	        {
	            label: "Passed",
	            fillColor: "rgba(151,187,205,0.05)",
	            strokeColor: "rgba(151,187,205,1)",
	            pointColor: "rgba(151,187,205,1)",
	            pointStrokeColor: "#fff",
	            pointHighlightFill: "#fff",
	            pointHighlightStroke: "rgba(151,187,205,1)"
	        },
	        {
	            label: "Plan",
	            fillColor: "rgba(0,255,0,0.05)",
	            strokeColor: "rgba(0,255,0,0.2)",
	            pointColor: "rgba(255,0,0,0.2)",
	            pointStrokeColor: "#fff",
	            pointHighlightFill: "#fff",
	            pointHighlightStroke: "rgba(151,187,205,1)"
	        }
	    ]
	};

	ajaxSetup();
	$.getJSON(link,function (respond) {
		data.labels = respond.labels
		data.datasets[0].data = respond.dataset
		data.datasets[1].data = respond.plan
		console.log(data)
		var ctx = $('#statistics').get(0).getContext('2d')
		var chart = new Chart(ctx).Line(data)
	})

	return data;
}