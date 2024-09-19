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
    export let primaryBordered = false;
    export let secondaryBordered = false;
    export let isRound = false;
</script>

<button
    class="component-button"
    class:button-clicked={clicked}
    class:expanded={isExpanded}
    class:loading={isLoading}
    class:primary-border={primaryBordered}
    class:secondary-border={secondaryBordered}
    class:round={isRound}
    style="background-color: {backgroundColor}"
    on:click={onClick}><slot></slot></button
>

<style>
    .component-button {
        appearance: none;

        color: white;

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

    .primary-border {
        border: 2px solid #007bff;
        color: #007bff;
    }

    .secondary-border {
        border: 2px solid #f50707;
        color: #f50707;
    }

    .round {
        border-radius: 20px;
    }
</style>
