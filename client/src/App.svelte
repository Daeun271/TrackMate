<script>
    import DesktopHeader from './components/DesktopHeader.svelte';
    import MobileFooter from './components/MobileFooter.svelte';
    import WaterIntake from './components/pages/WaterIntake.svelte';
    import Settings from './components/pages/Settings.svelte';
    import LogInUp from './components/auth/LogInUp.svelte';
    import FoodIntake from './components/pages/FoodIntake.svelte';
    import Exercise from './components/pages/Exercise.svelte';
    import Community from './components/pages/Community.svelte';
    import Home from './components/pages/Home.svelte';

    import { currentTab } from './tabs.js';
    import { user } from './user.js';

    let isMobile = window.matchMedia('(max-width: 480px)').matches;
    window.matchMedia('(max-width: 480px)').addEventListener('change', (e) => {
        isMobile = e.matches;
    });
</script>

<div class="app">
    {#if $user}
        {#if !isMobile}
            <DesktopHeader />
        {/if}
        <main>
            {#if $currentTab === 'home'}
                <Home />
            {:else if $currentTab === 'exercise'}
                <Exercise />
            {:else if $currentTab === 'food_intake'}
                <FoodIntake />
            {:else if $currentTab === 'water_intake'}
                <WaterIntake />
            {:else if $currentTab === 'community'}
                <Community />
            {:else if $currentTab === 'settings'}
                <Settings />
            {:else}
                <p>404: Page not found</p>
            {/if}
        </main>
        {#if isMobile}
            <MobileFooter />
        {/if}
    {:else}
        <LogInUp />
    {/if}
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
