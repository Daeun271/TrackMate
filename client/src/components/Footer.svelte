<script>
    import { currentTab } from '../tabs.js';
</script>

<footer>
    <button on:click={() => currentTab.set('home')}>Home</button>
    <button on:click={() => currentTab.set('exercise')}>Exercise</button>
    <button on:click={() => currentTab.set('food_intake')}>Food Intake</button>
    <button on:click={() => currentTab.set('water_intake')}>Water Intake</button
    >
    <button on:click={() => currentTab.set('community')}>Community</button>
</footer>

<style>
    footer {
        flex: 0 0 auto;
    }
</style>
