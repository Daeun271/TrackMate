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
    export let widthAndHeight = '45px';

    let isMobile = window.matchMedia('(max-width: 480px)').matches;
    window.matchMedia('(max-width: 480px)').addEventListener('change', (e) => {
        isMobile = e.matches;
    });
</script>

<button
    class:button-clicked={clicked}
    class:floating-button={floated}
    class:mobile-floating-button={floated && isMobile}
    class:desktop-floating-button={floated && !isMobile}
    style:width={widthAndHeight}
    style:height={widthAndHeight}
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
        z-index: 1000;
        box-shadow: 2px 2px 3px #999;
    }

    button.mobile-floating-button {
        bottom: 70px;
        right: 20px;
    }

    button.desktop-floating-button {
        bottom: 30px;
        right: 40px;
    }

    button.floating-button.button-clicked {
        transform: none;
    }
</style>
