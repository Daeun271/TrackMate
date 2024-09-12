<script>
    import EmptyPage from '../EmptyPage.svelte';
    import imageUrl from '../../assets/icons/exercise-routine.png?url';
    import Modal from '../exercise/Modal.svelte';

    let exercises = [
        {
            uid: '1',
            name: 'Running',
            type: 'Cardio',
            burned_calories: '500',
            date: '2021-09-01',
            time: '08:00',
            duration: '1 hour',
            img_src: '',
            img_blob: null,
        },
        {
            uid: '2',
            name: 'Weightlifting',
            type: 'Strength',
            burned_calories: '300',
            date: '2021-09-01',
            time: '10:00',
            duration: '1 hour',
            img_src: '',
            img_blob: null,
        },
        {
            uid: '3',
            name: 'Yoga',
            type: 'Flexibility',
            burned_calories: '200',
            date: '2021-09-01',
            time: '12:00',
            duration: '1 hour',
            img_src: '',
            img_blob: null,
        },
        {
            uid: '4',
            name: 'Running',
            type: 'Cardio',
            burned_calories: '500',
            date: '2021-09-01',
            time: '08:00',
            duration: '1 hour',
            img_src: '',
            img_blob: null,
        },
        {
            uid: '5',
            name: 'Weightlifting',
            type: 'Strength',
            burned_calories: '300',
            date: '2021-09-01',
            time: '10:00',
            duration: '1 hour',
            img_src: '',
            img_blob: null,
        },
        {
            uid: '6',
            name: 'Yoga',
            type: 'Flexibility',
            burned_calories: '200',
            date: '2021-09-01',
            time: '12:00',
            duration: '1 hour',
            img_src: '',
            img_blob: null,
        },
    ];

    let exercise = {
        uid: '',
        name: '',
        type: '',
        burned_calories: '',
        date: '',
        time: '',
        duration: '',
        img_src: '',
        img_blob: null,
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
        text2="Get started by adding a new exercise"
        {imageUrl}
        on:modalClick={() => {
            isAdding = true;
            isModalOpen = true;
        }}
    ></EmptyPage>
{:else}
    <div class="bg">
        <div class="date-header">
            <button>Previous</button>
            <h2>September 1, 2021</h2>
            <button>Next</button>
        </div>
        <div class="exercise-list">
            <div class="exercise-card-wrapper">
                {#each exercises as exercise}
                    <div class="exercise-card">
                        <div class="exercise-card-img"></div>
                        <div class="exercise-card-content">
                            <h3>{exercise.name}</h3>
                            <p>{exercise.type}</p>
                            <p>{exercise.burned_calories} calories burned</p>
                            <p>{exercise.date} {exercise.time}</p>
                            <p>{exercise.duration}</p>
                        </div>
                        <div class="exercise-card-actions">
                            <button
                                on:click={() => {
                                    isAdding = false;
                                    isModalOpen = true;
                                    exercise = { ...exercise };
                                }}>Edit</button
                            >
                            <button
                                on:click={() => {
                                    isAdding = false;
                                    isModalOpen = true;
                                    exercise = { ...exercise };
                                }}>Delete</button
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

    .exercise-list {
        flex: 1 1 auto;
        overflow-y: auto;

        display: flex;
        flex-direction: column;
    }

    .exercise-card-wrapper {
        display: flex;
        flex-direction: column;
        row-gap: 30px;
        padding: 30px;
    }

    .exercise-card {
        display: flex;
        flex-direction: row;
        column-gap: 10px;
        padding: 10px;
        border: 2px solid #007bff;
        border-radius: 5px;
        background-color: white;
    }
</style>
