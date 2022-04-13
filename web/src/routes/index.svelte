<script lang="ts">
	async function seek() {
		await fetch(`http://localhost:5000/seek`, { method: 'POST' })
			.then((response) => response.json())
			.then((game) => {
				localStorage.setItem('game', JSON.stringify(game));
				window.location.href = `/seek/${game.uuid}/`;
			});
	}
</script>

<div>
	<h1 class="title">Hide & Seek</h1>
	<div class="mt-5 flex actions-container">
		<a href="/hide" class="link bg-secondary other-text" type="button">Hide</a>
		<button class="button bg-secondary other-text" type="button" on:click={seek}>Seek</button>
	</div>
</div>
