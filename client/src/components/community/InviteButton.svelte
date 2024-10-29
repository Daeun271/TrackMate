<script>
    import { buttonClick } from '../../button_click';
    import InviteToast from './InviteToast.svelte';

    let linkCopied = false;
    let lastTimeout = null;

    function onClick() {
        if (lastTimeout) {
            clearTimeout(lastTimeout);
        }

        linkCopied = true;

        lastTimeout = setTimeout(() => {
            linkCopied = false;
        }, 1500);
    }

    export let groupCode = '';
</script>

<button
    class="invite-btn"
    use:buttonClick
    on:click={() => {
        navigator.clipboard
            .writeText(window.location.href + '?inviteCode=' + groupCode)
            .then(() => {
                onClick();
            });
    }}>Invite Friends</button
>

<InviteToast {linkCopied} />

<style>
    .invite-btn {
        width: 130px;
        height: 30px;
        padding: 5px 20px;
        margin-top: auto;
        margin-bottom: auto;
        border: none;
        border-radius: 5px;
        color: #000;
        background-color: #f0f0f0;
        appearance: none;
        cursor: pointer;
    }

    .invite-btn:global(.clicked) {
        background-color: #c9c7c7;
    }
</style>
