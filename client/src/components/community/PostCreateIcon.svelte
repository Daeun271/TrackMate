<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    function click() {
        dispatch('modalClick');
    }

    export let text;
</script>

<div class="empty-container">
    <p>{text}</p>
    <img
        src="images/icons8-text-50.png"
        on:click={click}
        style="width: 40px; height: 40px;"
    />
</div>

<style>
    .empty-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        row-gap: 10px;
        width: 100%;
    }

    p {
        margin: 0;
        font-size: 20px;
        text-align: center;
        cursor: default;
        user-select: none;
        -webkit-user-select: none;
    }

    img {
        width: 40px;
        height: 40px;
        cursor: pointer;
    }
</style>
