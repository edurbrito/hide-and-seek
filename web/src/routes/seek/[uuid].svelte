<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import Map from './map.svelte';

	const BACKEND = import.meta.env.VITE_BACKEND
		? import.meta.env.VITE_BACKEND
		: 'http://127.0.0.1:5000';

	const uuid = $page.params.uuid;
	var game;
	var tableFound;
	var tableMissing;
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
			tableFound = document.querySelector('#hiders-container-found');
			tableMissing = document.querySelector('#hiders-container-missing');

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
							`${BACKEND}/seek/${uuid}?latitude=${currentPosition.latitude}&longitude=${currentPosition.longitude}`,
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
		let hidersFound = '';
		let hidersMissing = '';
		let found = 0;
		for (const hider in hiders) {
			if (Object.prototype.hasOwnProperty.call(hiders, hider)) {
				found += hiders[hider].found
				let opacity = hiders[hider].found ? "" : "opacity-60"
				let pill = `<div class="rounded-full bg-secondary text-white p-2 m-1 text-xs drop-shadow-md w-fit ${opacity}">${hiders[hider].username}</div>\n`
				if (hiders[hider].found) {
					hidersFound += pill
				} else {
					hidersMissing += pill
				}
			}
		}

		if (tableFound) tableFound.innerHTML = hidersFound
		if (tableMissing) tableMissing.innerHTML = hidersMissing

		document.getElementById('found').innerHTML = `${found}/${Object.keys(game.hiders).length}`;
		document.getElementById('game_id').innerHTML = game.game_id.toUpperCase();
	}

	function copyToClipBoard(text) {
		navigator.clipboard.writeText(text);
	}

	$: updateTable(game);

	let shownGameID = false;
	let shownLink = false;
</script>

<div class="scrollport w-full h-full">
	<div class="child h-full w-full relative flex flex-shrink-0 flex-col bg-primary">
		<Map {game} {currentPosition} />

		{#if shownGameID}
			<div
				id="navbar"
				class="w-fit h-fit absolute right-0 left-0 m-auto bottom-12 text-xs text-white p-2 bg-primary drop-shadow-lg"
				style="z-index: 10000002;"
				on:click={() => {
					shownGameID = false;
				}}
			>
				Copied to clipboard! Share it with your friends
			</div>
		{/if}
		<div
			id="navbar"
			class="w-full h-fit absolute bottom-0 flex flex-row text-white p-2 bg-primary"
			style="z-index: 10000000;"
		>
			<div class="w-full items-center text-center">
				<span class="text-sm font-bold">Game ID:</span>
				<span
					class="text-sm underline"
					on:click={() => {
						copyToClipBoard(game.game_id);
						shownGameID = true;
						setTimeout(() => {
							shownGameID = false;
						}, 3000);
					}}
					id="game_id"
				/>
			</div>
			<div
				class="w-full items-center text-center"
				on:click={() => {
					let toView = document.getElementById('hiders-section');
					toView.scrollIntoView();
				}}
			>
				<span class="text-sm font-bold">Found:</span>
				<span class="text-sm underline" id="found">0/0</span>
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
		class="child h-full w-full flex flex-shrink-0 sm:p-2 md:p-12 pt-4 flex-col items-center bg-primary text-white"
		id="hiders-section"
	>
		<h2 class="text-2xl text-white font-extrabold mb-2 mt-auto">HIDERS</h2>
		<hr class="w-10/12 mb-4">
		<h3 class="text-white font-extrabold mb-2 md:mt-auto text-base text-center mt-2">FOUND</h3>
		<div id="hiders-container-found" class="w-full flex justify-center flex-wrap overflow-y-scroll">
		</div>
		<hr class="w-6/12 m-4">
		<h3 class="text-white font-extrabold mb-2 md:mt-auto text-base text-center mt-2">MISSING</h3>
		<div id="hiders-container-missing" class="w-full flex justify-center flex-wrap overflow-y-scroll">
		</div>
		<hr class="w-10/12 mt-auto">
		<h3 class="text-xl text-white font-extrabold mt-2">SHARE</h3>
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
					shownLink = true;
					setTimeout(() => {
						shownLink = false;
					}, 3000);
				}}
				class="share-btn"
			>
				<img src="/social/link.png" alt="Copy Link" class="w-6" />
			</button>
		</div>
		{#if shownLink}
			<div
				id="navbar"
				class="w-fit h-fit absolute right-0 left-0 m-auto bottom-2 text-xs text-white p-2 bg-primary drop-shadow-lg"
				style="z-index: 10000002;"
				on:click={() => {
					shownLink = false;
				}}
			>
				Copied to clipboard! Share it with your friends
			</div>
		{/if}
	</div>
</div>
