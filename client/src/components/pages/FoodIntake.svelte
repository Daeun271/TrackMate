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
    import Modal from '../food_intakes/Modal.svelte';
    import CircleButton from '../CircleButton.svelte';
    import { getFoodImageUrl, searchFoodIntakes } from '../../api';
    import EmptyPage from '../EmptyPage.svelte';
    import imageUrl from '../../assets/icons/vegan-food.png?url';
    import { onMount } from 'svelte';

    let isModalOpen = false;
    let isAdding = true;

    let foodDateList = [];
    let loading = false;

    onMount(async () => {
        if (loading) return;

        loading = true;

        const searchDate = new Date(
            new Date().setDate(new Date().getDate() + 3),
        );
        const foodIntakeRes = await searchFoodIntakes(formatDate(searchDate));

        if (foodIntakeRes.foods.length === 0) {
            loading = false;
            return;
        }

        for (let i = 0; i < foodIntakeRes.foods.length; i++) {
            const food = foodIntakeRes.foods[i];

            if (food.has_image === true) {
                food.img_src = getFoodImageUrl(food.uid);
            } else {
                food.img_src = null;
            }

            food.priority =
                timeCategoryPriorities[food.time_category] ?? Infinity;

            let found = false;

            for (let j = 0; j < foodDateList.length; j++) {
                if (foodDateList[j].date === food.consumed_at) {
                    for (let k = 0; k < foodDateList[j].foods.length; k++) {
                        if (food.priority < foodDateList[j].foods[k].priority) {
                            foodDateList[j].foods.splice(k, 0, food);
                            found = true;
                            break;
                        }
                    }

                    if (!found) {
                        foodDateList[j].foods.push(food);
                        found = true;
                    }
                }
            }

            if (!found) {
                foodDateList.push({
                    date: food.consumed_at,
                    foods: [food],
                });
            }
        }

        foodDateList = foodDateList.toSorted(
            (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
        );

        loading = false;
    });

    function addFoodIntake(event) {}

    let foodIntake = null;

    function displayFoodIntake(food) {
        foodIntake = structuredClone(food);
        isAdding = false;
        isModalOpen = true;
    }

    function updateFoodIntake(event) {
        console.log(event.detail);
    }

    function deleteFoodIntake(event) {
        console.log(event.detail);
    }

    let scrollDiv;

    function loadData(event) {
        if (
            scrollDiv.scrollHeight - scrollDiv.scrollTop ===
            scrollDiv.clientHeight
        ) {
            console.log('loading more data');
        }
    }
</script>

{#if foodDateList.length === 0}
    {#if loading}
        <div>Loading...</div>
    {:else}
        <EmptyPage
            text1="No food intake found"
            text2="Get started by recoding your food intake"
            {imageUrl}
            on:modalClick={() => {
                isAdding = true;
                isModalOpen = true;
            }}
        ></EmptyPage>
    {/if}
{:else}
    <div class="background" bind:this={scrollDiv} on:scroll={loadData}>
        {#each foodDateList as entry (entry.date)}
            <h1>{entry.date}</h1>
            <div class="foodintake-wrapper">
                {#each entry.foods as food}
                    {#if food.img_src === null}
                        <div
                            class="name-container"
                            on:click={() => displayFoodIntake(food)}
                        >
                            <span>{food.name}</span>
                        </div>
                    {:else}
                        <img
                            src={food.img_src}
                            alt="food"
                            on:click={() => displayFoodIntake(food)}
                        />
                    {/if}
                {/each}
            </div>
            {#if loading}
                <div>Loading...</div>
            {/if}
        {/each}
        {#if !isModalOpen}
            <CircleButton
                floated
                on:click={() => {
                    isAdding = true;
                    isModalOpen = true;
                }}
            >
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
    </div>
{/if}

<Modal
    bind:isModalOpen
    bind:foodIntake
    bind:isAdding
    on:add={addFoodIntake}
    on:edit={updateFoodIntake}
    on:delete={deleteFoodIntake}
/>

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
        justify-content: space-around;
        grid-template-columns: repeat(auto-fill, 100px);
        grid-auto-rows: 100px;
        gap: 15px;
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
