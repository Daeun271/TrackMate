<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let clicked = false;
    let lastTimeout = null;

    function onClick() {
        if (lastTimeout) {
            clearTimeout(lastTimeout);
        }

        clicked = true;
        dispatch('click');

        lastTimeout = setTimeout(() => {
            clicked = false;
        }, 150);
    }

    export let floated = false;

    let isMobile = window.matchMedia('(max-width: 480px)').matches;
</script>

<button
    class:button-clicked={clicked}
    class:floating-button={floated}
    style={isMobile ? 'bottom: 90px;' : 'bottom: 20px;'}
    on:click={onClick}
>
    <slot></slot>
</button>

<style>
    button {
        appearance: none;

        background-color: #007bff;
        color: white;

        display: flex;
        justify-content: center;
        align-items: center;

        width: 45px;
        height: 45px;
        padding: 0;

        border: none;
        border-radius: 50%;

        cursor: pointer;

        box-shadow: none;

        transition: all ease 0.3s;
    }

    button.button-clicked {
        background-color: #0042a2;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transform: scale(1.05);
    }

    button.floating-button {
        position: fixed;
        right: 20px;
        z-index: 1000;
        box-shadow: 2px 2px 3px #999;
    }

    button.floating-button.button-clicked {
        transform: none;
    }
</style>
