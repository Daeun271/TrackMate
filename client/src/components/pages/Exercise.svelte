<script>
    import Modal from '../exercise/Modal.svelte';
    import { formatDate } from './FoodIntake.svelte';
    import {
        activities,
        categoryToColor,
    } from '../../../../server/temp/activities.js';
    import { getExercisesTotal, deleteExercise } from '../../api.js';
    import DatePicker from '../DatePicker.svelte';

    let today = formatDate(new Date());
    let date = today;

    async function showYesterday(event) {
        let exercises = await exercisePromise;

        const newDate = event.detail;

        if (!(newDate in exercises)) {
            appendExercises(exercises, newDate);
        }

        date = newDate;
    }

    async function showData() {
        let exercises = await exercisePromise;

        if (!(date in exercises)) {
            appendExercises(exercises, date);
        }
    }

    let exercisePromise = getExercises();

    async function getExercises() {
        const today = formatDate(new Date());
        const tomorrow = formatDate(
            new Date(new Date().setDate(new Date().getDate() + 1)),
        );
        const exerciseRes = await getExercisesTotal(today, tomorrow);

        const exercises = {};
        exercises[today] = [];

        if (exerciseRes.exercises.length !== 0) {
            for (let i = 0; i < exerciseRes.exercises.length; i++) {
                const exercise = exerciseRes.exercises[i];
                exercises[today].unshift(exercise);
            }
        }

        return exercises;
    }

    async function appendExercises(exercises, date) {
        const tomorrow = formatDate(
            new Date(new Date(date).setDate(new Date(date).getDate() + 1)),
        );
        const exerciseRes = await getExercisesTotal(date, tomorrow);

        exercises[date] = [];

        if (exerciseRes.exercises.length !== 0) {
            for (let i = 0; i < exerciseRes.exercises.length; i++) {
                const exercise = exerciseRes.exercises[i];
                exercises[date].unshift(exercise);
            }
        }

        exercisePromise = Promise.resolve(exercises);
    }

    let isModalOpen = false;
    let isAdding = true;

    async function addExercise(event) {
        let exercises = await exercisePromise;

        const exercise = {
            uid: event.detail.uid,
            category: event.detail.category,
            exercise_id: event.detail.exercise_id,
            date: event.detail.date,
            duration: event.detail.duration,
            burned_calories: event.detail.burned_calories || null,
        };

        if (exercises) {
            if (exercise.date in exercises) {
                exercises[exercise.date].unshift(exercise);
            } else {
                exercises[exercise.date] = [exercise];
            }
        } else {
            exercises = { [exercise.date]: [exercise] };
        }

        exercisePromise = Promise.resolve(exercises);
    }

    async function updateExercise(event) {
        let exercises = await exercisePromise;

        const newExercise = {
            uid: event.detail.uid,
            category: event.detail.category,
            exercise_id: event.detail.exercise_id,
            date: event.detail.date,
            duration: event.detail.duration,
            burned_calories: event.detail.burned_calories || null,
        };

        for (const date in exercises) {
            let oldExercise = exercises[date].find(
                (exercise) => exercise.uid === newExercise.uid,
            );

            if (oldExercise) {
                const index = exercises[date].indexOf(oldExercise);
                exercises[date].splice(index, 1);
                if (exercises[date].length === 0) {
                    delete exercises[date];
                }

                if (newExercise.date in exercises) {
                    exercises[newExercise.date].unshift(newExercise);
                } else {
                    exercises[newExercise.date] = [newExercise];
                }

                break;
            }
        }

        exercisePromise = Promise.resolve(exercises);
    }

    async function removeExerciseImmediately(exercise) {
        await deleteExercise(exercise.uid);

        let exercises = await exercisePromise;

        let oldExercise = exercises[exercise.date].find(
            (ex) => ex.uid === exercise.uid,
        );

        if (oldExercise) {
            const index = exercises[exercise.date].indexOf(oldExercise);
            exercises[exercise.date].splice(index, 1);
            if (exercises[exercise.date].length === 0) {
                delete exercises[exercise.date];
            }
        }

        exercisePromise = Promise.resolve(exercises);
    }

    async function removeExercise(event) {
        let exercises = await exercisePromise;

        for (const date in exercises) {
            let exercise = exercises[date].find(
                (exercise) => exercise.uid === event.detail.uid,
            );

            if (exercise) {
                const index = exercises[date].indexOf(exercise);
                exercises[date].splice(index, 1);
                if (exercises[date].length === 0) {
                    delete exercises[date];
                }

                break;
            }
        }

        exercisePromise = Promise.resolve(exercises);
    }

    let activity = null;

    function displayExercise(exercise) {
        activity = structuredClone(exercise);
        isAdding = false;
        isModalOpen = true;
    }
</script>

{#await exercisePromise}
    <p>loading...</p>
{:then exercises}
    <div class="bg">
        <DatePicker
            on:showYesterday={showYesterday}
            on:showData={showData}
            bind:date
        ></DatePicker>
        <div class="exercise-list">
            <div class="exercise-card-wrapper">
                <div class="empty-exercise-card">
                    <p>Click the button below to add a new exercise</p>
                    <svg
                        on:click={() => {
                            activity = {
                                date: date,
                            };
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
                {#if date in exercises}
                    {#each exercises[date] as exercise}
                        {@const activity = activities[exercise.exercise_id]}
                        {@const backgroundColor =
                            categoryToColor[exercise.category] ?? '#e6f9f6'}
                        <div
                            class="exercise-card"
                            style={`background-color: ${backgroundColor}`}
                        >
                            <div class="exercise-card-content">
                                <h3>
                                    {activity?.description ??
                                        'Unknown activity'}
                                </h3>
                                <p>
                                    {Math.round(Number(exercise.duration))} minutes
                                </p>
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
                                    on:click={() =>
                                        removeExerciseImmediately(exercise)}
                                    >🚮</button
                                >
                            </div>
                        </div>
                    {/each}
                {/if}
            </div>
        </div>
    </div>
{/await}

<Modal
    bind:isAdding
    bind:isModalOpen
    bind:exercise={activity}
    on:add={addExercise}
    on:edit={updateExercise}
    on:delete={removeExercise}
></Modal>

<style>
    .bg {
        display: flex;
        flex-direction: column;
        height: 100%;
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
