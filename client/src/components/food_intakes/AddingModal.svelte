<script>
    import Modal from '../Modal.svelte';

    export let isAddingModalOpen = false;
    const today = new Date().toISOString().split('T')[0];

    function getInitialInputs() {
        return {
            imageUrl: '',
            name: '',
            calories: '',
            date: today,
            timeCategory: '',
        };
    }

    let userInputs = getInitialInputs();

    let imageInput;

    function uploadImage(event) {
        const file = event.target.files[0];

        userInputs.imageUrl = window.URL.createObjectURL(file);
    }

    function handleMaxDate(event) {
        new Date(event.target.value) > new Date()
            ? (event.target.value = today)
            : event.target.value;
        userInputs.date = event.target.value;
    }
</script>

<Modal
    bind:isOpen={isAddingModalOpen}
    on:close={() => {
        userInputs = getInitialInputs();
    }}
>
    <div class="modal-wrapper">
        <div class="input-container">
            <label for="image">Image</label>
            <input
                bind:this={imageInput}
                on:change={uploadImage}
                type="file"
                id="image"
                name="image"
                accept="image/*"
                style="display:none;"
            />
            <div class="image-preview" on:click={() => imageInput.click()}>
                {#if userInputs.imageUrl}
                    <img src={userInputs.imageUrl} />
                {:else}
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M6.827 6.175A2.31 2.31 0 0 1 5.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 0 0-1.134-.175 2.31 2.31 0 0 1-1.64-1.055l-.822-1.316a2.192 2.192 0 0 0-1.736-1.039 48.774 48.774 0 0 0-5.232 0 2.192 2.192 0 0 0-1.736 1.039l-.821 1.316Z"
                        />
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M16.5 12.75a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0ZM18.75 10.5h.008v.008h-.008V10.5Z"
                        />
                    </svg>
                {/if}
            </div>
            <label for="name">Name</label>
            <input
                type="text"
                id="name"
                name="name"
                bind:value={userInputs.name}
            />
            <label for="calories">Calories</label>
            <input
                type="number"
                pattern="[0-9]*"
                id="calories"
                name="calories"
                onkeypress="return event.charCode >= 48 && event.charCode <= 57"
                oninput="this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');"
                bind:value={userInputs.calories}
            />
            <label for="date">Date</label>
            <input
                type="date"
                id="date"
                name="date"
                max={today}
                on:change={handleMaxDate}
                value={today}
            />
            <label for="category">Category</label>
            <select
                id="category"
                name="category"
                bind:value={userInputs.timeCategory}
            >
                <option hidden disabled selected value>
                    -- select an option --
                </option>
                <option value="BREAKFAST">Breakfast</option>
                <option value="LUNCH">Lunch</option>
                <option value="DINNER">Dinner</option>
                <option value="DESSERT">Dessert</option>
                <option value="NIGHT_SNACK">Night snack</option>
            </select>
            <button on:click={() => console.log(userInputs)}>Add</button>
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
        width: min(calc(100dvw - 40px), 400px);
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
        margin-bottom: 10px;
        border: 1px solid #ced4da;
        border-radius: 5px;
        outline: solid 2px #f8f8f8;
        font-size: 18px;
        color: #000;
        background-color: #fff;
    }

    input[type='number'] {
        -moz-appearance: textfield;
        appearance: textfield;

        cursor: text;
    }

    input[type='number']::-webkit-inner-spin-button,
    input[type='number']::-webkit-outer-spin-button {
        -webkit-appearance: none;
    }

    input[type='date'] {
        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;
    }

    input[type='date']::-webkit-inner-spin-button {
        display: none;
    }

    input[type='date']::-webkit-calendar-picker-indicator {
        background-image: url('../../assets/icons/calendar.png');
        cursor: pointer;
    }

    input[type='date']::-webkit-date-and-time-value {
        text-align: left;
    }

    .image-preview {
        align-self: center;
        width: 60%;
        aspect-ratio: 1/1;
        border: 1px solid #ced4da;
        border-radius: 5px;
        outline: solid 2px #f8f8f8;
        margin-bottom: 10px;

        display: flex;
        justify-content: center;
        align-items: center;
    }

    .image-preview > img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .image-preview > svg {
        width: 50px;
        height: 50px;
        cursor: pointer;
        color: #ced4da;
    }

    .input-container select {
        width: 100%;
        height: 40px;
        padding: 10px;
        margin-bottom: 30px;
        border: 1px solid #ced4da;
        border-radius: 5px;
        outline: solid 2px #f8f8f8;
        font-size: 18px;
        color: #000;
        background-color: #fff;
        cursor: pointer;
    }

    .input-container button {
        appearance: none;
        padding: 10px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        width: 100%;
        height: 40px;
        cursor: pointer;
    }
</style>
