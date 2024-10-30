<script>
    import Modal from '../components/Modal.svelte';
    import Button from '../components/Button.svelte';
    import Loader from '../components/Loader.svelte';

    let email = '';
    let isLoading = false;
    let errorMessage = '';

    export let isOpen = false;
</script>

<Modal bind:isOpen isPopup={true}>
    <div class="modal-wrapper">
        <div class="input-container">
            <label for="email">New Email<span class="required">*</span></label>
            <input
                type="email"
                id="email"
                name="email"
                placeholder="Enter your new email"
                bind:value={email}
            />

            <Button bind:isLoading isExpanded={true}>
                {#if isLoading}
                    <Loader></Loader>
                {:else}
                    <span>Change</span>
                {/if}
            </Button>
            <p class="error-message">{errorMessage}</p>
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

    .input-container label {
        font-size: 20px;
        margin: 10px 0 5px 0;
        width: 100%;
        text-align: left;
        pointer-events: none;
    }

    .input-container input {
        width: 100%;
        height: 40px;
        padding: 10px;
        margin-bottom: 20px;
        border: 1px solid #ced4da;
        border-radius: 5px;
        outline: solid 2px #f8f8f8;
        font-size: 18px;
        color: #000;
        background-color: #fff;
    }

    .required {
        color: #f50707;
        margin-left: 5px;
    }

    .error-message {
        color: #f50707;
        font-size: 15px;
        margin: 5px 0 5px 0;
    }
</style>
