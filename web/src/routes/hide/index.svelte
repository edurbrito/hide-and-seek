<script lang="ts">
	let gameID : string = ""

	function redirect(event) {
		if (gameID.length == 6)
			window.location.href = `/hide/${gameID}`
	}
</script>

<div class="flex flex-col items-center justify-center w-full h-full align-middle gap-2 p-4">
	<h1 class="font-bold w-fit text-4xl uppercase text-white mb-4">Hide & Seek</h1>
	<input
		type="text"
		minlength="6"
		maxlength="6"
		name="pin-code"
		id="pin-code"
		placeholder="XXXXXX"
		class="w-1/2 bg-other font-bold text-white placeholder-white rounded py-2 px-4 text-center"
		bind:value={gameID}
	/>
	<button
		class="w-1/2 bg-secondary text-white font-bold py-2 px-4 border-b-4 rounded"
		type="button"
		on:click={redirect}>Join Game
	</button>
</div>
