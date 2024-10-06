import * as Utils from './chartUtils.js';
import { getStats } from './api.js';

const weeklyLabels = Utils.weekdays({ count: 7 });
const monthlyLabels = Utils.months({ count: 6, section: 3 });

function stringToHslColor(str, s = 50, l = 50) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }

    let h = hash % 360;
    return `hsl(${h}, ${s}%, ${l}%)`;
}

export async function getStatsForCharts() {
    const stats = await getStats();

    const weeklyCategoryData = {
        labels: Object.keys(stats.weekly.category),
        datasets: [
            {
                label: 'Workout Category',
                data: Object.values(stats.weekly.category),
                backgroundColor: Object.keys(stats.weekly.category).map((key) =>
                    stringToHslColor(key),
                ),
                hoverOffset: 4,
            },
        ],
    };

    const weeklyWaterintakeData = {
        labels: weeklyLabels,
        datasets: [
            {
                label: 'Water Intake',
                data: stats.weekly.water_intake,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235)',
                borderWidth: 1,
            },
        ],
    };

    const weeklyCaloriesData = {
        labels: weeklyLabels,
        datasets: [
            {
                label: 'Consumed Calories',
                data: stats.weekly.calories[1],
                fill: false,
                borderColor: 'rgba(192,75,192,1)',
                lineTenstion: 0.1,
            },
            {
                label: 'Burned Calories',
                data: stats.weekly.calories[0],
                fill: false,
                borderColor: 'rgba(75,192,192,1)',
                lineTension: 0.1,
            },
        ],
    };

    const monthlyCategoryData = {
        labels: Object.keys(stats.monthly.category),
        datasets: [
            {
                label: 'Workout Category',
                data: Object.values(stats.monthly.category),
                backgroundColor: Object.keys(stats.monthly.category).map(
                    (key) => stringToHslColor(key),
                ),
                hoverOffset: 4,
            },
        ],
    };

    const monthlyWaterintakeData = {
        labels: monthlyLabels,
        datasets: [
            {
                label: 'Water Intake',
                data: stats.monthly.water_intake,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235)',
                borderWidth: 1,
            },
        ],
    };

    const monthlyCaloriesData = {
        labels: monthlyLabels,
        datasets: [
            {
                label: 'Consumed Calories',
                data: stats.monthly.calories[1],
                fill: false,
                borderColor: 'rgba(192,75,192,1)',
                lineTension: 0.1,
            },
            {
                label: 'Burned Calories',
                data: stats.monthly.calories[0],
                fill: false,
                borderColor: 'rgba(75,192,192,1)',
                lineTension: 0.1,
            },
        ],
    };

    return {
        weeklyCategoryData,
        weeklyWaterintakeData,
        weeklyCaloriesData,
        monthlyCategoryData,
        monthlyWaterintakeData,
        monthlyCaloriesData,
    };
}
