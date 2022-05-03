<script>
	const BACKEND = import.meta.env.VITE_BACKEND
		? import.meta.env.VITE_BACKEND
		: 'http://localhost:5000';

	let gameid = '';

	const handleSubmitButtonClick = async (event) => {
		event.preventDefault();
		await fetch(`${BACKEND}/hide/${gameid}`, { method: 'POST' })
			.then((response) => {
				if (!response.ok) {
					throw Error(response.statusText);
				}
				return response.json();
			})
			.then((hider) => {
				localStorage.setItem('hider', JSON.stringify(hider));
				window.location.href = `/hide/${gameid}`;
			}).catch(function(error) {
				console.log(error);
				document.getElementById("errors").hidden = false;
			});
	};
</script>

<div>
	<h1 class="title">Hide & Seek</h1>
	<form class="mt-3 flex flex-col items-center">
		<input
			bind:value={gameid}
			class="input bg-other other-text placeholder:text-white"
			type="text"
			maxlength="6"
			size="1"
			placeholder="GAME ID"
		/>
		<button
			on:click={handleSubmitButtonClick}
			class="button bg-secondary other-text hover:bg-gray-600 active:bg-gray-700 focus:outline-none drop-shadow-lg"
			type="sumbit"
			disabled={!(gameid.length === 6)}
		>
			Join Game
		</button>
		<span id="errors" class="text-xs mt-3" hidden>That's an invalid game ID 😕...</span>
	</form>
</div>
