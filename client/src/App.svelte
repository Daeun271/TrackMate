<script>
    import MobileHeader from './components/MobileHeader.svelte';
    import DesktopHeader from './components/DesktopHeader.svelte';
    import MobileFooter from './components/MobileFooter.svelte';
    import DesktopFooter from './components/DesktopFooter.svelte';
    import WaterIntake from './components/pages/WaterIntake.svelte';

    import { currentTab } from './tabs.js';

    let isMobile = window.matchMedia('(max-width: 480px)').matches;
</script>

<div class="app">
    {#if isMobile}
        <MobileHeader />
    {:else}
        <DesktopHeader />
    {/if}
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
        {:else if $currentTab === 'settings'}
            Settings
        {:else}
            <p>404: Page not found</p>
        {/if}
    </main>
    {#if isMobile}
        <MobileFooter />
    {:else}
        <DesktopFooter />
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
