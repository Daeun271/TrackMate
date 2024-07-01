<script context="module">
    export function formatDate(date) {
        const year = date.getFullYear();
        const month = ('0' + (date.getMonth() + 1)).slice(-2);
        const day = ('0' + date.getDate()).slice(-2);

        return `${year}-${month}-${day}`;
    }

    const timeCategoryPriorities = {
        BREAKFAST: 1,
        LUNCH: 2,
        DINNER: 3,
        DESSERT: 4,
        NIGHT_SNACK: 5,
    };
</script>

<script>
    import AddingModal from '../food_intakes/AddingModal.svelte';
    import EditingModal from '../food_intakes/EditingModal.svelte';
    import CircleButton from '../CircleButton.svelte';
    import { getFoodIntakesTotal, getFoodImageUrl } from '../../api';

    let addingModalOpen = false;
    let showingModalOpen = false;

    let foodIntakePromise = getFoodIntakes();

    async function getFoodIntakes() {
        const today = new Date();
        const tomorrow = new Date(today.setDate(today.getDate() + 1));
        const lastWeek = new Date(today.setDate(today.getDate() - 7));
        const foodIntakeRes = await getFoodIntakesTotal(
            formatDate(lastWeek),
            formatDate(tomorrow),
        );

        if (foodIntakeRes.foods.length === 0) {
            return null;
        }

        const foods = {};

        for (let i = 0; i < foodIntakeRes.foods.length; i++) {
            const food = foodIntakeRes.foods[i];

            if (food.has_image === true) {
                food.imgSrc = getFoodImageUrl(food.uid);
            } else {
                food.imgSrc = null;
            }

            food.priority =
                timeCategoryPriorities[food.time_category] ?? Infinity;

            if (!(food.consumed_at in foods)) {
                foods[food.consumed_at] = [food];
            } else {
                foods[food.consumed_at].push(food);
            }
        }

        for (const key in foods) {
            foods[key] = foods[key].sort((a, b) => a.priority - b.priority);
        }

        return foods;
    }

    async function addFoodIntake(event) {
        let foods = await foodIntakePromise;

        const food = {
            calories: Number(event.detail.userInputs.calories),
            name: event.detail.userInputs.name,
            consumed_at: event.detail.userInputs.date,
            time_category: event.detail.userInputs.timeCategory || null,
            has_image: event.detail.userInputs.imageUrl !== '',
            imgSrc: event.detail.userInputs.imageUrl || null,
            priority:
                timeCategoryPriorities[event.detail.userInputs.timeCategory] ??
                Infinity,
            uid: event.detail.userInputs.uid,
        };

        if (foods) {
            if (food.consumed_at in foods) {
                foods[food.consumed_at].push(food);
                foods[food.consumed_at] = foods[food.consumed_at].sort(
                    (a, b) => a.priority - b.priority,
                );
            } else {
                foods[food.consumed_at] = [food];
            }
        } else {
            foods = {
                [food.consumed_at]: [food],
            };
        }

        foodIntakePromise = Promise.resolve(foods);
    }
</script>

<div class="background">
    {#await foodIntakePromise}
        <p>loading...</p>
    {:then foods}
        {#if !foods}
            <div class="empty-container">
                <p>There is no food intake data.</p>
                <p>Click the button below to record your food intake.</p>
                <svg
                    on:click={() => (addingModalOpen = true)}
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
        {:else}
            {#each Object.keys(foods) as date}
                <h1>{date}</h1>
                <div
                    class="foodintake-wrapper"
                    on:click={() => (showingModalOpen = true)}
                >
                    {#each foods[date] as food}
                        {#if food.imgSrc === null}
                            <div class="name-container">
                                <span>{food.name}</span>
                            </div>
                        {:else}
                            <img
                                src={food.imgSrc}
                                alt="food"
                                on:click={() => (showingModalOpen = true)}
                            />
                        {/if}
                    {/each}
                </div>
            {/each}
            {#if !showingModalOpen && !addingModalOpen}
                <CircleButton floated on:click={() => (addingModalOpen = true)}>
                    <svg
                        class="floating-button"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M12 9v6m3-3H9"
                        />
                    </svg>
                </CircleButton>
            {/if}
        {/if}
    {/await}

    <AddingModal
        bind:isAddingModalOpen={addingModalOpen}
        on:add={addFoodIntake}
    />
    <EditingModal bind:isEditingModalOpen={showingModalOpen} />
</div>

<style>
    .background {
        display: flex;
        flex-direction: column;
        row-gap: 20px;
        overflow-y: auto;
        height: 100%;
        padding: 20px;
    }

    .background h1 {
        margin: 0;
        font-size: 30px;
    }

    .foodintake-wrapper {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        grid-auto-rows: 100px;
        gap: 20px;
    }

    .foodintake-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        cursor: pointer;
    }

    .floating-button {
        width: 50px;
        height: 50px;
        cursor: pointer;
    }

    .empty-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: none;
        margin-top: auto;
        margin-bottom: auto;
        row-gap: 20px;
    }

    .empty-container p {
        margin: 0;
    }

    .empty-container svg {
        width: 100px;
        height: 100px;
        cursor: pointer;
    }

    .name-container {
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #ced4da;
        border-radius: 5px;
        outline: solid 2px #f8f8f8;
        padding: 10px;
        font-size: 20px;
        cursor: pointer;
    }
</style>
