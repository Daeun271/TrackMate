<script>
    import UserNameModal from '../../settings/UserNameModal.svelte';
    import EmailModal from '../../settings/EmailModal.svelte';
    import PasswordModal from '../../settings/PasswordModal.svelte';
    import LogOutModal from '../../settings/LogOutModal.svelte';
    import DeleteAccountModal from '../../settings/DeleteAccountModal.svelte';
    import Toast from '../../settings/Toast.svelte';

    let isUserNameModalOpen = false;
    let isEmailModalOpen = false;
    let isPasswordModalOpen = false;
    let isLogOutModalOpen = false;
    let isDeleteAccountModalOpen = false;

    let success = false;
    let message = '';
    let lastTimeout = null;

    function onSuccess(msg) {
        if (lastTimeout) {
            clearTimeout(lastTimeout);
        }

        message = msg;
        success = true;

        lastTimeout = setTimeout(() => {
            success = false;
            message = '';
        }, 1500);
    }
</script>

<div class="background">
    <div class="wrapper">
        <button on:click={() => (isUserNameModalOpen = true)}
            >Change user name</button
        >
        <button on:click={() => (isEmailModalOpen = true)}>Change email</button>
        <button on:click={() => (isPasswordModalOpen = true)}
            >Change password</button
        >
        <button on:click={() => (isLogOutModalOpen = true)}>Log out</button>
        <button on:click={() => (isDeleteAccountModalOpen = true)}
            >Delete account</button
        >
    </div>
    <Toast {success} {message}></Toast>
</div>

<UserNameModal
    bind:isOpen={isUserNameModalOpen}
    on:success={(event) => {
        onSuccess(event.detail.message);
    }}
></UserNameModal>
<EmailModal
    bind:isOpen={isEmailModalOpen}
    on:success={(event) => {
        onSuccess(event.detail.message);
    }}
></EmailModal>
<PasswordModal
    bind:isOpen={isPasswordModalOpen}
    on:success={(event) => {
        onSuccess(event.detail.message);
    }}
></PasswordModal>
<LogOutModal bind:isOpen={isLogOutModalOpen}></LogOutModal>
<DeleteAccountModal bind:isOpen={isDeleteAccountModalOpen}></DeleteAccountModal>

<style>
    .background {
        display: flex;
        flex-direction: column;
        row-gap: 20px;

        height: 100%;
        position: relative;
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
