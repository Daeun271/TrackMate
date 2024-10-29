<script>
    import {
        logoutFromCurrentDevice,
        logoutFromAllDevices,
    } from '../../user.js';
    import Button from '../Button.svelte';
    import { currentTab } from '../../tabs.js';
</script>

<div>
    <Button
        isExpanded={false}
        on:click={async () => {
            await logoutFromCurrentDevice();
            currentTab.set('home');
        }}
    >
        <span>Log out from the current device</span>
    </Button>
    <Button
        isExpanded={false}
        on:click={async () => {
            await logoutFromAllDevices();
            currentTab.set('home');
        }}
    >
        <span>Log out from all devices</span>
    </Button>
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        align-items: center;
        row-gap: 30px;
        height: 100dvh;
    }
</style>
