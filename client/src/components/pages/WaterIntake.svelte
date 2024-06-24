<script>
    import WaterCup from '../water_intakes/WaterCup.svelte';
    import CircleButton from '../water_intakes/CircleButton.svelte';
    import Modal from '../Modal.svelte';
    import Button from '../water_intakes/Button.svelte';
    import { getWaterIntakesTotal, addWaterIntake } from '../../api.js';

    let newVolume = 0;

    let modalOpen = false;

    let waterIntakePromise = getWaterIntake();
    async function getWaterIntake() {
        const waterIntakeTotalRes = await getWaterIntakesTotal(
            new Date().toISOString(),
        );

        return waterIntakeTotalRes;
    }

    async function updateWaterIntake() {
        await addWaterIntake(newVolume, new Date().toISOString());
        modalOpen = false;
        waterIntakePromise = getWaterIntake();
    }

    function openModal() {
        newVolume = 0;
        modalOpen = true;
    }

    $: waterLevel = Math.min(newVolume / 2, 1);
    $: levelPercent = -90 * waterLevel + 90;
</script>

<div class="waterintake-wrapper">
    {#await waterIntakePromise}
        <p>loading...</p>
    {:then waterIntakeTotalRes}
        {#if waterIntakeTotalRes.total_volume >= 0 && waterIntakeTotalRes.total_volume < 0.5}
            <p>Let's drink 2L of water!</p>
        {:else if waterIntakeTotalRes.total_volume >= 0.5 && waterIntakeTotalRes.total_volume < 1}
            <p>Keep going!</p>
        {:else if waterIntakeTotalRes.total_volume >= 1 && waterIntakeTotalRes.total_volume < 1.5}
            <p>Halfway there!</p>
        {:else if waterIntakeTotalRes.total_volume >= 1.5 && waterIntakeTotalRes.total_volume < 2}
            <p>Almost there!</p>
        {:else if waterIntakeTotalRes.total_volume >= 2}
            <p>Good job!</p>
        {/if}

        <p>{waterIntakeTotalRes.total_volume} L</p>

        {@const waterLevel = Math.min(waterIntakeTotalRes.total_volume / 2, 1)}
        <div>
            <WaterCup level={waterLevel} />
        </div>
    {/await}

    <Button btnTxt="Record" on:click={openModal} />
    <Modal bind:isOpen={modalOpen}>
        <div
            slot="modal-background"
            class="waterWaveContainer"
            style="top: {levelPercent}%"
        >
            <svg
                viewBox="0 0 500 100"
                preserveAspectRatio="none"
                class="waterWave"
                height="100"
            >
                <path
                    d="M0,40 C150,90 350,10 500,40 L500,100 L0,100 Z"
                    style="stroke: none; fill: #74ccf4;"
                >
                    <animate
                        attributeName="d"
                        dur="1.5s"
                        repeatCount="indefinite"
                        keyTimes="0;0.5;1"
                        values="
                    M0,40 C150,90 350,10 500,40 L500,100 L0,100 Z;
                    M0,40 C150,10 350,90 500,40 L500,100 L0,100 Z;
                    M0,40 C150,90 350,10 500,40 L500,100 L0,100 Z
                "
                    >
                    </animate>
                </path>
            </svg>

            <div class="waterBody"></div>
        </div>
        <div class="modal-wrapper">
            <p>Today's Water Intake</p>

            <div class="volume-buttons">
                <CircleButton
                    on:click={async () => {
                        newVolume = Math.max(0, newVolume - 0.25);
                    }}
                >
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
                </CircleButton>
                <p>{newVolume} L</p>
                <CircleButton
                    on:click={() => {
                        newVolume += 0.25;
                    }}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="white"
                    >
                        <path
                            d="M10.75 4.75a.75.75 0 0 0-1.5 0v4.5h-4.5a.75.75 0 0 0 0 1.5h4.5v4.5a.75.75 0 0 0 1.5 0v-4.5h4.5a.75.75 0 0 0 0-1.5h-4.5v-4.5Z"
                        />
                    </svg>
                </CircleButton>
            </div>
            <Button btnTxt="Save" on:click={updateWaterIntake} />
        </div>
    </Modal>
</div>

<style>
    .waterintake-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 100%;
    }

    .waterintake-wrapper > p:nth-child(1) {
        margin: 0 0 10px 0;
        font-size: 30px;
    }

    .waterintake-wrapper > p:nth-child(2) {
        margin: 0 0 10px 0;
        font-size: 50px;
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

    .modal-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 100%;
    }

    .modal-wrapper > p {
        margin: 0 0 20px 0;
    }

    .waterWaveContainer {
        display: flex;
        flex-direction: column;

        position: absolute;
        left: 0;
        width: 100%;
        height: 100%;
        transition: top 0.3s ease;
        opacity: 0.5;

        z-index: 1;
        pointer-events: none;
    }

    .waterWave {
        flex: 0 0 auto;
    }

    .waterBody {
        flex: 1 1 auto;
        width: 100%;
        margin-top: -2px;
        background: linear-gradient(180deg, #74ccf4, #00adf1);
    }
</style>
