<script>
    import UserNameModal from '../../settings/UserNameModal.svelte';
    import EmailModal from '../../settings/EmailModal.svelte';
    import PasswordModal from '../../settings/PasswordModal.svelte';
    import LogOutModal from '../../settings/LogOutModal.svelte';
    import DeleteAccountModal from '../../settings/DeleteAccountModal.svelte';

    let isUserNameModalOpen = false;
    let isEmailModalOpen = false;
    let isPasswordModalOpen = false;
    let isLogOutModalOpen = false;
    let isDeleteAccountModalOpen = false;
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
</div>

<UserNameModal bind:isOpen={isUserNameModalOpen}></UserNameModal>
<EmailModal bind:isOpen={isEmailModalOpen}></EmailModal>
<PasswordModal bind:isOpen={isPasswordModalOpen}></PasswordModal>
<LogOutModal bind:isOpen={isLogOutModalOpen}></LogOutModal>
<DeleteAccountModal bind:isOpen={isDeleteAccountModalOpen}></DeleteAccountModal>

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
