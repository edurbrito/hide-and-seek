<script>
	import '../app.css';
</script>

<div
	id="warning"
	class="w-full h-full bg-primary flex flex-col items-center justify-center text-center text-white p-8 font-bold absolute"
	style="z-index: 1000000000; display: none;"
>
	🙈 Please, turn on Geolocation on your device and refresh this page. 🙉
</div>
<slot class="bg-primary" />
