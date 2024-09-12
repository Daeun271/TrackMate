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

    export let isExpanded = true;
    export let isLoading = false;
    export let backgroundColor = '#007bff';
    export let bordered = false;
</script>

<button
    class="component-button"
    class:button-clicked={clicked}
    class:expanded={isExpanded}
    class:loading={isLoading}
    class:bordered
    style:background-color={backgroundColor}
    on:click={onClick}><slot></slot></button
>

<style>
    .component-button {
        appearance: none;

        color: white;
        background-color: #007bff;

        border: none;
        border-radius: 5px;
        outline: none;

        cursor: pointer;

        font-size: 16px;

        height: 40px;
        padding: 10px 20px;
    }

    .button-clicked {
        background-color: #0042a2;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .expanded {
        width: 100%;
    }

    .loading {
        cursor: none;
        pointer-events: none;
    }

    .bordered {
        border: 2px solid #007bff;
        background-color: white;
        color: #007bff;
    }
</style>
