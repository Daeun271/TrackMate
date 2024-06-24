<script>
    import { signUp } from '../../user.js';
    import { logIn } from '../../user.js';

    let isLogin = true;
    let name = '';
    let email = '';
    let password = '';
    let loginErrorMsg = '';
    let signupErrorMsg = '';

    async function validateAndLogIn(email, password) {
        try {
            await logIn(email, password);
        } catch (error) {
            loginErrorMsg = error.message;
            return;
        }

        email = '';
        password = '';
    }

    async function validateAndSignUp(name, email, password) {
        try {
            await signUp(name, email, password);
        } catch (error) {
            signupErrorMsg = error.message;
            return;
        }

        name = '';
        email = '';
        password = '';
    }
</script>

<div class="wrapper">
    {#if isLogin}
        <h1>Log In</h1>
        <div class="container">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" bind:value={email} />
            <label for="password">Password</label>
            <input
                type="password"
                id="password"
                name="password"
                bind:value={password}
            />
            <button on:click={() => validateAndLogIn(email, password)}
                >Log In</button
            >
            <p class="error-message">{loginErrorMsg}</p>
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
            <label for="name">Name</label>
            <input type="text" id="name" name="name" bind:value={name} />
            <label for="email">Email</label>
            <input type="email" id="email" name="email" bind:value={email} />
            <label for="password">Password</label>
            <input
                type="password"
                id="password"
                name="password"
                bind:value={password}
            />
            <button on:click={() => validateAndSignUp(name, email, password)}
                >Sign Up</button
            >
            <p class="error-message">{signupErrorMsg}</p>
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
    .wrapper {
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
        padding: 20px;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        width: min(calc(100dvw - 40px), 400px);
    }

    label {
        font-size: 20px;
        margin: 10px 0 5px 0;
    }

    input {
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ced4da;
        border-radius: 5px;
        outline: solid 2px #f8f8f8;
        width: 100%;
        height: 40px;
        font-size: 18px;
    }

    .container > button {
        margin-top: 10px;
        padding: 10px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }

    .container > button:hover {
        background-color: #0056b3;
    }

    .container > button:active {
        background-color: #004286;
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
        background-color: transparent;
        border: none;
        padding: 0;
        font-size: 18px;
        color: #007bff;
        cursor: pointer;
    }
</style>
