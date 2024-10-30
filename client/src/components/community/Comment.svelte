<script>
    import { buttonClick } from '../../button_click';
    import {
        createComment,
        getComments,
        updateComment,
        deleteComment,
    } from '../../api';
    import { formatDate } from '../pages/FoodIntake.svelte';

    let today = formatDate(new Date());

    let loading = false;
    let errorMessage = '';
    let updateErrorMessage = '';
    let editingCommentId = null;
    let commentContent = '';
    let newCommentsbyId = {};
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

    function displayEditBox(comment) {
        editingCommentId =
            editingCommentId === comment.comment_id ? null : comment.comment_id;
        newCommentsbyId[comment.comment_id] = comment.content;
        updateErrorMessage = '';
    }

    async function uploadComment(comment) {
        const newComment = newCommentsbyId[comment.comment_id];
        if (newComment.trim() === '') {
            updateErrorMessage = 'Please enter a comment';
            return;
        }

        if (comment.content === newComment) {
            updateErrorMessage = 'No changes detected';
            return;
        }

        try {
            await updateComment(comment.comment_id, newComment);
        } catch (error) {
            updateErrorMessage = 'An error occurred. Please try again later.';
            return;
        }

        comment.content = newComment;

        updateErrorMessage = '';
        editingCommentId = null;
    }

    async function removeComment(commentId) {
        await deleteComment(commentId);
        comments = comments.filter(
            (comment) => comment.comment_id !== commentId,
        );
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
                            <div class="comment-header-container">
                                <p>{comment.user_name}</p>
                                <p class="comment-date">
                                    {comment.created_at.split('T')[0]}
                                </p>
                            </div>
                            {#if comment.is_user}
                                <div class="comment-header-container">
                                    <button
                                        class="icon-button"
                                        on:click={() => displayEditBox(comment)}
                                        >⚙️</button
                                    >
                                    <button
                                        class="icon-button"
                                        on:click={() =>
                                            removeComment(comment.comment_id)}
                                        >🚮</button
                                    >
                                </div>
                            {/if}
                        </div>
                        {#if editingCommentId === comment.comment_id}
                            <div class="edit-box">
                                <input
                                    type="text"
                                    bind:value={newCommentsbyId[
                                        comment.comment_id
                                    ]}
                                />
                                <button on:click={() => uploadComment(comment)}
                                    >Save</button
                                >
                            </div>
                            <p
                                class="error-message"
                                style={'margin: 5px 0 0 0;'}
                            >
                                {updateErrorMessage}
                            </p>
                        {:else}
                            <p>{comment.content}</p>
                        {/if}
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
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .comment-header-container {
        display: flex;
        justify-content: flex-start;
        column-gap: 10px;
    }

    .comment-date {
        color: #6c757d;
        font-size: 12px;
        padding-top: 5px;
    }

    .icon-button {
        appearance: none;
        font-size: 15px;
        padding: 0;
        background-color: transparent;
        border: none;
        cursor: pointer;
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

    .edit-box {
        display: flex;
        column-gap: 10px;
        margin-top: 10px;
    }
</style>
