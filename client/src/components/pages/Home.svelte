<script>
    import { afterUpdate, onMount } from 'svelte';
    import Chart from 'chart.js/auto';
    import * as Utils from '../../chartUtils.js';
    import ToggleButton from '../home/ToggleButton.svelte';
    import {
        weeklyCategoryData,
        weeklyWaterData,
        weeklyCaloriesData,
        monthlyCategoryData,
        monthlyWaterData,
        monthlyCaloriesData,
    } from '../../myCharts.js';

    let isMonthly = false;

    let elCategory = null;
    let elWater = null;
    let elCalories = null;

    let chartCategory = null;
    let chartWater = null;
    let chartCalories = null;

    onMount(() => {
        chartCategory = new Chart(elCategory, {
            type: 'line',
            data: {
                labels: [],
                datasets: [],
            },
        });

        chartWater = new Chart(elWater, {
            type: 'line',
            data: {
                labels: [],
                datasets: [],
            },
        });

        chartCalories = new Chart(elCalories, {
            type: 'line',
            data: {
                labels: [],
                datasets: [],
            },
        });

        /*if (isMonthly) {
            monthlyCategoryChart = new Chart(monthlyCategory, {
                type: 'line',
                data: monthlyCategoryData,
            });

            monthlyWaterChart = new Chart(monthlyWater, {
                type: 'line',
                data: monthlyWaterData,
            });

            monthlyCaloriesChart = new Chart(monthlyCalories, {
                type: 'line',
                data: monthlyCaloriesData,
            });
        } else {
            weeklyCategoryChart = new Chart(elCategory, {
                type: 'line',
                data: weeklyCategoryData,
            });

            weeklyWaterChart = new Chart(elWater, {
                type: 'line',
                data: weeklyWaterData,
            });

            weeklyCaloriesChart = new Chart(elCalories, {
                type: 'line',
                data: weeklyCaloriesData,
            });
        }*/
    });

    function updateCharts() {
        if (
            chartCategory === null ||
            chartWater === null ||
            chartCalories === null
        ) {
            return;
        }

        if (isMonthly) {
            chartCategory.data = monthlyCategoryData;
            chartWater.data = monthlyWaterData;
            chartCalories.data = monthlyCaloriesData;
        } else {
            chartCategory.data = weeklyCategoryData;
            chartWater.data = weeklyWaterData;
            chartCalories.data = weeklyCaloriesData;
        }

        chartCategory.update();
        chartWater.update();
        chartCalories.update();
    }

    $: {
        isMonthly;
        chartCategory;
        chartWater;
        chartCalories;

        updateCharts();
    }
</script>

<div class="bg">
    <div class="switch">
        <ToggleButton bind:isMonthly></ToggleButton>
    </div>

    <div class="charts-scroll">
        <div class="charts-container">
            <canvas bind:this={elCategory}></canvas>
            <canvas bind:this={elWater}></canvas>
            <canvas bind:this={elCalories}></canvas>
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
