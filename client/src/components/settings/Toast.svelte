<script>
    export let success = false;
    export let message = '';
</script>

{#if success}
    <div class="toast">
        <p>{message}</p>
    </div>
{/if}

<style>
    .toast {
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        padding: 10px;
        background-color: #000000;
        border-radius: 5px;
        color: #fff;
        animation: fadeInOut 1.5s;
        -webkit-animation: fadeInOut 1.5s;
        -moz-animation: fadeInOut 1.5s;
    }

    @keyframes fadeInOut {
        0% {
            opacity: 0;
        }
        10% {
            opacity: 0.5;
        }
        20% {
            opacity: 1;
        }
        80% {
            opacity: 1;
        }
        90% {
            opacity: 0.5;
        }
        100% {
            opacity: 0;
        }
    }

    @-moz-keyframes fadeInOut {
        0% {
            opacity: 0;
        }
        10% {
            opacity: 0.5;
        }
        20% {
            opacity: 1;
        }
        80% {
            opacity: 1;
        }
        90% {
            opacity: 0.5;
        }
        100% {
            opacity: 0;
        }
    }

    @-webkit-keyframes fadeInOut {
        0% {
            opacity: 0;
        }
        10% {
            opacity: 0.5;
        }
        20% {
            opacity: 1;
        }
        80% {
            opacity: 1;
        }
        90% {
            opacity: 0.5;
        }
        100% {
            opacity: 0;
        }
    }

    .toast > p {
        margin: 0;
    }
</style>
