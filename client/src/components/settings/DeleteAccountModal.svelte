<script>
    import Modal from '../Modal.svelte';
    import Button from '../Button.svelte';
    import Loader from '../Loader.svelte';
    import { validatePassword } from './user-field-validator';
    import { deleteUserAccount } from '../../api';
    import { user } from '../../user';
    import { currentTab } from '../../tabs';

    let password = '';
    let isLoading = false;
    let errorMessage = '';
    let shouldBeValidated = true;
    let isLoading2 = false;
    let errorMessage2 = '';

    export let isOpen = false;

    export async function validateUserPassword() {
        if (isLoading) {
            return;
        }
        isLoading = true;

        if (password.trim() === '') {
            errorMessage = 'Password cannot be empty';
            isLoading = false;
            shouldBeValidated = true;
            return;
        }

        try {
            const isValidPassword = await validatePassword(password);

            if (!isValidPassword) {
                errorMessage = 'An error occurred. Please try again';
                isLoading = false;
                shouldBeValidated = true;
                return;
            }
        } catch (error) {
            if (error.message === 'invalid password') {
                errorMessage = 'Please enter a valid password';
            } else if (error.message === 'wrong password') {
                errorMessage = 'Wrong password. Please try again';
            } else {
                errorMessage = 'An error occurred. Please try again';
            }
            isLoading = false;
            shouldBeValidated = true;
            return;
        }

        isLoading = false;
        errorMessage = '';
        shouldBeValidated = false;
    }

    async function removeAccount() {
        if (isLoading2) {
            return;
        }
        isLoading2 = true;

        try {
            await deleteUserAccount();
        } catch (error) {
            errorMessage2 = 'An error occurred. Please try again';
            isLoading2 = false;
            return;
        }

        isLoading2 = false;
        shouldBeValidated = true;
        errorMessage2 = '';
        isOpen = false;

        localStorage.clear();
        user.set(null);
        currentTab.set('home');

        isLoading2 = false;
        errorMessage2 = '';
        shouldBeValidated = true;
    }
</script>

<Modal
    bind:isOpen
    isPopup={true}
    on:close={() => {
        isLoading = false;
        isLoading2 = false;
        password = '';
        errorMessage = '';
        errorMessage2 = '';
        shouldBeValidated = true;
    }}
>
    <div class="modal-wrapper">
        <div class="input-container">
            {#if shouldBeValidated}
                <label for="password"
                    >Current Password<span class="required">*</span></label
                >
                <input
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Enter your current password to confirm"
                    bind:value={password}
                />

                <Button
                    bind:isLoading
                    isExpanded={true}
                    on:click={validateUserPassword}
                >
                    {#if isLoading}
                        <Loader></Loader>
                    {:else}
                        <span>Confirm</span>
                    {/if}
                </Button>
                <p class="error-message">{errorMessage}</p>
            {:else}
                <p style="font-size:18px;">
                    Are you sure you want to delete your account?
                </p>
                <Button
                    isExpanded={true}
                    backgroundColor="#f50707"
                    on:click={removeAccount}
                >
                    {#if isLoading2}
                        <Loader></Loader>
                    {:else}
                        <span>Delete Account</span>
                    {/if}
                </Button>
                <p class="error-message">{errorMessage2}</p>
            {/if}
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
