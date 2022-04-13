<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	const game_id = $page.params.gameid;
	let hider;
	let username = '';
	let distance = 'some';
	let found = false;
	var currentPosition = {
		latitude: 0,
		longitude: 0
	};

	const options = {
		enableHighAccuracy: true,
		maximumAge: 60000,
		timeout: 30000
	};

	onMount(async () => {
		hider = JSON.parse(localStorage.getItem('hider'));
		if (hider == null || !hider) {
			await fetch(`http://localhost:5000/hide/${game_id}`, { method: 'POST' })
				.then((response) => response.json())
				.then((response) => {
					localStorage.setItem('hider', JSON.stringify(response));
					hider = response;
				});
		}

		username = hider.username;

		if ('geolocation' in navigator) {
			getCurrentPosition();
			setInterval(getCurrentPosition, 15000);
		} else {
			document.getElementById('warning').style.setProperty('display', 'flex');
		}

		function getCurrentPosition() {
			navigator.geolocation.getCurrentPosition(
				async (position) => {
					currentPosition = {
						latitude: position.coords.latitude,
						longitude: position.coords.longitude
					};

					await fetch(
						`http://localhost:5000/hider/${game_id}?uuid=${hider.uuid}&latitude=${currentPosition.latitude}&longitude=${currentPosition.longitude}`,
						{ method: 'POST' }
					)
						.then((response) => response.json())
						.then((response) => {
							found = response.found;
							distance = response.distance;
						});
				},
				function (error) {
					switch (error.code) {
						case error.PERMISSION_DENIED:
							console.log('Denied request for Geolocation.');
							break;
						case error.POSITION_UNAVAILABLE:
							console.log('Location unavailable.');
							break;
						case error.TIMEOUT:
							console.log('Location request timed out.');
							break;
						default:
							console.log('Default case.');
							break;
					}
					document.getElementById('warning').style.setProperty('display', 'flex');
				},
				options
			);
		}
	});
</script>

<span class="mb-5 font-semibold">{username}</span>
<div class="game-circle">
	<span class="text-lg">Game ID</span>
	<span class="text-2xl font-bold">{game_id.toUpperCase()}</span>
</div>
<span class="mt-5 text-center text-lg"
	>The Seeker is <br />{distance == 'some' ? distance : Math.round(parseFloat(distance))} meters from
	you!</span
>
{#if found}
	<div class="text-white text-2xl font-bold text-center">
		You were found!<br />🙈🙉<br />
		<span class="text-base font-normal">Better luck next time...</span>
	</div>
{/if}
