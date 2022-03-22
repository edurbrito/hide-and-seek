<script lang="ts">
	import GUN from 'gun';
	import faker from '@faker-js/faker';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { sha256, randInt, distance } from '../../utils';
	import Map from './map.svelte';

	const uuid = $page.params.uuid;
	var gameID = '';
	var hiders = {};
	var found = new Set();
	var nfound = 0;
	var table, watchID;
	var currentPosition = {
		latitude: 0,
		longitude: 0
	};

	const options = {
		enableHighAccuracy: true,
		maximumAge: 5000,
		timeout: 2000
	};

	onMount(() => {
		if ('geolocation' in navigator) {
			const db = GUN({ peers: ['https://hideseekgun.herokuapp.com/gun'] });

			table = document.querySelector('#hiders');

			(async () => {
				gameID = (await sha256(uuid)).slice(0, 6).toUpperCase();

				let username = faker.name.firstName().toLowerCase() + `#${randInt(1000, 9999)}`;

				navigator.geolocation.getCurrentPosition(
					(position) => {
						currentPosition = {
							latitude: position.coords.latitude,
							longitude: position.coords.longitude
						};

						console.log('get current position', currentPosition);
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
							case error.UNKNOWN_ERROR:
								console.log('An unknown error occurred.');
								break;
							default:
								console.log('Default case.');
								break;
						}
						document.getElementById('warning').style.setProperty('display', 'flex');
					},
					options
				);

				db.get(gameID).put({ seeker: username, coordinates: JSON.stringify(currentPosition) });

				setInterval(() => {
					db.get(gameID)
						.get('hiders')
						.map()
						.once((data, id) => {
							if (data) {
								if (
									distance(JSON.parse(data.coordinates), currentPosition) <= 50 ||
									found.has(data.username)
								) {
									found.add(data.username);
									data.found = true;
								}
								hiders[data.username] = data;
							}
						});

					navigator.geolocation.getCurrentPosition(
						(position) => {
							currentPosition = {
								latitude: position.coords.latitude,
								longitude: position.coords.longitude
							};
							console.log('watch current position', currentPosition);

							db.get(gameID).put({
								seeker: username,
								coordinates: JSON.stringify(currentPosition)
							});

							for (const hider in hiders) {
								if (Object.prototype.hasOwnProperty.call(hiders, hider)) {
									if (
										distance(JSON.parse(hiders[hider].coordinates), currentPosition) <= 50 ||
										found.has(hider)
									) {
										found.add(hider);
										hiders[hider].found = true;
									}
								}
							}
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
								case error.UNKNOWN_ERROR:
									console.log('An unknown error occurred.');
									break;
							}
							document.getElementById('warning').style.setProperty('display', 'flex');
						},
						options
					);
				}, 30000);

				let shareUrl = `${$page.url.host}/hide/${gameID}`;
				let shareText = `Join my Hide and Seek game session! I am calling for the best hiders in town!`;

				document
					.getElementById('twitter-share')
					.setAttribute('href', `https://twitter.com/share?url=${shareUrl}&text=${shareText}`);

				document
					.getElementById('facebook-share')
					.setAttribute(
						'href',
						`https://www.facebook.com/sharer/sharer.php?u=${shareUrl}&text=${shareText}`
					);

				document
					.getElementById('reddit-share')
					.setAttribute('href', `https://reddit.com/submit?url=${shareUrl}&title=${shareText}`);

				document
					.getElementById('telegram-share')
					.setAttribute('href', `https://telegram.me/share/url?url=${shareUrl}&text=${shareText}`);

				document
					.getElementById('whatsapp-share')
					.setAttribute('href', `whatsapp://send?text=${shareText} ${shareUrl}`);
			})();
		} else {
			document.getElementById('warning').style.setProperty('display', 'flex');
		}
	});

	$: nfound = updateTable(hiders);

	function updateTable(hiders) {
		let result = '';

		for (const hider in hiders) {
			if (Object.prototype.hasOwnProperty.call(hiders, hider)) {
				let wasfound = found.has(hider);
				let sfound = wasfound ? 'Yaaa 🤟' : 'Noo 👀';
				let coordinates = wasfound
					? ((hider) => {
							let coords = JSON.parse(hider.coordinates);
							let latitude = coords.latitude;
							let longitude = coords.longitude;
							return `lat: ${latitude}, lon: ${longitude}`;
					  })(hiders[hider])
					: '';

				result += `<tr class="bg-secondary table-border w-full flex flex-row">
				<td class="table-border py-2 text-center text-xs w-1/3">${hider}</td>
				<td class="table-border py-2 text-center text-xs w-1/3">${sfound}</td>
				<td class="table-border py-2 text-center text-xs w-1/3">${coordinates}</td>
				</tr>`;
			}
		}

		if (table) table.innerHTML = result;

		return found.size;
	}

	function copyToClipBoard(text) {
		navigator.clipboard.writeText(text);
	}
</script>

<div class="scrollport w-screen h-screen">
	<div class="child h-full w-full relative flex flex-shrink-0 flex-col bg-primary">
		<Map {hiders} {currentPosition} />
		<div
			id="navbar"
			class="w-full h-fit absolute bottom-0 flex flex-row text-white p-2 bg-primary"
			style="z-index: 10000000;"
		>
			<div class="w-1/2 items-center text-center">
				<span class="text-sm font-bold">Game ID:</span>
				<span
					class="text-sm"
					on:click={() => {
						copyToClipBoard(gameID);
					}}>{gameID}</span
				>
			</div>
			<div class="w-1/2 items-center text-center">
				<span class="text-sm font-bold">Found:</span>
				<span class="text-sm">{nfound}/{Object.keys(hiders).length}</span>
			</div>
		</div>
	</div>
	<div
		class="child h-full w-full flex flex-shrink-0 sm:p-2 md:p-12 pt-24 flex-col items-center bg-primary text-white"
	>
		<h2 class="text-2xl text-white font-extrabold mb-2 md:mt-auto">HIDERS</h2>
		<thead class="w-full h-fit text-sm bg-secondary border">
			<tr class="text-white font-bold table-border w-full flex">
				<th class="py-2 text-sm w-1/3">Nickname</th>
				<th class="py-2 text-sm w-1/3">Found</th>
				<th class="py-2 text-sm w-1/3">Coordinates</th>
			</tr>
		</thead>
		<tbody
			id="hiders"
			class="bg-transparent overflow-y-scroll w-full border"
			style="max-height: 240px;"
		/>
		<h3 class="text-xl text-white font-extrabold mt-auto">SHARE</h3>
		<div class="px-4 py-1 text-center mb-auto">
			<a id="twitter-share" href="/" class="share-btn">
				<img src="/social/twitter.png" alt="Twitter" class="w-6" />
			</a>

			<a id="facebook-share" href="/" class="share-btn">
				<img src="/social/facebook.png" alt="Facebook" class="w-6" />
			</a>

			<a id="reddit-share" href="/" class="share-btn">
				<img src="/social/reddit.png" alt="Reddit" class="w-6" />
			</a>

			<a id="telegram-share" href="/" class="share-btn">
				<img src="/social/telegram.png" alt="Telegram" class="w-6" />
			</a>

			<a id="whatsapp-share" href="/" class="share-btn">
				<img src="/social/whatsapp.png" alt="Whatsapp" class="w-6" />
			</a>

			<button
				on:click={() => {
					copyToClipBoard(`${$page.url.host}/hide/${gameID}`);
				}}
				class="share-btn"
			>
				<img src="/social/link.png" alt="Copy Link" class="w-6" />
			</button>
		</div>
	</div>
</div>
