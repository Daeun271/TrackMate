<script>
    import Modal from '../Modal.svelte';
    export let isEditingModalOpen = false;
</script>

<Modal bind:isOpen={isEditingModalOpen}>
    <h1>Food</h1>
</Modal>
