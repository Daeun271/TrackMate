<script>
    import { currentTab } from '../tabs.js';
</script>

<header>
    <button on:click={() => currentTab.set('home')}>🏠</button>
    <button on:click={() => currentTab.set('exercise')}>💪</button>
    <button on:click={() => currentTab.set('food_intake')}>🍴</button>
    <button on:click={() => currentTab.set('water_intake')}>🥛</button>
    <button on:click={() => currentTab.set('community')}>🗣</button>
    <button on:click={() => currentTab.set('settings')}>⚙️</button>
</header>

<style>
    header {
        flex: 0 0 auto;

        display: flex;
        justify-content: space-evenly;
        background-color: #f0f0f0;
        height: 50px;
    }

    button {
        font-size: 25px;
        background-color: transparent;
        border: none;
        cursor: pointer;
    }
</style>
