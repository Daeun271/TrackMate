<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';
    import ToggleButton from '../home/ToggleButton.svelte';
    import { getStatsForCharts } from '../../myCharts.js';

    let isMonthly = false;

    let elCategory = null;
    let elWaterintake = null;
    let elCalories = null;

    let chartCategory = null;
    let chartWaterintake = null;
    let chartCalories = null;

    let statsData = null;

    let isCategoryChartHidden = false;

    onMount(() => {
        chartCategory = new Chart(elCategory, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [],
            },
        });

        chartWaterintake = new Chart(elWaterintake, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [],
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        });

        chartCalories = new Chart(elCalories, {
            type: 'line',
            data: {
                labels: [],
                datasets: [],
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        });

        getStatsForCharts().then((data) => {
            statsData = data;
        });
    });

    function updateCharts() {
        if (
            chartCategory === null ||
            chartWaterintake === null ||
            chartCalories === null ||
            statsData === null
        ) {
            return;
        }

        isCategoryChartHidden = false;

        if (isMonthly) {
            if (statsData.monthlyCategoryData.labels.length === 0) {
                isCategoryChartHidden = true;
            }

            chartCategory.data = statsData.monthlyCategoryData;
            chartWaterintake.data = statsData.monthlyWaterintakeData;
            chartCalories.data = statsData.monthlyCaloriesData;
        } else {
            if (statsData.weeklyCategoryData.labels.length === 0) {
                isCategoryChartHidden = true;
            }

            chartCategory.data = statsData.weeklyCategoryData;
            chartWaterintake.data = statsData.weeklyWaterintakeData;
            chartCalories.data = statsData.weeklyCaloriesData;
        }

        chartCategory.update();
        chartWaterintake.update();
        chartCalories.update();
    }

    $: {
        isMonthly;
        chartCategory;
        chartWaterintake;
        chartCalories;
        statsData;

        updateCharts();
    }
</script>

<div class="bg">
    <div class="switch">
        <ToggleButton bind:isMonthly></ToggleButton>
    </div>

    <div class="charts-scroll">
        <div class="charts-container">
            <canvas bind:this={elWaterintake}></canvas>
            <canvas bind:this={elCalories}></canvas>
            <canvas bind:this={elCategory} class:hidden={isCategoryChartHidden}
            ></canvas>
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
        padding: 10px;
    }

    .hidden {
        display: none !important;
    }
</style>
