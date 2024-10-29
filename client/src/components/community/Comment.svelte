<script>
    import { buttonClick } from '../../button_click';

    let loading = false;
    let comments = [
        {
            username: 'John Doe',
            date: '2021-09-01',
            text: 'This is a comment',
        },
        {
            username: 'Jane Doe',
            date: '2021-09-02',
            text: 'This is another comment',
        },
    ];

    export let isCommentOpen = false;
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
                    <input type="text" placeholder="Add a comment" />
                    <button use:buttonClick>Post</button>
                </div>
                <p class="error-message"></p>
            </div>

            {#if comments.length}
                {#each comments as comment}
                    <div class="comment">
                        <div class="comment-header">
                            <p>{comment.username}</p>
                            <p class="comment-date">{comment.date}</p>
                        </div>
                        <p>{comment.text}</p>
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
