<script>
    import Modal from '../Modal.svelte';
    import Button from '../Button.svelte';
    import Loader from '../Loader.svelte';
    import { formatDate } from '../pages/FoodIntake.svelte';
    import { createEventDispatcher } from 'svelte';

    export let isModalOpen = false;
    export let isAdding = true;
    export let exercise = {};

    let today = formatDate(new Date());

    const dispatch = createEventDispatcher();

    function getInitialInputs() {
        return {
            uid: '',
            name: '',
            type: '',
            burned_calories: '',
            date: today,
            duration: '',
        };
    }

    exercise = getInitialInputs();

    function handleMaxDate(event) {
        new Date(event.target.value) > new Date()
            ? (event.target.value = today)
            : event.target.value;
        exercise.date = event.target.value;
    }

    let errorMessage = '';
    let isLoading = false;

    async function uploadFoodIntake() {
        if (isLoading) return;
        isLoading = true;

        if (
            exercise.name.trim() === '' ||
            exercise.type.trim() === '' ||
            exercise.duration.trim() === ''
        ) {
            errorMessage = 'Please fill all required fields';
            isLoading = false;
            return;
        }

        if (exercise.date > today) {
            errorMessage = 'Date cannot be in the future';
            isLoading = false;
            return;
        }

        if (isAdding) {
            try {
                //add exercise
            } catch (error) {
                errorMessage =
                    'Failed to add the exercise. Please try again later.';
                isLoading = false;
                return;
            }
        } else {
            try {
                // edit exercise
            } catch (error) {
                errorMessage =
                    'Failed to edit the exercise. Please try again later.';
                isLoading = false;
                return;
            }
        }

        isLoading = false;

        if (isAdding) {
            dispatch('add', exercise);
        } else {
            dispatch('edit', exercise);
        }

        isModalOpen = false;
    }

    let deleteErrorMessage = '';

    async function removeFoodIntake() {
        if (isLoading) return;
        isLoading = true;

        try {
            // delete exercise
        } catch (error) {
            deleteErrorMessage =
                'Failed to delete the exercise. Please try again later.';
            isLoading = false;
            return;
        }

        isLoading = false;
        dispatch('delete', exercise);
        isModalOpen = false;
    }
</script>

<Modal
    bind:isOpen={isModalOpen}
    on:close={() => {
        errorMessage = '';
        deleteErrorMessage = '';
        exercise = getInitialInputs();
    }}
>
    <div class="modal-wrapper">
        <div class="input-container">
            <label for="name">Name<span class="required">*</span></label>
            <input
                type="text"
                id="name"
                name="name"
                bind:value={exercise.name}
            />
            <label for="type">Workout type<span class="required">*</span></label
            >
            <select id="type" name="type" bind:value={exercise.type}>
                <option hidden disabled selected value>
                    -- select an option --
                </option>
                <option value="CARDIO">Cardio</option>
                <option value="STRENGTH">Strength</option>
                <option value="FLEXIBILITY">Flexibility</option>
            </select>
            <label for="date">Workout date<span class="required">*</span></label
            >
            <input
                type="date"
                id="date"
                name="date"
                max={today}
                on:change={handleMaxDate}
                bind:value={exercise.date}
            />
            <label for="duration"
                >Workout duration<span class="required">*</span></label
            >
            <input
                style="margin-bottom: 20px;"
                type="number"
                pattern="[0-9]*"
                id="duration"
                name="duration"
                onkeypress="return event.charCode >= 48 && event.charCode <= 57"
                oninput="this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');"
                bind:value={exercise.duration}
            />
            <div class="calories-container">
                <label for="calories">Calories burned</label>
                <Button
                    primaryBordered={true}
                    isExpanded={false}
                    backgroundColor="white"
                >
                    <span>Calculate</span>
                </Button>
            </div>

            {#if isAdding}
                <Button
                    bind:isLoading
                    isExpanded={true}
                    on:click={uploadFoodIntake}
                >
                    {#if isLoading}
                        <Loader></Loader>
                    {:else}
                        <span>Add</span>
                    {/if}
                </Button>
                <p class="error-message">{errorMessage}</p>
            {:else}
                <Button
                    bind:isLoading
                    isExpanded={true}
                    on:click={uploadFoodIntake}
                >
                    {#if isLoading}
                        <Loader></Loader>
                    {:else}
                        <span>Edit</span>
                    {/if}
                </Button>
                <p class="error-message">{errorMessage}</p>
                <Button
                    bind:isLoading
                    isExpanded={true}
                    backgroundColor="#f50707"
                    on:click={removeFoodIntake}
                >
                    {#if isLoading}
                        <Loader></Loader>
                    {:else}
                        <span>Delete</span>
                    {/if}
                </Button>
                <p class="error-message">{deleteErrorMessage}</p>
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

    @media (max-width: 400px) {
        .modal-wrapper {
            height: auto;
        }
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

    .input-container > select {
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
        cursor: pointer;
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

    .calories-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
</style>
