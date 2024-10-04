<script>
    import CircleButton from './CircleButton.svelte';
    import { createEventDispatcher } from 'svelte';
    import { formatDate } from './pages/FoodIntake.svelte';

    const dispatch = createEventDispatcher();

    let today = formatDate(new Date());
    export let date = today;

    function handleMaxDate(event) {
        new Date(event.target.value) > new Date()
            ? (event.target.value = today)
            : event.target.value;
        date = event.target.value;

        dispatch('showData');
    }

    function showYesterday() {
        const newDate = formatDate(
            new Date(new Date(date).setDate(new Date(date).getDate() - 1)),
        );

        dispatch('showYesterday', newDate);
    }

    function showTomorrow() {
        const newDate = formatDate(
            new Date(new Date(date).setDate(new Date(date).getDate() + 1)),
        );

        if (newDate <= today) {
            date = newDate;
        }
    }
</script>

<div class="date-header">
    <CircleButton on:click={showYesterday} widthAndHeight="25px"
        >&lt</CircleButton
    >
    <input
        type="date"
        bind:value={date}
        max={today}
        on:change={handleMaxDate}
    />
    <CircleButton on:click={showTomorrow} widthAndHeight="25px"
        >&gt</CircleButton
    >
</div>

<style>
    * {
        -webkit-user-select: none;
        user-select: none;
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
        background-image: url('../assets/icons/calendar.png');
        cursor: pointer;
    }

    input[type='date']::-webkit-date-and-time-value {
        text-align: left;
    }
</style>
