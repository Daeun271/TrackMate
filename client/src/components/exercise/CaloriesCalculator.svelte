<script>
    import Modal from '../../components/Modal.svelte';
    import Button from '../../components/Button.svelte';
    import { activities } from '../../../../server/temp/activities';
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    export let isPopupOpen = false;
    export let activity = {
        exercise_id: '',
        duration: '',
    };
    export let userWeight = 0;

    $: met = activity.exercise_id ? activities[activity.exercise_id].met : 0;
    $: calories = Math.round(
        (Number(userWeight) * met * 3.5 * Number(activity.duration)) / 200,
    );

    let errorMessage = '';

    async function saveCalories() {
        if (Number(userWeight) === 0) {
            errorMessage = 'Please enter your weight';
            return;
        }

        dispatch('calculated', calories);
        isPopupOpen = false;
    }
</script>

<Modal
    bind:isOpen={isPopupOpen}
    isPopup={true}
    on:close={() => {
        errorMessage = '';
    }}
>
    <div class="modal-wrapper">
        <div class="input-container">
            <label for="weight"
                >Weight (kg)<span class="required">*</span></label
            >
            <input
                type="number"
                pattern="[0-9]*"
                id="weight"
                name="weight"
                onkeypress="return event.charCode >= 48 && event.charCode <= 57"
                oninput="this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');"
                bind:value={userWeight}
            />
            <label for="calories">Calories burned</label>
            <input
                type="number"
                id="calories"
                name="calories"
                readonly
                style="margin-bottom: 30px;"
                bind:value={calories}
            />
            <Button on:click={saveCalories}>Save</Button>
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

    @media (max-width: 400px) {
        .modal-wrapper {
            height: auto;
        }
    }

    .input-container {
        display: flex;
        flex-direction: column;
        width: 90%;
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

    .required {
        color: #f50707;
        margin-left: 5px;
    }

    .error-message {
        color: #f50707;
        font-size: 15px;
        margin: 5px 0 5px 0;
    }
</style>
