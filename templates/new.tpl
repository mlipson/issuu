{% extends "form2.tpl" %}

{% set post = "/upload" %}

{% block top_nav %}
	<a href="/">
		<!-- <img src="http://magazinec.com/wp-content/themes/cpub_landing/img/logo-ccalistyle.svg"> -->
		C California Style & Culture
	</a>
{% endblock %}

{% block mode %}
{% endblock %}

{% block form_a %}
{% endblock %}

{% block form_b %}
	<div class="form_item">
		<span class="form_head">title</span>
		<br>
		<input type="text" name="title" title="title" class="url" placeholder="C California Style" value="{{title}}">
	</div>
	<div class="form_item">
		<span class="form_head">name</span>
		<br>
		<input type="text" name="name" title="name" class="url" placeholder="name" required="required" value="{{name}}">
	</div>
{% endblock %}

{% block form_c %}
		<div class="form_item">
			<span class="form_head">publishDate</span>
			<br>
			<input type="text" name="publishDate" id="datepicker1" class="url" placeholder="yyyy-mm-dd" title="yyyy-mm-dd format" value="{{publishDate}}">
		</div>
		<div class="form_item">
			<span class="form_head">description</span>
			<br>
			<input type="text" name="description" class="url" placeholder="description" title="description" value="{{description}}">
		</div>
{% endblock %}

{% block form_d %}
		<div class="form_item">
			<span class="form_head">tags</span>
			<br>
			<input type="text" name="tags" title="Comma separated" class="url" placeholder="comma separated" value="{{tags}}">
		</div>
		<div class="form_item">
			<span class="form_head">access</span>
			<br>
			<input type="text" name="access" title="Comma separated" class="url" placeholder="private" value="{{access}}">
		</div>
		<div class="form_item">
			<span class="form_head">doc</span>
			<br>
			<input type="file" name="file"/>
		</div>
{% endblock %}

{% block form_e %}
	<div class="form_item">
		<br>
		<input type="submit" name="btn" value="Cancel" class="cbp-mc-submit">&nbsp;
		<input type="submit" name="btn" value="Submit" class="cbp-mc-submit">
	</div>
{% endblock %}

{% block form_f %}
<link href="https://api.motion.ai/sdk/webchat.css" rel="stylesheet" type="text/css">
<script src="https://api.motion.ai/sdk/webchat.js"></script>
<script>
   motionAI_Init('85259?color=3588eb&sendBtn=SEND&inputBox=Type%20something...&token=bab0fb066277f15cff8b8eddf76b862d',true,400,470,'https://api.motion.ai/sdk/botbtn.png');
   /* You may also invoke motionAI_Open() to manually open the modal. */
</script>

{% endblock %}

{% block footer %}
    {{version}}&nbsp;&nbsp;|&nbsp;&nbsp;2018 C Publishing, LLC
{% endblock %}

{% block script %}
	<script>
		var picker1 = new Pikaday(
		{
			field: document.getElementById('datepicker1'),
			firstDay: 1,
			minDate: new Date('2000-01-01'),
			maxDate: new Date('2020-12-31'),
			yearRange: [2000,2020],
			format: 'YYYY-MM-DD',
			});
		var picker2 = new Pikaday(
		{
			field: document.getElementById('datepicker2'),
			firstDay: 1,
			minDate: new Date('2000-01-01'),
			maxDate: new Date('2020-12-31'),
			yearRange: [2000,2020],
			format: 'YYYY-MM-DD',
		});
	</script>
{% endblock %}
