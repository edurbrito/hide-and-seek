<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import Map from './map.svelte';

	const BACKEND = import.meta.env.VITE_BACKEND
		? import.meta.env.VITE_BACKEND
		: 'http://127.0.0.1:5000';

	const uuid = $page.params.uuid;
	var game;
	var table;
	var currentPosition = {
		latitude: 0,
		longitude: 0
	};
	var timer = '30';

	const options = {
		enableHighAccuracy: true,
		maximumAge: 5000,
		timeout: 2000
	};

	onMount(() => {
		game = JSON.parse(localStorage.getItem('game'));

		if ('geolocation' in navigator) {
			table = document.querySelector('#hiders');

			getCurrentPosition();
			setInterval(getCurrentPosition, 30000);

			setInterval(() => {
				let _timer = parseInt(timer) - 1;
				if (_timer <= 0) {
					_timer = 30;
				}

				if (_timer < 10) {
					timer = `0${_timer}`;
				} else {
					timer = `${_timer}`;
				}
			}, 1000);

			let shareUrl = `${$page.url.host}/hide/${game.game_id}`;
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

			function getCurrentPosition() {
				navigator.geolocation.getCurrentPosition(
					async (position) => {
						currentPosition = {
							latitude: position.coords.latitude,
							longitude: position.coords.longitude
						};
						console.log('watch current position', currentPosition);

						await fetch(
							`${BACKEND}/seek/${uuid}?latitude=${
								currentPosition.latitude
							}&longitude=${currentPosition.longitude}`,
							{ method: 'POST' }
						)
							.then((response) => response.json())
							.then((response) => {
								game = response;
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
		} else {
			document.getElementById('warning').style.setProperty('display', 'flex');
		}
	});

	function updateTable(game) {
		if (!game) return;
		let hiders = game.hiders;
		let result = '';
		let found = 0;
		for (const hider in hiders) {
			if (Object.prototype.hasOwnProperty.call(hiders, hider)) {
				found += hiders[hider].found;
				let sfound = hiders[hider].found ? 'Yaaa 🤟' : 'Noo 👀';
				let coordinates = hiders[hider].found
					? `lat: ${hiders[hider].latitude}, lon: ${hiders[hider].longitude}`
					: '';

				result += `<tr class="bg-secondary table-border w-full flex flex-row">
				<td class="table-border py-2 text-center text-xs w-1/3">${hiders[hider].username}</td>
				<td class="table-border py-2 text-center text-xs w-1/3">${sfound}</td>
				<td class="table-border py-2 text-center text-xs w-1/3">${coordinates}</td>
				</tr>`;
			}
		}

		if (table) table.innerHTML = result;

		document.getElementById('found').innerHTML = `${found}/${Object.keys(game.hiders).length}`;
		document.getElementById('game_id').innerHTML = game.game_id.toUpperCase();
	}

	function copyToClipBoard(text) {
		navigator.clipboard.writeText(text);
	}

	$: updateTable(game);
</script>

<div class="scrollport w-screen h-screen">
	<div class="child h-full w-full relative flex flex-shrink-0 flex-col bg-primary">
		<Map {game} {currentPosition} />
		<div
			id="navbar"
			class="w-full h-fit absolute bottom-0 flex flex-row text-white p-2 bg-primary"
			style="z-index: 10000000;"
		>
			<div class="w-full items-center text-center">
				<span class="text-sm font-bold">Game ID:</span>
				<span
					class="text-sm"
					on:click={() => {
						copyToClipBoard(game.game_id);
					}}
					id="game_id"
				/>
			</div>
			<div class="w-full items-center text-center">
				<span class="text-sm font-bold">Found:</span>
				<span class="text-sm" id="found">0/0</span>
			</div>
			<div class="w-auto items-center text-center justify-center flex flex-col pr-1">
				<img
					src="/map/refresh.png"
					style="width: auto; height: 80%;"
					class="absolute"
					alt="refresh"
				/>
				<span class="font-base" style="font-size: 0.75em;">{timer}</span>
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
					copyToClipBoard(`${$page.url.host}/hide/${game.game_id}`);
				}}
				class="share-btn"
			>
				<img src="/social/link.png" alt="Copy Link" class="w-6" />
			</button>
		</div>
	</div>
</div>
