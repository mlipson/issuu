{% extends "base_2.tpl" %}

{% block top_nav %}
	<a href="/">
		<img src="https://magazinec.com/wp-content/uploads/2019/04/CLogo_Web.svg" height=75>
		<span class="c_style">California Style & Culture</span>
	</a>
{% endblock %}

{% block mode %}
{% endblock %}

{% block content %}
	<a href="/" class="alignleft hilite">all issues</a>
	<span class="alignright">{{result['title']}}&nbsp;&nbsp;|&nbsp;&nbsp;{{result['description']}}</span>
	<br>
	<br>
	<br>
	<iframe allowfullscreen allow="fullscreen"
		style="border:none;width:100%;height:730px;"
		src="//e.issuu.com/embed.html?d={{ result['name'] }}
			&hideIssuuLogo=true
			&hideShareButton=true
			&u=cdigital
			&backgroundColor=%23f7f7f7">
	</iframe>
{% endblock %}

{% block footer %}
    {{version}}&nbsp;&nbsp;|&nbsp;&nbsp;2020 C Publishing, LLC
{% endblock %}

{% block script %}
	<!-- <script type="text/javascript" src="//e.issuu.com/embed.js" async="true"></script> -->
{% endblock %}
