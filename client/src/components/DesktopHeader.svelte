<script>
    import { currentTab } from '../tabs.js';

    const TABS = [
        { name: 'home', icon: '🏠' },
        { name: 'exercise', icon: '💪' },
        { name: 'food_intake', icon: '🍴' },
        { name: 'water_intake', icon: '🥛' },
        { name: 'community', icon: '🗣' },
        { name: 'settings', icon: '⚙️' },
    ];
</script>

<header>
    {#each TABS as tab}
        <button
            class:current={$currentTab == tab.name}
            on:click={() => currentTab.set(tab.name)}>{tab.icon}</button
        >
    {/each}
</header>

<style>
    header {
        flex: 0 0 auto;

        display: grid;
        grid-auto-columns: 1fr;
        background-color: #f0f0f0;
    }

    button {
        appearance: none;
        font-size: 20px;
        background-color: transparent;
        border: none;
        cursor: pointer;
        height: 50px;

        grid-row: 1;
    }

    .current {
        background-color: #cecccc;
    }
</style>
