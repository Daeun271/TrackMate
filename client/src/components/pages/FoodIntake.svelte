<script>
    import AddingModal from '../food_intakes/AddingModal.svelte';
    import EditingModal from '../food_intakes/EditingModal.svelte';

    let addingModalOpen = false;
    let showingModalOpen = false;

    let timeCategory = '';

    $: today = new Date().toISOString().split('T')[0];
</script>

<div class="background">
    <h1>26.06.24</h1>
    <div class="foodintake-wrapper">
        <img
            src="https://www.einfachkochen.de/sites/einfachkochen.de/files/styles/full_width_tablet_4_3/public/2023-01/2023_hamburger_aufmacher.jpg?h=6eb229a4&itok=AHgcUVO2"
            alt="food"
            on:click={() => (showingModalOpen = true)}
        />
        <div class="add-wrapper">
            <svg
                on:click={() => (addingModalOpen = true)}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1"
                stroke="currentColor"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                />
            </svg>
        </div>
    </div>

    <AddingModal bind:isAddingModalOpen={addingModalOpen} />
    <EditingModal bind:isEditingModalOpen={showingModalOpen} />
</div>

<style>
    .background {
        display: flex;
        flex-direction: column;
        row-gap: 20px;
        overflow-y: auto;
        height: 100%;
        padding: 20px;
    }

    .background > h1 {
        margin: 0;
        font-size: 30px;
    }

    .foodintake-wrapper {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        grid-auto-rows: 100px;
        gap: 20px;
    }

    .foodintake-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        cursor: pointer;
    }

    .add-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        border: none;
    }

    .add-wrapper > svg {
        width: 50px;
        height: 50px;
        cursor: pointer;
    }
</style>
