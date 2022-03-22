<script lang="ts">
	import GUN from 'gun';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import faker from '@faker-js/faker';
	import { distance, randInt, sha256 } from '../../utils';

	var distanceToSeeker = 'some';
	var seekerCoords = { latitude: 0, longitude: 0 };
	var found = false;
	var coords = { latitude: 100000, longitude: 100000 };

	onMount(() => {
		if ('geolocation' in navigator) {
			const db = GUN({ peers: ['http://localhost:8765/gun'] });

			found = localStorage.getItem($page.params.gameID + "_found") != null;

			var username, user, watchID;
			const options = {
				enableHighAccuracy: true,
				maximumAge: 60000,
				timeout: 30000
			};

			(async () => {
				username = localStorage.getItem($page.params.gameID + "_username");
				if (!username) {
					username =
						faker.name.firstName().toLowerCase() +
						`-${(await sha256($page.params.gameID)).slice(0, 4).toUpperCase()}${randInt(10, 99)}`;
					localStorage.setItem($page.params.gameID + "_username", username);
				}

				user = db.get(username);

				watchID = navigator.geolocation.watchPosition(
					(position) => {
						coords = {
							latitude: position.coords.latitude,
							longitude: position.coords.longitude
						};

						user.put({
							username: username,
							coordinates: JSON.stringify(coords)
						});

						db.get($page.params.gameID).get('hiders').set(user);

						let dst = Math.round(distance(seekerCoords, coords));
						distanceToSeeker = '' + dst;
						if (dst <= 50) {
							found = true;
							localStorage.setItem($page.params.gameID + "_found", "true")
						}
					},
					null,
					options
				);

				db.get($page.params.gameID)
					.get('coordinates')
					.on((data, id) => {						
						seekerCoords = JSON.parse(data);

						let dst = Math.round(distance(seekerCoords, coords));
						distanceToSeeker = '' + dst;
						if (dst <= 50) {
							found = true;
							localStorage.setItem($page.params.gameID + "_found", "true")
						}
					});
			})();
		} else {
			console.log('Hey');
		}
	});
</script>

<div class="w-full h-full flex flex-col justify-center items-center">
	<div class="w-40 h-40 rounded-full bg-white flex flex-col items-center justify-center text-white">
		<div
			class="w-36 h-36 rounded-full bg-primary flex flex-col items-center justify-center text-white text-2xl font-bold"
		>
			<span class="text-xs font-normal">Game ID:</span>
			{$page.params.gameID}
		</div>
	</div>
	<div class="text-white p-4 text-lg text-center">
		The Seeker is<br />{distanceToSeeker} meters from you!
	</div>
	{#if found}
		<div class="text-white text-2xl font-bold text-center">
			You were found!<br />🙈🙉<br />
			<span class="text-base font-normal">Better luck next time...</span>
		</div>
	{/if}
</div>
