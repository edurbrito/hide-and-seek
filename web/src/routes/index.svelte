<script lang="ts">
	import { v4 as uuidv4 } from 'uuid';

	function seek() {
		let uuid = uuidv4()
		window.location.href = `/seek/${uuid}/`;
	}
</script>

<div class="flex flex-col justify-center items-center w-full h-full">
	<h1 class="font-bold w-fit text-4xl uppercase text-white">Hide & Seek</h1>
	<div class="inline-flex mt-12 gap-2">
		<a href="/hide"
			><button
				class="bg-secondary hover:bg-secondary text-white font-bold py-2 px-4 border-b-4 rounded"
			>
				Hide
			</button></a
		>
		<button
			class="bg-secondary hover:bg-secondary text-white font-bold py-2 px-4 border-b-4 rounded"
			on:click={seek}
		>
			Seek
		</button>
	</div>
</div>
