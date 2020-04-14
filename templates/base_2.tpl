<!DOCTYPE html>
<!--[if lt IE 7 ]><html class="ie ie6" lang="en"> <![endif]-->
<!--[if IE 7 ]><html class="ie ie7" lang="en"> <![endif]-->
<!--[if IE 8 ]><html class="ie ie8" lang="en"> <![endif]-->
<!--[if (gte IE 9)|!(IE)]><!--><html lang="en"> <!--<![endif]-->

	<head>
			<!-- Basic Page Needs
	  ================================================== -->
		<meta charset="utf-8">
		<title>C California Style & Culture</title>
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
		<link href="https://p.typekit.net/p.css?s=1&k=gow0agp&ht=tk&f=6781.6782.6785.6788.10881.10882.10884.10885.10954.13453.13454.13455.13458.13464.13465.13468.13472.13473.19416.19420.25657.25658.25659.25660.25670.25671.25672.25673.32874.32875.39283.39292.41781.41782.41787.41788.41793.41794.41795.41796.41797.41798.41799.41800&a=14419530&app=typekit&e=css" rel="stylesheet">



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
