<script lang="ts">
	const BACKEND = import.meta.env.VITE_BACKEND
		? import.meta.env.VITE_BACKEND
		: 'http://127.0.0.1:5000';

	async function seek() {
		await fetch(`${BACKEND}/seek`, { method: 'POST' })
			.then((response) => response.json())
			.then((game) => {
				localStorage.setItem('game', JSON.stringify(game));
				window.location.href = `/seek/${game.uuid}/`;
			});
	}

	function hide() {
		window.location.href = "/hide"
	}
</script>

<div class="w-full h-full flex flex-col items-center justify-center">
	<h1 class="title mt-auto">Hide & Seek</h1>
	<div class="mt-5 flex actions-container">
		<button class="button bg-secondary other-text hover:bg-gray-600 active:bg-gray-700 focus:outline-none drop-shadow-lg" type="button" on:click={hide}>Hide</button>
		<button class="button bg-secondary other-text hover:bg-gray-600 active:bg-gray-700 focus:outline-none drop-shadow-lg" type="button" on:click={seek}>Seek</button>
	</div>
	<div class="text-xs mt-auto w-full flex flex-row mb-4 items-center justify-center">
		🤟 SPM 2022 • Group Iron Man <img src="/logo.png" alt="team icon" style="width: 1em; height: 1em;" class="mx-1"></div>
</div>
