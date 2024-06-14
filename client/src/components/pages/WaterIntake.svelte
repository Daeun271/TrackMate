<script>
    import WaterCup from '../water_intakes/WaterCup.svelte';
    import CircleButton from '../water_intakes/CircleButton.svelte';
    import Modal from '../Modal.svelte';
    import Button from '../water_intakes/Button.svelte';

    let volume = 0;

    $: water_level = Math.min(volume / 2, 1);

    let modalOpen = false;
</script>

<div class="waterintake-wrapper">
    <p>Today's Water Intake</p>
    <p>{volume} L</p>
    <div>
        <WaterCup level={water_level} />
    </div>
    <Button btnTxt="Record" on:click={() => (modalOpen = true)} />
    {#if modalOpen}
        <Modal on:close={() => (modalOpen = false)}>
            <div class="modal-wrapper">
                <p>Let's drink 2L of water</p>
                <div class="volume-buttons">
                    <CircleButton
                        on:click={() => {
                            volume = Math.max(0, volume - 0.25);
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
                    <p>{volume} L</p>
                    <CircleButton
                        on:click={() => {
                            volume += 0.25;
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
                <Button btnTxt="Save" on:click={() => (modalOpen = false)} />
            </div>
        </Modal>
    {/if}
</div>

<style>
    .waterintake-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 100%;
    }

    .waterintake-wrapper > p {
        margin: 0 0 10px 0;
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
</style>
