<script>
    import Modal from './GroupCreateModal.svelte';
    import GroupList from './GroupList.svelte';
    import { getMembers } from '../../api';
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    export let isListOpen = false;
    let isModalOpen = false;

    function onClick() {
        isListOpen = false;
    }

    export let groups = [];

    let members = [];
    async function getGroupMembers(groupId) {
        members = await getMembers(groupId);
    }

    async function addGroup(newGroup) {
        groups = [...groups, newGroup];
    }
</script>

<div class="list-bg" class:isListOpen>
    <div class="list-wrapper">
        <button class="list-close" on:click={onClick}>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="size-6"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M6 18 18 6M6 6l12 12"
                />
            </svg>
        </button>
        <div class="list-content">
            {#each groups as group}
                <div class="group-container">
                    <GroupList
                        on:open={() => getGroupMembers(group.id)}
                        groupName={group.name}
                        {members}
                        on:move={() => {
                            localStorage.setItem(
                                'currentGroupId',
                                JSON.stringify(group.id),
                            );
                            dispatch('change');
                        }}
                        {isListOpen}
                    ></GroupList>
                </div>
            {/each}
            <button class="create-btn" on:click={() => (isModalOpen = true)}
                >Create Group</button
            >
        </div>
    </div>
</div>

<Modal bind:isModalOpen on:add={(event) => addGroup(event.detail)}></Modal>

<svelte:window
    on:keydown={(e) => e.key === 'Escape' && isListOpen && onClick()}
/>

<style>
    .list-bg {
        position: absolute;
        top: 0;
        right: 0;
        width: 100%;
        height: 100%;

        background-color: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(5px);

        z-index: 99;

        opacity: 0;
        transition: opacity 0.3s;
        pointer-events: none;
    }

    .list-bg.isListOpen {
        opacity: 1;
        pointer-events: auto;
    }

    .list-wrapper {
        position: absolute;
        top: 0;
        right: 0;
        width: 50%;
        height: 100%;

        background-color: #fff;
        border-left: 1px solid #8f8b8b;
        border-radius: 10px 0 0 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);

        display: flex;
        flex-direction: column;

        z-index: 100;

        transform: translateX(100%);
        transition: transform 0.3s;
    }

    .isListOpen .list-wrapper {
        transform: translateX(0);
    }

    .list-close {
        margin-left: auto;
        width: 50px;
        height: 50px;
        color: #000;
        background-color: transparent;
        border: none;
        cursor: pointer;
    }

    .list-content {
        flex: 1 1 auto;
        overflow-y: auto;

        display: flex;
        flex-direction: column;
        row-gap: 20px;
        padding: 20px;
    }

    .group-container {
        display: flex;
        align-items: center;

        padding-bottom: 10px;

        border-bottom: 1px solid #c7c7c7;
    }

    .create-btn {
        width: 100%;
        height: 35px;
        padding: 10px;

        text-align: center;
        color: #000;

        background-color: #fff;
        border: 1px solid #c7c7c7;
        border-radius: 3px;

        cursor: pointer;

        appearance: none;
    }
</style>
