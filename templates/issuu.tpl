{% extends "base_2.tpl" %}

{% set style = 'grid2' %}

{% block top_nav %}
	<a href="/">
		<img src="https://magazinec.com/wp-content/uploads/2019/04/CLogo_Web.svg" height=75>
		<span class="c_style">California Style & Culture</span>
	</a>
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
    {{version}}&nbsp;&nbsp;|&nbsp;&nbsp;2020 C Publishing, LLC
{% endblock %}
