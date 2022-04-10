<script>
    import { onMount } from 'svelte';

    let gameid = ''
    let distance = '0'

    onMount(() => {
        gameid = localStorage.getItem('gameid')
        distance = localStorage.getItem('distance')
    })
</script>

<span class="mb-5 font-semibold">Username</span>
<div class="game-circle">
    <span class="text-lg">Game ID</span>
    <span class="text-2xl font-bold">{gameid}</span>
</div>
<span class="mt-5 text-center text-lg">The Seeker is {Math.round(Number(distance))} meters from you!</span>