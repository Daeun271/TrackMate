<script>
    import { createEventDispatcher } from 'svelte';

    export let isOpen = false;

    const dispatch = createEventDispatcher();

    export function setOpen(value) {
        isOpen = value;
    }

    function onClick() {
        isOpen = false;
        dispatch('close');
    }

    export let isPopup = false;
</script>

{#if isOpen}
    {#if isPopup}
        <div class="pop-up-bg"></div>
    {/if}
    <div class={isPopup ? 'pop-up' : 'modal-container'}>
        <slot name="modal-background"></slot>
        <button class="modal-close" on:click={onClick}>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="size-6"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M6 18 18 6M6 6l12 12"
                />
            </svg>
        </button>
        <div class="modal-content">
            <slot></slot>
        </div>
    </div>
{/if}

<svelte:window on:keydown={(e) => e.key === 'Escape' && isOpen && onClick()} />

<style>
    .modal-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100dvw;
        height: 100dvh;
        background-color: #fff;

        display: flex;
        flex-direction: column;

        z-index: 1000;
    }

    .pop-up-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100dvw;
        height: 100dvh;
        background-color: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(5px);

        z-index: 1500;
    }

    .pop-up {
        position: fixed;
        top: 25dvh;
        left: 10dvw;
        width: 80dvw;
        height: 50dvh;
        background-color: #fff;

        display: flex;
        flex-direction: column;

        z-index: 2000;

        border: 1px solid #8f8b8b;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    }

    .modal-close {
        margin-left: auto;
        width: 50px;
        height: 50px;
        color: #000;
        background-color: transparent;
        border: none;
        cursor: pointer;
    }

    .modal-content {
        flex: 1 1 auto;
        overflow-y: auto;
    }
</style>
