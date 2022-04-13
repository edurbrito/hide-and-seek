<script>
	const BACKEND = import.meta.env.VITE_BACKEND
		? import.meta.env.VITE_BACKEND
		: 'http://localhost:5000';

	let gameid = '';

	const handleSubmitButtonClick = async (event) => {
		event.preventDefault();
		await fetch(`${BACKEND}/hide/${gameid}`, { method: 'POST' })
			.then((response) => response.json())
			.then((hider) => {
				localStorage.setItem('hider', JSON.stringify(hider));
				window.location.href = `/hide/${gameid}`;
			});
	};
</script>

<div>
	<h1 class="title">Hide & Seek</h1>
	<form class="mt-3">
		<input
			bind:value={gameid}
			class="input bg-other other-text focus:outline-none focus:ring-1 focus:ring-slate-600"
			type="text"
			maxlength="6"
			size="1"
		/>
		<button
			on:click={handleSubmitButtonClick}
			class="button bg-secondary other-text"
			type="sumbit"
			disabled={!(gameid.length === 6)}
		>
			Join Game
		</button>
	</form>
</div>
