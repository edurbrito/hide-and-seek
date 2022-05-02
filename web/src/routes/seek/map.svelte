<script lang="ts" defer>
	import { afterUpdate } from 'svelte';

	export var currentPosition, game;

	var map;

	afterUpdate(async () => {
		let hiders;
		try {
			hiders = game.hiders;
		} catch (error) {}
		
		const L = await import('leaflet');

		let container = L.DomUtil.get('map');
		if (container != null) {
			container._leaflet_id = null;
		}

		map = L.map('map').setView([currentPosition.latitude, currentPosition.longitude], 13);
		map._handlers.forEach(function (handler) {
			handler.disable();
		});

		L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
			attribution: `&copy;<a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>,
				&copy;<a href="https://carto.com/attributions" target="_blank">CARTO</a>`,
			subdomains: 'abcd',
			maxZoom: 16
		}).addTo(map);

		var seekerIcon = L.icon({
			iconUrl: '/map/seeker.png',
			shadowUrl: '/map/shadow.png',
			iconSize: [32, 32], // size of the icon
			shadowSize: [32, 32], // size of the shadow
			iconAnchor: [0, -16], // point of the icon which will correspond to marker's location
			shadowAnchor: [-8, -16], // the same for the shadow
			popupAnchor: [0, -18] // point from which the popup should open relative to the iconAnchor
		});

		var hiderIcon = L.icon({
			iconUrl: '/map/hider.png',
			// shadowUrl: '/map/shadow.png',
			iconSize: [32, 32], // size of the icon
			// shadowSize:   [32, 32], // size of the shadow
			iconAnchor: [16, 32], // point of the icon which will correspond to marker's location
			// shadowAnchor: [8, 32],  // the same for the shadow
			popupAnchor: [0, -32] // point from which the popup should open relative to the iconAnchor
		});

		for (const hider in hiders) {
			if (Object.prototype.hasOwnProperty.call(hiders, hider)) {
				if (!hiders[hider].found) {
					let colour = stringToColour(hider);
					let circle = L.circle([hiders[hider].latitude, hiders[hider].longitude], {
						color: colour,
						fillColor: colour,
						fillOpacity: 0.5,
						radius: 500
					}).addTo(map);
				} else {
					let marker = L.marker([hiders[hider].latitude, hiders[hider].longitude], {
						icon: hiderIcon
					}).addTo(map);
					marker.bindPopup(hiders[hider].username);
				}
			}
		}

		let marker = L.marker(
			[currentPosition.latitude, currentPosition.longitude]
			// {icon: seekerIcon}
		).addTo(map);
		marker.bindPopup('This is You!');
	});

	function stringToColour(string) {
		return '#' + parseInt(string, 36).toString(16).slice(0, 6).toUpperCase();
	}
</script>

<svelte:head>
	<link
		rel="stylesheet"
		href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
		integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
		crossorigin=""
	/>
</svelte:head>

<div id="map" class="w-screen h-screen" style="z-index: 10000;"/>
