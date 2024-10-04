<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';
    import * as Utils from '../../chartUtils.js';
    import ToggleButton from '../home/ToggleButton.svelte';

    let dailyCategory = null;
    let dailyWater = null;
    let dailyCalories = null;
    let monthlyCategory = null;
    let monthlyWater = null;
    let monthlyCalories = null;

    const labels = Utils.months({ count: 7 });
    const data = {
        labels: labels,
        datasets: [
            {
                label: 'My First Dataset',
                data: [65, 59, 80, 81, 56, 55, 40],
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
            },
        ],
    };

    onMount(() => {
        new Chart(dailyCategory, {
            type: 'line',
            data: data,
        });

        new Chart(dailyWater, {
            type: 'line',
            data: data,
        });

        new Chart(dailyCalories, {
            type: 'line',
            data: data,
        });

        new Chart(monthlyCategory, {
            type: 'line',
            data: data,
        });

        new Chart(monthlyWater, {
            type: 'line',
            data: data,
        });

        new Chart(monthlyCalories, {
            type: 'line',
            data: data,
        });
    });
</script>

<div class="bg">
    <div class="switch">
        <ToggleButton />
    </div>

    <div class="charts-scroll">
        <div class="charts-container">
            <canvas bind:this={dailyCategory}></canvas>
            <canvas bind:this={dailyWater}></canvas>
            <canvas bind:this={dailyCalories}></canvas>
            <canvas bind:this={monthlyCategory}></canvas>
            <canvas bind:this={monthlyWater}></canvas>
            <canvas bind:this={monthlyCalories}></canvas>
        </div>
    </div>
</div>

<style>
    .bg {
        display: flex;
        flex-direction: column;
        max-height: 100%;
        max-width: 760px;
        margin: 0 auto;
    }

    .switch {
        padding: 15px;
        flex: 0 0 auto;
    }

    .charts-scroll {
        flex: 1 1 auto;
        overflow: auto;
    }

    .charts-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        padding: 20px;
    }

    canvas {
        background-color: #f0f0f0;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
</style>
