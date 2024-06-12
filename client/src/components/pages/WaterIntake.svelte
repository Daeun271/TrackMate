<script>
    import WaterCup from '../water_intakes/WaterCup.svelte';

    let volume = 0;

    $: water_level = Math.min(volume / 2, 1);

    let incrementVolume = () => {
        volume += 0.25;
    };

    let decrementVolume = () => {
        volume = Math.max(volume - 0.25, 0);
    };
</script>

<div class="waterintake-wrapper">
    <p>Today's Water Intake</p>
    <p>{volume} L</p>
    <div>
        <WaterCup level={water_level} />
    </div>
    <p>Record</p>
    <div class="volume-buttons">
        <button on:click={decrementVolume}>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="white"
            >
                <path
                    fill-rule="evenodd"
                    d="M4 10a.75.75 0 0 1 .75-.75h10.5a.75.75 0 0 1 0 1.5H4.75A.75.75 0 0 1 4 10Z"
                    clip-rule="evenodd"
                />
            </svg>
        </button>
        <p>0.25 L</p>
        <button on:click={incrementVolume}>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="white"
            >
                <path
                    d="M10.75 4.75a.75.75 0 0 0-1.5 0v4.5h-4.5a.75.75 0 0 0 0 1.5h4.5v4.5a.75.75 0 0 0 1.5 0v-4.5h4.5a.75.75 0 0 0 0-1.5h-4.5v-4.5Z"
                />
            </svg>
        </button>
    </div>
</div>

<style>
    .waterintake-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        row-gap: 10px;
        height: 100%;
    }

    .waterintake-wrapper p {
        margin: 0;
    }

    .volume-buttons {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: row;
    }

    .volume-buttons p {
        margin: 0 20px;
    }

    .volume-buttons svg {
        width: 30px;
        height: 30px;
    }

    .volume-buttons > button {
        background-color: #007bff;
        color: white;

        display: flex;
        justify-content: center;
        align-items: center;

        width: 45px;
        height: 45px;
        padding: 0;

        border: none;
        border-radius: 50%;

        cursor: pointer;

        box-shadow: none;

        transition:
            all 0.2s ease-in-out,
            background-color 0.3s,
            transform 0.3s;
    }

    .volume-buttons > button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transform: 0.1s;
    }

    .volume-buttons > button:active {
        background-color: #0042a2;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transform: scale(1.1), 0.1s;
    }
</style>
