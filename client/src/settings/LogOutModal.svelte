<script>
    import Modal from '../components/Modal.svelte';
    import Button from '../components/Button.svelte';
    import { logoutFromCurrentDevice, logoutFromAllDevices } from '../user.js';
    import { currentTab } from '../tabs.js';

    export let isOpen = false;
</script>

<Modal bind:isOpen isPopup={true}>
    <div class="modal-wrapper">
        <div class="input-container">
            <div class="button-container">
                <p>Select the option you want to log out from:</p>
                <Button
                    isExpanded={false}
                    on:click={async () => {
                        await logoutFromCurrentDevice();
                        currentTab.set('home');
                    }}
                >
                    <span>Current Device</span>
                </Button>
                <Button
                    isExpanded={false}
                    on:click={async () => {
                        await logoutFromAllDevices();
                        currentTab.set('home');
                    }}
                >
                    <span>All Devices</span>
                </Button>
            </div>
        </div>
    </div>
</Modal>

<style>
    .modal-wrapper {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    .input-container {
        display: flex;
        flex-direction: column;
        width: 90%;
        padding-bottom: 20px;
    }

    .button-container {
        display: flex;
        flex-direction: column;
        row-gap: 30px;
    }

    p {
        margin: 0;
        font-size: 20px;
    }
</style>
