<script>
    import Modal from '../Modal.svelte';
    import Button from '../Button.svelte';
    import Loader from '../Loader.svelte';
    import { formatDate } from '../pages/FoodIntake.svelte';
    import { createEventDispatcher } from 'svelte';
    import {
        activities,
        categories,
    } from '../../../../server/temp/activities.js';
    import CaloriesCalculator from './CaloriesCalculator.svelte';
    import {
        addExercise,
        updateExercise,
        deleteExercise,
        getUserWeight,
        uploadUserWeight,
    } from '../../api';

    let isPopupOpen = false;

    export let isModalOpen = false;
    export let isAdding = true;
    export let exercise = {};

    let today = formatDate(new Date());

    const dispatch = createEventDispatcher();

    function getInitialInputs() {
        return {
            uid: '',
            category: '',
            exercise_id: '',
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

    async function uploadExercise() {
        if (isLoading) return;
        isLoading = true;

        if (
            exercise.category.trim() === '' ||
            exercise.exercise_id.trim() === '' ||
            exercise.date.trim() === '' ||
            Number(exercise.duration) === 0
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
                const result = await addExercise(
                    exercise.exercise_id,
                    exercise.category,
                    exercise.date,
                    Number(exercise.duration),
                    Number(exercise.burned_calories) || 0,
                );

                exercise.uid = result.uid;
            } catch (error) {
                errorMessage =
                    'Failed to add the exercise. Please try again later.';
                isLoading = false;
                return;
            }
        } else {
            try {
                await updateExercise(
                    exercise.uid,
                    exercise.exercise_id,
                    exercise.category,
                    exercise.date,
                    Number(exercise.duration),
                    Number(exercise.burned_calories) || 0,
                );
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

    async function removeExercise() {
        if (isLoading) return;
        isLoading = true;

        try {
            await deleteExercise(exercise.uid);
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

    let activity = {
        exercise_id: '',
        duration: '',
    };

    let caculateErrorMessage = '';
    let userWeight = 0;
    let oldWeight = 0;

    async function calculateCalories() {
        if (
            exercise.category.trim() === '' ||
            exercise.exercise_id.trim() === '' ||
            Number(exercise.duration) === 0
        ) {
            caculateErrorMessage =
                'Category, activity and duration of the workout are required';
            return;
        }

        userWeight = await getUserWeight();
        oldWeight = userWeight;

        activity = {
            exercise_id: exercise.exercise_id,
            duration: exercise.duration,
        };
        isPopupOpen = true;
    }

    async function displayCalories(event) {
        if (oldWeight !== userWeight) {
            await uploadUserWeight(Number(userWeight));
            oldWeight = userWeight;
        }

        exercise.burned_calories = event.detail;
    }
</script>

<Modal
    bind:isOpen={isModalOpen}
    on:close={() => {
        errorMessage = '';
        deleteErrorMessage = '';
        caculateErrorMessage = '';
        exercise = getInitialInputs();
    }}
>
    <div class="modal-wrapper">
        <div class="input-container">
            <label for="category">Category<span class="required">*</span></label
            >
            <select
                id="category"
                name="category"
                bind:value={exercise.category}
            >
                <option hidden disabled selected value>
                    -- select an option --
                </option>
                {#each Object.keys(categories) as category}
                    <option value={category}>{category}</option>
                {/each}
            </select>
            <label for="description"
                >Activity<span class="required">*</span></label
            >
            <select
                id="description"
                name="description"
                bind:value={exercise.exercise_id}
            >
                {#if exercise.category}
                    {#if !exercise.exercise_id}
                        <option hidden disabled selected value>
                            -- select an option --
                        </option>
                    {/if}
                    {#each categories[exercise.category] as id}
                        <option value={id}
                            >{activities[id]['description']}</option
                        >
                    {/each}
                {:else}
                    <option value="">Please select a category first</option>
                {/if}
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
                >Workout duration (minutes)<span class="required">*</span
                ></label
            >
            <input
                type="number"
                pattern="[0-9]*"
                id="duration"
                name="duration"
                onkeypress="return event.charCode >= 48 && event.charCode <= 57"
                oninput="this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');"
                bind:value={exercise.duration}
            />
            <div class="calories-wrapper">
                <p class="calories-span">Calories burned</p>
                <div class="calories-container">
                    <input
                        type="number"
                        pattern="[0-9]*"
                        onkeypress="return event.charCode >= 48 && event.charCode <= 57"
                        oninput="this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');"
                        bind:value={exercise.burned_calories}
                    />
                    <Button
                        primaryBordered={true}
                        isExpanded={false}
                        backgroundColor="white"
                        on:click={calculateCalories}
                    >
                        <span>Calculate</span>
                    </Button>
                </div>
                <p class="error-message">{caculateErrorMessage}</p>
            </div>

            {#if isAdding}
                <Button
                    bind:isLoading
                    isExpanded={true}
                    on:click={uploadExercise}
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
                    on:click={uploadExercise}
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
                    on:click={removeExercise}
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

<CaloriesCalculator
    bind:isPopupOpen
    bind:activity
    bind:userWeight
    on:calculated={displayCalories}
></CaloriesCalculator>

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

    .calories-wrapper {
        margin-bottom: 20px;
    }

    .calories-container {
        display: flex;
        justify-content: space-between;
    }

    .calories-span {
        font-size: 20px;
        margin: 10px 0 5px 0;
        width: 100%;
        text-align: left;
        pointer-events: none;
    }

    .calories-container input {
        width: 65%;
        margin: 0;
    }
</style>
