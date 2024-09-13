<script>
    import EmptyPage from '../EmptyPage.svelte';
    import imageUrl from '../../assets/icons/exercise-routine.png?url';
    import Modal from '../exercise/Modal.svelte';
    import CircleButton from '../CircleButton.svelte';
    import { formatDate } from './FoodIntake.svelte';

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
            name: 'Running',
            type: 'CARDIO',
            burned_calories: '500',
            date: '2021-09-01',
            duration: '1 hour',
        },
        {
            uid: '2',
            name: 'Weightlifting',
            type: 'STRENGTH',
            burned_calories: '300',
            date: '2021-09-01',
            duration: '1 hour',
        },
        {
            uid: '3',
            name: 'Yoga',
            type: 'FLEXIBILITY',
            burned_calories: '200',
            date: '2021-09-01',
            duration: '1 hour',
        },
        {
            uid: '4',
            name: 'Running',
            type: 'CARDIO',
            burned_calories: '500',
            date: '2021-09-01',
            duration: '1 hour',
        },
        {
            uid: '5',
            name: 'Weightlifting',
            type: 'STRENGTH',
            burned_calories: '300',
            date: '2021-09-01',
            duration: '1 hour',
        },
        {
            uid: '6',
            name: 'Yoga',
            type: 'FLEXIBILITY',
            burned_calories: '200',
            date: '2021-09-01',
            duration: '1 hour',
        },
    ];

    let exercise = {
        uid: '',
        name: '',
        type: '',
        burned_calories: '',
        date: '',
        duration: '',
    };

    let isModalOpen = false;
    let isAdding = true;

    function addExercise(event) {
        console.log('add exercise');
    }

    function updateExercise(event) {
        console.log('update exercise');
    }

    function deleteExercise(event) {
        console.log('delete exercise');
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
                    <div class="exercise-card" data-type={exercise.type}>
                        <div class="exercise-card-content">
                            <h3>{exercise.name}</h3>
                            <p>{exercise.burned_calories} calories burned</p>
                            <p>{exercise.date}</p>
                            <p>{exercise.duration}</p>
                        </div>
                        <div class="exercise-card-actions">
                            <button
                                class="icon-button"
                                on:click={() => {
                                    isAdding = false;
                                    isModalOpen = true;
                                    exercise = { ...exercise };
                                }}>⚙️</button
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
    bind:exercise
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

    .exercise-card[data-type='CARDIO'] {
        border-color: #d1f7ff;
        background-color: #e6f9ff;
    }

    .exercise-card[data-type='STRENGTH'] {
        border-color: #f7d1f7;
        background-color: #ffe6ff;
    }

    .exercise-card[data-type='FLEXIBILITY'] {
        border-color: #f7f7d1;
        background-color: #ffffe6;
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
        top: 10px;
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
