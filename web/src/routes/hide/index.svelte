<script>
    let userData = {}
    let gameid = ''

    const handleSubmitButtonClick = async (event) => {
        event.preventDefault()
        await fetch(`http://localhost:5000/hide/${gameid}`, {method: "POST"})
            .then((response) => response.json())
            .then(obj => {
                userData = obj 
            })

        await fetch(`http://localhost:5000/hider/${gameid}?uuid=${userData.uuid}&latitude=30.001&longitude=20.001`, {method: "POST"})
            .then((response) => response.json())
            .then(obj => localStorage.setItem('distance', obj.distance))
        
        localStorage.setItem('gameid', gameid)

        window.location.href = `/hide/${gameid}?uuid=${userData.uuid}&latitude=30.001&longitude=20.001`
    }
</script>

<div>
	<h1 class="title">Hide & Seek</h1>
    <form class="mt-3">
        <input bind:value={gameid} class="input bg-other other-text focus:outline-none focus:ring-1 focus:ring-slate-600" type="text" maxlength="6" size="1">
        <button on:click={handleSubmitButtonClick} class="button bg-secondary other-text" type="sumbit" disabled={!(gameid.length === 6)}>
            Join Game
        </button>
    </form>
</div>