<script>
    import {
        logoutFromCurrentDevice,
        logoutFromAllDevices,
    } from '../../user.js';
</script>

<div>
    <button on:click={async () => await logoutFromCurrentDevice()}
        >Log out from the current device</button
    >
    <button on:click={async () => await logoutFromAllDevices()}
        >Log out from all devices</button
    >
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        row-gap: 30px;
        height: 100dvh;
    }

    button {
        appearance: none;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        outline: none;
        padding: 10px 20px;
        margin-left: auto;
        margin-right: auto;
        cursor: pointer;
        font-size: 16px;
    }
</style>
