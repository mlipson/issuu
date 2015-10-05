<!DOCTYPE html>
	<!--[if lt IE 7 ]><html class="ie ie6" lang="en"> <![endif]-->
	<!--[if IE 7 ]><html class="ie ie7" lang="en"> <![endif]-->
	<!--[if IE 8 ]><html class="ie ie8" lang="en"> <![endif]-->
	<!--[if (gte IE 9)|!(IE)]><!--><html lang="en"> <!--<![endif]-->

	<head>
			<!-- Basic Page Needs
	  ================================================== -->
		<meta charset="utf-8">
		<title>C California Style</title>
		<meta name="description" content="">
		<meta name="author" content="">

		<!-- Mobile Specific Metas
	  ================================================== -->
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

		<!-- CSS
	  ================================================== -->
		<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/base.css') }}">
		<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/layout.css') }}">
		<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/skeleton.css') }}">
		<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/pikaday.css') }}">
		<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/issuu.css') }}">

		<!-- JS
	  ================================================== -->
		<script src="{{ url_for('static', filename='js/moment.js') }}"></script>
		<script src="{{ url_for('static', filename='js/pikaday.js') }}"></script>

	</head>	

	<header>
		<div class="container">	
			<div class="sixteen columns top_nav grid1">	
				{% block top_nav %}
				{% endblock %}
			</div>
		</div>
	</header>

	<body>
		<br>
		<hr>
		<form action="{{post}}" method="POST" class="form_a" enctype="multipart/form-data">
			<div class="container">
				<div class="sixteen columns">
					<div class="">
						{% block form_a %}
						{% endblock %}
					</div>
				</div>
			</div>
			<div class="container">
				<div class="one-third column">
					<div class="">
						{% block form_b %}
						{% endblock %}
					</div>
				</div>
				<div class="one-third column">
					<div class="">
						{% block form_c %}
						{% endblock %}
					</div>
				</div>
				<div class="one-third column">
					<div class="">
						{% block form_d %}
						{% endblock %}
					</div>
				</div>
			</div>
			<div class="container">
				<div class="sixteen columns">
					<div class="alignleft">
						{% block form_e %}
						{% endblock %}
					</div>
				</div>
			</div>
			{% block form_f %}
			{% endblock %}
		</form>
	</body>

	<footer>
		<br>
		<hr>
		<div class="container">
			<div class="sixteen columns">
				<div class="footer">
					{% block footer %}
					{% endblock %}
				</div>
			</div>
		</div>
	</footer>
	
	{% block script %}
	{% endblock %}
	
</html>
