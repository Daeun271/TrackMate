<script>
    import Header from './components/Header.svelte';
    import Footer from './components/Footer.svelte';
    import WaterIntake from './components/pages/WaterIntake.svelte';

    import { currentTab } from './tabs.js';
</script>

<div class="app">
    <Header />
    <main>
        {#if $currentTab === 'home'}
            Home
        {:else if $currentTab === 'exercise'}
            Exercise
        {:else if $currentTab === 'food_intake'}
            Food Intake
        {:else if $currentTab === 'water_intake'}
            <WaterIntake />
        {:else if $currentTab === 'community'}
            Community
        {:else}
            <p>404: Page not found</p>
        {/if}
    </main>
    <Footer />
</div>

<style>
    .app {
        display: flex;
        flex-direction: column;
        height: 100dvh;
    }

    main {
        flex: 1 1 auto;
        overflow-y: auto;
    }
</style>
