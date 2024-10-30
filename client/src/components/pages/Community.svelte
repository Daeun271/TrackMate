<script>
    import EmptyPage from '../EmptyPage.svelte';
    import imageUrl from '../../assets/icons/three-friends.png?url';
    import GroupCreateModal from '../community/GroupCreateModal.svelte';
    import PostModal from '../community/PostModal.svelte';
    import PostCreateIcon from '../community/PostCreateIcon.svelte';
    import SideBar from '../community/SideBar.svelte';
    import InviteButton from '../community/InviteButton.svelte';
    import Comment from '../community/Comment.svelte';
    import { onMount, afterUpdate } from 'svelte';
    import { getGroups, searchPosts, deletePost, addMember } from '../../api';
    import { formatDate } from './FoodIntake.svelte';
    import { paramsInviteCode, clearParamsInviteCode } from '../../tabs';

    let isModalOpen = false;
    let isPostModalOpen = false;
    let isAdding = true;
    let isListOpen = false;

    let groups = [];
    let posts = [];
    let postProps = {};
    let loading = false;
    let currentGroupId = null;
    let currentGroupName = null;
    let currentGroupCode = '';

    async function getCurrentPosts() {
        loading = true;

        const searchDate = new Date(
            new Date().setDate(new Date().getDate() + 3),
        );

        const postsRes = await searchPosts(
            currentGroupId,
            formatDate(searchDate),
        );
        posts = postsRes.posts;

        if (posts.length === 0) {
            loading = false;
            return;
        }

        loading = false;
    }

    onMount(async () => {
        if (loading) return;
        loading = true;

        let invitedGroudId = null;

        if (paramsInviteCode) {
            const groupId = await addMember(paramsInviteCode);
            if (groupId) {
                invitedGroudId = groupId;
            } else {
                alert('Invalid invite code!');
            }
            clearParamsInviteCode();
        }

        const result = await getGroups();
        groups = result.groups;

        if (groups.length === 0) {
            loading = false;
            return;
        }

        if (invitedGroudId !== null) {
            localStorage.setItem(
                'currentGroupId',
                JSON.stringify(invitedGroudId),
            );
            currentGroupId = invitedGroudId;
        }

        if (localStorage.getItem('currentGroupId')) {
            currentGroupId = JSON.parse(localStorage.getItem('currentGroupId'));
        } else {
            currentGroupId = groups[0].id;
            localStorage.setItem(
                'currentGroupId',
                JSON.stringify(currentGroupId),
            );
        }

        await getCurrentPosts();
    });

    afterUpdate(() => {
        loadData();
    });

    let scrollDiv = null;
    let scrollDivResizeObserver = new ResizeObserver(() => {
        loadData();
    });
    $: {
        if (scrollDiv) {
            scrollDivResizeObserver.observe(scrollDiv);
        } else {
            scrollDivResizeObserver.disconnect();
        }
    }

    function getCurrentPostsIfNotLoading() {
        if (!loading) {
            getCurrentPosts();
        }
    }

    $: {
        if (currentGroupId) {
            currentGroupName = groups.find(
                (group) => group.id === currentGroupId,
            ).name;

            currentGroupCode = groups.find(
                (group) => group.id === currentGroupId,
            ).code;

            getCurrentPostsIfNotLoading();
        }
    }

    let isMobile = window.matchMedia('(max-width: 480px)').matches;
    window.matchMedia('(max-width: 480px)').addEventListener('change', (e) => {
        isMobile = e.matches;
    });

    let loadedAll = false;

    async function loadData(event) {
        if (loadedAll) return;

        let shouldLoad = false;

        if (!scrollDiv) return;

        if (loading) return;

        if (posts.length === 0) return;

        if (isMobile) {
            if (
                scrollDiv.scrollTop + scrollDiv.clientHeight >=
                scrollDiv.scrollHeight - 30
            ) {
                shouldLoad = true;
            }
        } else {
            if (
                scrollDiv.scrollTop + scrollDiv.clientHeight >=
                scrollDiv.scrollHeight - 60
            ) {
                shouldLoad = true;
            }
        }

        if (shouldLoad) {
            loading = true;

            const lastDate = new Date(posts[posts.length - 1].created_at);

            const postsRes = await searchPosts(
                currentGroupId,
                formatDate(lastDate),
            );

            if (postsRes.posts.length === 0) {
                loadedAll = true;
                loading = false;
                return;
            }

            posts = [...posts, ...postsRes.posts];
        }

        loading = false;
    }

    function displayPost(post) {
        postProps = structuredClone({
            groupId: currentGroupId,
            postId: post.id,
            title: post.title,
            content: post.content,
            createdAt: post.created_at,
        });

        isAdding = false;
        isPostModalOpen = true;
    }

    async function deleteGroupPost(post) {
        await deletePost(post.id);
        posts = posts.filter((p) => p.id !== post.id);
    }

    function addGroup(group) {
        groups = [...groups, group];
        localStorage.setItem('currentGroupId', JSON.stringify(group.id));
        currentGroupId = group.id;
    }

    let postIdForCurrentCommentOpen = null;

    function toggleComments(postId) {
        postIdForCurrentCommentOpen =
            postIdForCurrentCommentOpen === postId ? null : postId;
    }
</script>

{#if groups.length === 0}
    {#if loading}
        <div class="loader-box">
            <span class="loader"></span>
        </div>
    {:else}
        <EmptyPage
            text1="Don't you have any groups yet?"
            text2="Create a group and invite your friends!"
            {imageUrl}
            on:modalClick={() => {
                isModalOpen = true;
            }}
        ></EmptyPage>
    {/if}
{:else}
    <div class="wrapper">
        <div class="content" bind:this={scrollDiv} on:scroll={loadData}>
            <div class="group-info-box">
                <h1>{currentGroupName}</h1>
                <InviteButton bind:groupCode={currentGroupCode}></InviteButton>
            </div>
            {#if posts.length === 0}
                {#if loading}
                    <div class="loader-box">
                        <span class="loader"></span>
                    </div>
                {:else}
                    <EmptyPage
                        text1="No posts yet!"
                        text2="Create a post and share it with your friends!"
                        on:modalClick={() => {
                            isAdding = true;
                            isPostModalOpen = true;
                        }}
                    ></EmptyPage>
                {/if}
            {:else}
                <PostCreateIcon
                    text="Add a post"
                    on:modalClick={() => {
                        isAdding = true;
                        isPostModalOpen = true;
                    }}
                ></PostCreateIcon>
                {#each posts as post}
                    <div class="post-box">
                        <div class="post-meta-data">
                            <p>{post.user_name}</p>
                            <p>{post.created_at.split('T')[0]}</p>
                        </div>
                        <div class="post-content">
                            <h3>{post.title}</h3>
                            <p>{post.content}</p>
                        </div>
                        <div class="post-icons">
                            <img
                                src="images/icons8-bemerkungen-24.png"
                                alt="comment"
                                class="comment"
                                on:click={() => toggleComments(post.id)}
                            />
                            {#if post.is_user}
                                <div class="post-action">
                                    <button
                                        class="icon-button"
                                        on:click={() => displayPost(post)}
                                        >⚙️</button
                                    >
                                    <button
                                        class="icon-button"
                                        on:click={async () =>
                                            deleteGroupPost(post)}>🚮</button
                                    >
                                </div>
                            {/if}
                        </div>
                        <Comment
                            isCommentOpen={postIdForCurrentCommentOpen ===
                                post.id}
                            bind:postId={post.id}
                        />
                    </div>
                {/each}
            {/if}
        </div>
        <img
            src="images/icons8-liste-30.png"
            alt="list"
            class="list"
            on:click={() => {
                isListOpen = true;
            }}
        />
        <SideBar
            bind:isListOpen
            {groups}
            on:change={() => {
                currentGroupId = JSON.parse(
                    localStorage.getItem('currentGroupId'),
                );
                isListOpen = false;
            }}
            on:add={(event) => {
                addGroup(event.detail);
                isListOpen = false;
            }}
        ></SideBar>
    </div>
{/if}

<GroupCreateModal
    bind:isModalOpen
    on:add={(event) => {
        addGroup(event.detail);
    }}
></GroupCreateModal>
<PostModal
    bind:isPostModalOpen
    {isAdding}
    bind:groupId={currentGroupId}
    bind:post={postProps}
    on:create={(event) => {
        posts = [event.detail, ...posts];
    }}
    on:update={(event) => {
        const updatedPost = event.detail;
        const index = posts.findIndex((post) => post.id === updatedPost.id);
        posts[index] = updatedPost;
    }}
    on:delete={(event) => {
        posts = posts.filter((post) => post.id !== event.detail.postId);
    }}
></PostModal>

<style>
    .wrapper {
        display: flex;
        width: 100%;
        height: 100%;

        position: relative;

        overflow-x: hidden;
    }

    .content {
        display: flex;
        flex-direction: column;
        row-gap: 20px;
        padding: 20px;
        width: 100%;

        overflow-y: auto;
    }

    .list {
        position: absolute;
        right: 20px;
        top: 10px;

        cursor: pointer;
    }

    .group-info-box {
        display: flex;
        flex-direction: row;
        column-gap: 20px;
        height: 50px;

        border-bottom: 1px solid #c7c7c7;
    }

    .group-info-box h1 {
        margin: 0 0 10px 0;
    }

    h1,
    h3,
    p {
        margin: 0;
    }

    .post-box {
        display: flex;
        flex-direction: column;
        row-gap: 10px;
        padding: 10px;
        border: 1px solid #c7c7c7;
        border-radius: 5px;
    }

    .post-meta-data {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        font-size: 13px;
    }

    .post-content {
        display: flex;
        flex-direction: column;
        row-gap: 5px;
        padding: 10px;
        background-color: #f0f0f0;
    }

    .post-icons {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        column-gap: 10px;
    }

    .post-icons img {
        width: 20px;
        height: 20px;
        cursor: pointer;
    }

    .post-action {
        display: flex;
        flex-direction: row;
        column-gap: 10px;
    }

    .post-action button {
        appearance: none;
        width: 20px;
        height: 20px;
        font-size: 17px;
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
</style>
