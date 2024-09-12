<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    function click() {
        dispatch('modalClick');
    }

    export let text1;
    export let text2;
    export let imageUrl;
</script>

<div class="background">
    <div class="empty-container">
        <div class="empty-container-bg-container">
            <div
                class="empty-container-bg"
                style="background:url({imageUrl}) center/cover no-repeat;"
            ></div>
        </div>
        <div class="empty-content">
            <p>{text1}</p>
            <p>{text2}</p>
            <svg
                on:click={click}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1"
                stroke="currentColor"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                />
            </svg>
        </div>
    </div>
</div>

<style>
    .background {
        display: flex;
        flex-direction: column;
        row-gap: 20px;
        overflow-y: auto;
        height: 100%;
        padding: 20px;
    }

    .empty-container {
        position: relative;
        margin-top: auto;
        margin-bottom: auto;
    }

    .empty-container-bg-container {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .empty-container-bg {
        flex: 1 0 auto;
        aspect-ratio: 1 / 1;
        max-width: 350px;
        max-height: 350px;
        opacity: 0.1;
    }

    .empty-content {
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        row-gap: 10px;
        width: 100%;
        height: 100%;
        opacity: 1;
        -webkit-text-stroke: 2px #fffa;
        paint-order: stroke fill;
    }

    .empty-content p {
        margin: 0;
        font-size: 20px;
        text-align: center;
        cursor: default;
        user-select: none;
        -webkit-user-select: none;
    }

    .empty-content svg {
        width: 100px;
        height: 100px;
        cursor: pointer;
    }
</style>
