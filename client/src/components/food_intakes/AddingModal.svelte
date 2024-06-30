<script>
    import { addFoodIntake, uploadFoodImage } from '../../api';
    import Modal from '../Modal.svelte';
    import Loader from '../Loader.svelte';
    import Button from '../Button.svelte';

    export let isAddingModalOpen = false;
    const today = new Date().toISOString().split('T')[0];

    function getInitialInputs() {
        return {
            imageUrl: '',
            imageBlob: null,
            name: '',
            calories: '',
            date: today,
            timeCategory: '',
        };
    }

    let userInputs = getInitialInputs();

    let imageInput;

    async function onImageFileChanged(event) {
        const file = event.target.files[0];

        if (!file) {
            return;
        }

        const image = new Image();
        image.src = URL.createObjectURL(file);
        await new Promise((resolve) => {
            image.onload = () => resolve(image);
        });

        let width = image.width;
        let height = image.height;

        const MAX_SIZE = 600;

        if (width > height) {
            if (width > MAX_SIZE) {
                height *= MAX_SIZE / width;
                width = MAX_SIZE;
            }
        } else {
            if (height > MAX_SIZE) {
                width *= MAX_SIZE / height;
                height = MAX_SIZE;
            }
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(image, 0, 0, width, height);

        const jpegBlob = await new Promise((resolve) => {
            canvas.toBlob(
                (blob) => {
                    resolve(blob);
                },
                'image/jpeg',
                0.8,
            );
        });

        userInputs.imageBlob = jpegBlob;
        const jpegUrl = URL.createObjectURL(jpegBlob);
        userInputs.imageUrl = jpegUrl;
    }

    function handleMaxDate(event) {
        new Date(event.target.value) > new Date()
            ? (event.target.value = today)
            : event.target.value;
        userInputs.date = event.target.value;
    }

    let errorMessage = '';
    let isLoading = false;

    async function uploadFoodIntake() {
        if (isLoading) return;
        isLoading = true;

        if (!userInputs.name) {
            errorMessage = 'Please fill all required fields';
            isLoading = false;
            return;
        }

        let uid;
        try {
            const result = await addFoodIntake(
                userInputs.name,
                Number(userInputs.calories),
                userInputs.date,
                userInputs.timeCategory || null,
            );

            uid = result.uid;
        } catch (error) {
            errorMessage = 'Failed to add food intake';
            isLoading = false;
            return;
        }

        if (userInputs.imageBlob) {
            const imageFile = new File([userInputs.imageBlob], 'file', {
                type: 'image/jpeg',
            });

            try {
                await uploadFoodImage(uid, imageFile);
            } catch (error) {
                errorMessage = 'Failed to upload image';
                isLoading = false;
                return;
            }
        }

        isLoading = false;

        errorMessage = '';
        userInputs = getInitialInputs();
        isAddingModalOpen = false;
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
                on:change={onImageFileChanged}
                type="file"
                id="image"
                name="image"
                accept="image/*"
                style="display:none;"
            />
            <div class="image-preview" on:click={() => imageInput.click()}>
                {#if userInputs.imageUrl}
                    <img
                        src={userInputs.imageUrl}
                        alt="selectedImage"
                        style="cursor: pointer;"
                    />
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
            <label for="name">Name<span class="required">*</span></label>
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
            <label for="date">Date<span class="required">*</span></label>
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
            <Button isExpanded={true} on:click={uploadFoodIntake}>
                {#if isLoading}
                    <Loader></Loader>
                {:else}
                    <span>Add</span>
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
        object-fit: contain;
    }

    .image-preview > svg {
        width: 50px;
        height: 50px;
        cursor: pointer;
        color: #ced4da;
    }

    .input-container > select {
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

    .required {
        color: #f50707;
        margin-left: 5px;
    }

    .error-message {
        color: #f50707;
        font-size: 15px;
        margin: 5px 0 0 0;
    }
</style>
