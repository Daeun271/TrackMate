<script>
    import { buttonClick } from '../../button_click';
    import { createComment, getComments } from '../../api';
    import { formatDate } from '../pages/FoodIntake.svelte';

    let today = formatDate(new Date());

    let loading = false;
    let errorMessage = '';
    let commentContent = '';
    let comments = [];

    export let isCommentOpen = false;
    export let postId = null;

    async function addComment() {
        if (loading) return;
        loading = true;

        if (commentContent.trim() === '') {
            errorMessage = 'Please enter a comment';
            loading = false;
            return;
        }

        try {
            const newComment = await createComment(
                postId,
                commentContent,
                today,
            );
            comments = [newComment, ...comments];
        } catch (error) {
            errorMessage = 'An error occurred. Please try again later.';
            loading = false;
            return;
        }

        loading = false;
        commentContent = '';
        errorMessage = '';
    }

    async function fetchComments(postId) {
        if (loading) return;
        loading = true;

        try {
            const res = await getComments(postId);
            comments = res.comments;
        } catch (error) {
            errorMessage = 'An error occurred. Please try again later.';
            loading = false;
            return;
        }

        loading = false;
        errorMessage = '';
    }

    $: {
        if (isCommentOpen) {
            fetchComments(postId);
        }
    }

    $: {
        if (isCommentOpen === false) {
            errorMessage = '';
        }
    }
</script>

{#if isCommentOpen}
    {#if loading}
        <div class="loader-box">
            <span class="loader"></span>
        </div>
    {:else}
        <div class="comment-wrapper">
            <div class="input-box-wrapper">
                <div class="input-box">
                    <input
                        type="text"
                        placeholder="Add a comment"
                        bind:value={commentContent}
                    />
                    <button use:buttonClick on:click={addComment}>Post</button>
                </div>
                <p class="error-message">{errorMessage}</p>
            </div>

            {#if comments.length}
                {#each comments as comment}
                    <div class="comment">
                        <div class="comment-header">
                            <p>{comment.user_name}</p>
                            <p class="comment-date">
                                {comment.created_at.split('T')[0]}
                            </p>
                        </div>
                        <p>{comment.content}</p>
                    </div>
                {/each}
            {/if}
        </div>
    {/if}
{/if}

<style>
    .comment-wrapper {
        display: flex;
        flex-direction: column;
        row-gap: 20px;
        padding: 20px 10px 10px 10px;
        margin-top: 10px;
        width: 100%;
        border-top: 1px solid #b8b7b7;
    }

    .input-box-wrapper {
        display: flex;
        flex-direction: column;
    }

    .input-box {
        display: flex;
        column-gap: 10px;
        width: 100%;
        height: 35px;
    }

    input {
        width: 100%;
        padding: 10px;
        border: 1px solid #b8b7b7;
        border-radius: 5px;
        outline: none;
    }

    button {
        padding: 10px;
        border: none;
        border-radius: 5px;
        background-color: #007bff;
        color: white;
        cursor: pointer;
    }

    button:global(.clicked) {
        background-color: #0056b3;
    }

    .error-message {
        color: #f50707;
        font-size: 15px;
        margin: 5px 0 0 0;
    }

    .comment {
        display: flex;
        flex-direction: column;
        padding: 10px;
        border: 1px solid #b8b7b7;
        border-radius: 5px;
    }

    .comment p {
        margin: 0;
    }

    .comment-header {
        display: flex;
        justify-content: flex-start;
        column-gap: 10px;
        margin-bottom: 10px;
    }

    .comment-date {
        color: #6c757d;
        font-size: 12px;
        padding-top: 5px;
    }

    .loader-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    .loader {
        width: 48px;
        height: 48px;
        border: 5px solid #b8b7b7;
        border-bottom-color: transparent;
        border-radius: 50%;
        display: inline-block;
        box-sizing: border-box;
        animation: rotation 1s linear infinite;
    }

    @keyframes rotation {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
</style>
