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
		<meta name="robots" content="noindex">

		<!-- Mobile Specific Metas
	  ================================================== -->
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

		<!-- CSS
	  ================================================== -->
		<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/base.css') }}">
		<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/layout.css') }}">
		<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/skeleton.css') }}">
		<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/issuu.css') }}">
		<link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">

	</head>

	<header >
		<div class="container">
			<div class="sixteen columns top_nav grid1">
				{% block top_nav %}
				{% endblock %}
			</div>
		</div>
	</header>

	<body>
		<hr>
		<div class="container">
			<div class="sixteen columns {{style}}">
				{% block content %}
				{% endblock %}
			</div>
		</div>
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


</html>
