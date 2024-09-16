<script>
    import EmptyPage from '../EmptyPage.svelte';
    import imageUrl from '../../assets/icons/exercise-routine.png?url';
    import Modal from '../exercise/Modal.svelte';
    import CircleButton from '../CircleButton.svelte';
    import { formatDate } from './FoodIntake.svelte';
    import {
        activities,
        categories,
        categoryToColor,
    } from '../../../../server/temp/activities.js';

    let today = formatDate(new Date());

    function handleMaxDate(event) {
        new Date(event.target.value) > new Date()
            ? (event.target.value = today)
            : event.target.value;
        //exercise.date = event.target.value;
    }

    let exercises = [
        {
            uid: '1',
            category: 'Bicycling',
            activity_id: '01003',
            burned_calories: 10.0,
            date: '2021-09-01',
            duration: 30,
        },
        {
            uid: '2',
            category: 'Bicycling',
            activity_id: '01004',
            burned_calories: '150.0',
            date: '2021-09-01',
            duration: '45',
        },
        {
            uid: '3',
            category: 'Bicycling',
            activity_id: '01008',
            burned_calories: '100',
            date: '2021-09-01',
            duration: '60',
        },
    ];

    let activity = {
        uid: '',
        category: '',
        activity_id: '',
        burned_calories: '',
        date: today,
        duration: '',
    };

    let isModalOpen = false;
    let isAdding = true;

    function addExercise(event) {
        // add exercise to database
        console.log('add exercise');
    }

    function updateExercise(event) {
        // update exercise in database
        console.log('update exercise');
    }

    function deleteExercise(event) {
        // delete exercise from database
        console.log('delete exercise');
    }

    function displayExercise(exercise) {
        activity = exercise;
        isAdding = false;
        isModalOpen = true;
    }
</script>

{#if exercises.length === 0}
    <EmptyPage
        text1="No exercises found"
        text2="Get started by tracking your exercise"
        {imageUrl}
        on:modalClick={() => {
            isAdding = true;
            isModalOpen = true;
        }}
    ></EmptyPage>
{:else}
    <div class="bg">
        <div class="date-header">
            <CircleButton widthAndHeight="25px">&lt</CircleButton>
            <input
                type="date"
                value={today}
                max={today}
                on:change={handleMaxDate}
            />
            <CircleButton widthAndHeight="25px">&gt</CircleButton>
        </div>
        <div class="exercise-list">
            <div class="exercise-card-wrapper">
                <div class="empty-exercise-card">
                    <p>Click the button below to add a new exercise</p>
                    <svg
                        on:click={() => {
                            isAdding = true;
                            isModalOpen = true;
                        }}
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
                {#each exercises as exercise}
                    {@const activity = activities[exercise.activity_id]}
                    {@const backgroundColor =
                        categoryToColor[exercise.category] ?? '#e6f9f6'}
                    <div
                        class="exercise-card"
                        style={`background-color: ${backgroundColor}`}
                    >
                        <div class="exercise-card-content">
                            <h3>
                                {activity?.description ?? 'Unknown activity'}
                            </h3>
                            <p>{exercise.date}</p>
                            <p>{exercise.duration} minutes</p>
                            {#if exercise.burned_calories}
                                <p>
                                    {Math.round(
                                        Number(exercise.burned_calories),
                                    )} calories burned
                                </p>
                            {/if}
                        </div>
                        <div class="exercise-card-actions">
                            <button
                                class="icon-button"
                                on:click={() => displayExercise(exercise)}
                                >⚙️</button
                            >
                            <button
                                class="icon-button"
                                on:click={deleteExercise}>🚮</button
                            >
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
{/if}

<Modal
    bind:isAdding
    bind:isModalOpen
    bind:exercise={activity}
    on:add={addExercise}
    on:edit={updateExercise}
    on:delete={deleteExercise}
></Modal>

<style>
    .bg {
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    .date-header {
        flex: 0 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        height: 40px;

        border-bottom: 2px solid #f0f0f0;
        background-color: transparent;
        color: 'black';
    }

    input[type='date'] {
        border: none;
        outline: none;

        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;

        font-size: 20px;
        text-align: center;

        color: black;
        background-color: transparent;
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

    .exercise-list {
        flex: 1 1 auto;
        overflow-y: auto;
    }

    .exercise-card-wrapper {
        display: grid;
        justify-content: space-around;
        grid-template-columns: repeat(auto-fill, 350px);
        gap: 30px;
        padding: 30px 10px 30px 10px;
    }

    .exercise-card {
        border-radius: 5px;
        padding: 20px;
        position: relative;
    }

    .exercise-card-content {
        display: flex;
        flex-direction: column;
        row-gap: 15px;
    }

    .exercise-card-content h3 {
        margin: 0;
    }

    .exercise-card-content p {
        margin: 0;
    }

    .exercise-card-actions {
        position: absolute;
        bottom: 10px;
        right: 15px;
    }

    .icon-button {
        appearance: none;
        font-size: 20px;
        background-color: transparent;
        border: none;
        cursor: pointer;
        border-radius: 8px;
        padding: 0 5px 0 0;
    }

    .empty-exercise-card {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 1px solid #ced4da;
        border-radius: 5px;
        padding: 20px;
        cursor: pointer;
    }

    .empty-exercise-card p {
        margin: 0 0 10px 0;
        font-size: 15px;
        text-align: center;
        cursor: default;
        user-select: none;
        -webkit-user-select: none;
    }

    .empty-exercise-card svg {
        width: 50px;
        height: 50px;
        cursor: pointer;
    }
</style>
