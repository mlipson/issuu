{% extends "base_2.tpl" %}

{% set style = 'grid2' %}

{% block top_nav %}
	<a href="/"><img src="http://magazinec.com/wp-content/themes/cpub_landing/img/logo-ccalistyle.svg"></a>
{% endblock %}

{% block content %}
	<ul>
		{% for i in result %}
			<li>
				<a title="{{i['title']}}" href="/{{i['name']}}">
				<img src="http://image.issuu.com/{{i['documentId']}}/jpg/page_1_thumb_large.jpg" height="240" width="180">
				<br>
				&nbsp;&nbsp;{{i['description']}}&nbsp;&nbsp;
				</a>
			</li>
		{% endfor %}
	</ul>
{% endblock %}

{% block footer %}
    {{version}}&nbsp;&nbsp;|&nbsp;&nbsp;2018 C Publishing, LLC
{% endblock %}
