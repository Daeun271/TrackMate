<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    function onClick() {
        dispatch('click');
    }

    export let btnTxt;
</script>

<button on:click={onClick}>{btnTxt}</button>

<style>
    button {
        appearance: none;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        outline: none;
        padding: 10px 20px;
        margin: 20px 0 0 0;
        cursor: pointer;
        font-size: 16px;
    }
</style>
