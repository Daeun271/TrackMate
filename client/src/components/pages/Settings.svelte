<script>
    import LogOut from '../auth/LogOut.svelte';

    let currentComponent = null;
</script>

<div class="background">
    <div class="wrapper">
        <button on:click={() => (currentComponent = 'Update Profile')}
            >Update Profile</button
        >
        <button on:click={() => (currentComponent = 'Set status')}
            >Set status</button
        >
        <button on:click={() => (currentComponent = 'Change password')}
            >Change password</button
        >
        <button on:click={() => (currentComponent = 'Log out')}>Log out</button>
        <button on:click={() => (currentComponent = 'Delete account')}
            >Delete account</button
        >
    </div>

    {#if currentComponent === 'Update Profile'}
        <h1>Update Profile</h1>
    {:else if currentComponent === 'Set status'}
        <h1>Set status</h1>
    {:else if currentComponent === 'Change password'}
        <h1>Change password</h1>
    {:else if currentComponent === 'Log out'}
        <LogOut />
    {:else if currentComponent === 'Delete account'}
        <h1>Delete account</h1>
    {/if}
</div>

<style>
    .background {
        display: flex;
        flex-direction: column;
        row-gap: 20px;
        height: 100dvh;
    }

    .wrapper {
        display: flex;
        flex-direction: column;
    }

    .wrapper > button {
        display: flex;
        padding: 10px;
        margin: 0;
        border-style: solid;
        border-width: 0 0 1px 0;
        border-color: #f0f0f0;
        background-color: transparent;
        color: #000;
        font-size: 18px;
        cursor: pointer;
    }

    .wrapper > button:hover {
        background-color: #f0f0f0;
    }
</style>
