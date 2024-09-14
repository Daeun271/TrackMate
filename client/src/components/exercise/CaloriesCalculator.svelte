<script>
    import Modal from '../../components/Modal.svelte';

    export let isPopupOpen = false;
</script>

<Modal bind:isOpen={isPopupOpen} isPopup={true}></Modal>
