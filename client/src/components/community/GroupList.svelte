<script>
    import { createEventDispatcher } from 'svelte';
    import { buttonClick } from '../../button_click';

    const dispatch = createEventDispatcher();

    let isOpen = false;
    export let isListOpen;

    $: {
        if (!isListOpen) {
            isOpen = false;
        }
    }

    export let groupName = '';
    export let members = [];
</script>

<details
    on:toggle={() => {
        if (isListOpen) {
            isOpen = !isOpen;
            if (isOpen) {
                dispatch('open');
            }
        }
    }}
    bind:open={isOpen}
>
    <summary><span>{groupName}</span></summary>
    <div class="group-members">
        {#each members as member}
            <p>{member}</p>
        {/each}
        <span
            use:buttonClick
            on:click={() => {
                dispatch('move');
            }}
            class="link">Go to the group</span
        >
    </div>
</details>

<style>
    details {
        width: 100%;

        font-size: 16px;
        text-align: left;
        color: #000;
    }

    details[open] {
        background-color: #f4f4f4;
    }

    summary {
        height: 30px;
        padding: 5px 10px;

        background-color: #f4f4f4;

        cursor: pointer;
        list-style: none;
    }

    details[open] > summary {
        background-color: #e7e7e7;
    }

    .group-members {
        display: flex;
        flex-direction: column;
        row-gap: 10px;
        padding: 10px;
    }

    p {
        margin: 0;
    }

    .link {
        text-align: center;
        color: #007bff;
        font-size: 14px;
        text-decoration: underline;

        cursor: pointer;
    }

    .link:global(.clicked) {
        color: #0056b3;
    }
</style>
