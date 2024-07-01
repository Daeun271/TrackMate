<script>
    import { signUp } from '../../user.js';
    import { logIn } from '../../user.js';
    import Loader from '../Loader.svelte';
    import Button from '../Button.svelte';

    let isLogin = true;
    let name = '';
    let email = '';
    let password = '';
    let loginErrorMsg = '';
    let signupErrorMsg = '';
    let isLoading = false;

    async function validateAndLogIn(email, password) {
        if (isLoading) {
            return;
        }
        isLoading = true;

        try {
            await logIn(email, password);
        } catch (error) {
            loginErrorMsg = error.message;
        }

        isLoading = false;

        email = '';
        password = '';
    }

    async function validateAndSignUp(name, email, password) {
        if (isLoading) {
            return;
        }
        isLoading = true;

        try {
            await signUp(name, email, password);
        } catch (error) {
            signupErrorMsg = error.message;
        }

        isLoading = false;

        name = '';
        email = '';
        password = '';
    }
</script>

<div class="background">
    {#if isLogin}
        <h1>Log In</h1>
        <div class="container">
            <div class="input-wrapper">
                <div class="label-input">
                    <label for="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        bind:value={email}
                    />
                </div>
                <div class="label-input">
                    <label for="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        bind:value={password}
                    />
                </div>
            </div>
            <div>
                <Button
                    bind:isLoading
                    on:click={() => validateAndLogIn(email, password)}
                >
                    {#if isLoading}
                        <Loader></Loader>
                    {:else}
                        <span>Log In</span>
                    {/if}
                </Button>
                <p class="error-message">{loginErrorMsg}</p>
            </div>
        </div>
        <div class="container-outside">
            <p>Don't have an account?</p>
            <button
                on:click={() => {
                    isLogin = false;
                }}>Sign Up</button
            >
        </div>
    {:else}
        <h1>Sign Up</h1>
        <div class="container">
            <div class="input-wrapper">
                <div class="label-input">
                    <label for="name">Name</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        bind:value={name}
                    />
                </div>
                <div class="label-input">
                    <label for="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        bind:value={email}
                    />
                </div>
                <div class="label-input">
                    <label for="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        bind:value={password}
                    />
                </div>
            </div>
            <div>
                <Button
                    bind:isLoading
                    on:click={() => validateAndSignUp(name, email, password)}
                >
                    {#if isLoading}
                        <Loader></Loader>
                    {:else}
                        <span>Sign Up</span>
                    {/if}
                </Button>
                <p class="error-message">{signupErrorMsg}</p>
            </div>
        </div>
        <div class="container-outside">
            <p>Already have an account?</p>
            <button
                on:click={() => {
                    isLogin = true;
                }}>Log In</button
            >
        </div>
    {/if}
</div>

<style>
    .background {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        row-gap: 20px;
        height: 100dvh;
        background-color: #f8f8f8;
    }

    h1 {
        margin: 0;
    }

    .container {
        display: flex;
        flex-direction: column;
        row-gap: 30px;
        padding: 30px 20px 20px 20px;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        width: min(calc(100dvw - 40px), 400px);
    }

    .input-wrapper {
        display: flex;
        flex-direction: column;
        row-gap: 20px;
    }

    .label-input {
        display: flex;
        flex-direction: column;
        row-gap: 5px;
    }

    label {
        font-size: 20px;
        pointer-events: none;
    }

    input {
        padding: 10px;
        border: 1px solid #ced4da;
        border-radius: 5px;
        outline: solid 2px #f8f8f8;
        width: 100%;
        height: 40px;
        font-size: 18px;
    }

    .error-message {
        color: #f50707;
        font-size: 15px;
        margin: 5px 0 0 0;
    }

    .container-outside {
        display: flex;
        flex-direction: row;
        column-gap: 10px;
    }

    .container-outside > p {
        margin: 0;
        font-size: 18px;
    }

    .container-outside > button {
        appearance: none;
        background-color: transparent;
        border: none;
        padding: 0;
        font-size: 18px;
        color: #007bff;
        cursor: pointer;
    }
</style>
