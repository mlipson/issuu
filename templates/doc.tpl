{% extends "base_2.tpl" %}

{% block top_nav %}
	<h2><a href="/">
		<!-- <img src="https://magazinec.com/wp-content/uploads/2019/05/SecondaryLogo-White-small.png" height="100"> -->
		C California Style & Culture
	</a>
</h2>
{% endblock %}

{% block mode %}
{% endblock %}

{% block content %}
	<a href="/" class="alignleft hilite">all issues</a>
	<span class="alignright">{{result['title']}}&nbsp;&nbsp;|&nbsp;&nbsp;{{result['description']}}</span>
	<br>
	<br>
	<br>
	<div data-configid="{{result['dataconfigId']}}" style="width: 800px; height: 685px;" class="issuuembed aligncenter"></div><script type="text/javascript" src="//e.issuu.com/embed.js" async="true"></script>
{% endblock %}

{% block footer %}
    {{version}}&nbsp;&nbsp;|&nbsp;&nbsp;2019 C Publishing, LLC
{% endblock %}

{% block script %}
	<script type="text/javascript" src="//e.issuu.com/embed.js" async="true"></script>
{% endblock %}
