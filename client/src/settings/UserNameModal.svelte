<script>
    import Modal from '../components/Modal.svelte';
    import Button from '../components/Button.svelte';
    import Loader from '../components/Loader.svelte';
    import { getUserName, updateUserName } from '../api';

    let name = '';
    let userName = '';
    let isLoading = false;
    let errorMessage = '';

    export let isOpen = false;

    async function getName() {
        const res = await getUserName();
        userName = res.user_name;
        name = res.user_name;
    }

    $: {
        if (isOpen) {
            getName();
        }
    }

    async function updateName() {
        if (isLoading) {
            return;
        }
        isLoading = true;

        if (name.trim() === '') {
            errorMessage = 'Name cannot be empty';
            isLoading = false;
            return;
        }

        if (name === userName) {
            errorMessage = 'Please enter a new name';
            isLoading = false;
            return;
        }

        try {
            const res = await updateUserName(name);
            userName = res.user_name;
            name = res.user_name;
        } catch (error) {
            errorMessage = 'Failed to update name. Please try again';
            isLoading = false;
            return;
        }

        isOpen = false;
        isLoading = false;
        errorMessage = '';
    }
</script>

<Modal
    bind:isOpen
    isPopup={true}
    on:close={async () => {
        isOpen = false;
        isLoading = false;
        errorMessage = '';
    }}
>
    <div class="modal-wrapper">
        <div class="input-container">
            <label for="name">Name<span class="required">*</span></label>
            <input
                type="text"
                id="name"
                name="name"
                placeholder="Enter your new name"
                bind:value={name}
            />

            <Button bind:isLoading isExpanded={true} on:click={updateName}>
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
