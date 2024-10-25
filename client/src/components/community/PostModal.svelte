<script>
    import Modal from '../Modal.svelte';
    import Button from '../Button.svelte';
    import Loader from '../Loader.svelte';
    import { createEventDispatcher } from 'svelte';
    import { createPost, updatePost, deletePost } from '../../api';
    import { formatDate } from '../pages/FoodIntake.svelte';

    const dispatch = createEventDispatcher();

    export let isPostModalOpen = false;
    let isLoading = false;
    let errorMessage = '';
    export let isAdding = true;

    export let post = {};
    export let groupId;
    let today = formatDate(new Date());
    function getInitialInputs() {
        return {
            groupId: groupId,
            postId: null,
            title: '',
            content: '',
            createdAt: today,
        };
    }
    post = getInitialInputs();

    $: {
        post.groupId = groupId;
    }

    async function uploadPost() {
        if (isLoading) return;
        isLoading = true;

        if (post.title.trim() === '' || post.content.trim() === '') {
            errorMessage = 'Please fill all the required fields.';
            isLoading = false;
            return;
        }

        if (isAdding) {
            try {
                post = await createPost(
                    post.groupId,
                    post.title,
                    post.content,
                    post.createdAt,
                );
            } catch (error) {
                errorMessage = 'Failed to create post. Please try again.';
                isLoading = false;
                return;
            }
        } else {
            try {
                post = await updatePost(post.postId, post.title, post.content);
            } catch (error) {
                errorMessage = 'Failed to update post. Please try again.';
                isLoading = false;
                return;
            }
        }

        isLoading = false;
        if (isAdding) {
            dispatch('create', post);
        } else {
            dispatch('update', post);
        }

        isPostModalOpen = false;
        post = getInitialInputs();
    }

    let deleteErrorMessage = '';
    async function removePost() {
        await deletePost(post.postId);
        dispatch('delete', post);
        isPostModalOpen = false;
    }
</script>

<Modal
    bind:isOpen={isPostModalOpen}
    on:close={() => {
        errorMessage = '';
        post = getInitialInputs();
    }}
>
    <div class="modal-wrapper">
        <div class="input-container">
            <label for="title">Title<span class="required">*</span></label>
            <input
                type="text"
                id="title"
                name="title"
                bind:value={post.title}
            />
            <label for="content">Content<span class="required">*</span></label>
            <textarea id="content" name="content" bind:value={post.content}
            ></textarea>
            {#if isAdding}
                <Button bind:isLoading isExpanded={true} on:click={uploadPost}>
                    {#if isLoading}
                        <Loader></Loader>
                    {:else}
                        <span>Post</span>
                    {/if}
                </Button>
                <p class="error-message">{errorMessage}</p>
            {:else}
                <Button bind:isLoading isExpanded={true} on:click={uploadPost}>
                    {#if isLoading}
                        <Loader></Loader>
                    {:else}
                        <span>Edit</span>
                    {/if}
                </Button>
                <p class="error-message">{errorMessage}</p>
                <Button
                    bind:isLoading
                    isExpanded={true}
                    backgroundColor="#f50707"
                    on:click={removePost}
                >
                    {#if isLoading}
                        <Loader></Loader>
                    {:else}
                        <span>Delete</span>
                    {/if}
                </Button>
                <p class="error-message">{deleteErrorMessage}</p>
            {/if}
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
        width: min(calc(100dvw - 40px), 400px);
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

    textarea {
        resize: none;

        width: 100%;
        height: 300px;
        padding: 10px;
        margin-bottom: 20px;
        border: 1px solid #ced4da;
        border-radius: 5px;
        outline: solid 2px #f8f8f8;
        font-size: 18px;
        color: #000;
        background-color: #fff;
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
