<script>
    export let isMonthly = false;
</script>

<div>
    <input type="checkbox" id="switch" bind:checked={isMonthly} />
    <label for="switch">
        <div class="weekly">Weekly</div>
        <div class="monthly">Monthly</div>
        <div class="indicator"></div>
    </label>
</div>

<style>
    * {
        box-sizing: border-box;
        -webkit-user-select: none;
        user-select: none;
    }

    label {
        display: flex;
        position: relative;
        gap: 10px;
        border-radius: 20px;
        background-color: rgba(0, 0, 0, 0.1);
        cursor: pointer;
    }

    label div {
        padding: 10px;
        border-radius: 20px;
        color: black;
        flex: 1;
        text-align: center;
        z-index: 2;

        transition: opacity 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    .indicator {
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        width: 50%;
        height: 100%;
        position: absolute;
        z-index: 1;
    }

    input {
        display: none;
    }

    input:checked + label .indicator {
        transform: translateX(100%);
    }

    input:checked + label .weekly,
    input:not(:checked) + label .monthly {
        opacity: 0.5;
    }
</style>
