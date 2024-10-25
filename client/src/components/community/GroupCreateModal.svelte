<script>
    import Modal from '../Modal.svelte';
    import Button from '../Button.svelte';
    import Loader from '../Loader.svelte';
    import { createGroup } from '../../api';
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let name = '';
    export let isModalOpen = false;
    let isLoading = false;
    let errorMessage = '';

    let newGroup = {};
    async function createUserGroup() {
        if (isLoading) return;
        isLoading = true;

        if (name.trim() === '') {
            errorMessage = 'Name is required';
            isLoading = false;
            return;
        }

        try {
            newGroup = await createGroup(name);
        } catch (error) {
            errorMessage = 'An error occurred. Please try again later.';
            isLoading = false;
            return;
        }

        isLoading = false;
        dispatch('add', newGroup);
        isModalOpen = false;
        errorMessage = '';
        name = '';
    }
</script>

<Modal
    bind:isOpen={isModalOpen}
    on:close={() => {
        errorMessage = '';
        name = '';
    }}
    isPopup={true}
>
    <div class="modal-wrapper">
        <div class="input-container">
            <label for="name">Name<span class="required">*</span></label>
            <input type="text" id="name" name="name" bind:value={name} />

            <Button bind:isLoading on:click={createUserGroup} isExpanded={true}>
                {#if isLoading}
                    <Loader></Loader>
                {:else}
                    <span>Create</span>
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
