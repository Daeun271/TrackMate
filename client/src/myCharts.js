import * as Utils from './chartUtils.js';

const weeklyLabels = Utils.weekdays({ count: 7 });
const monthlyLabels = Utils.months({ count: 6, section: 3 });

export const weeklyCategoryData = {
    labels: weeklyLabels,
    datasets: [
        {
            label: 'Category 1',
            data: [65, 59, 80, 81, 56, 55, 40],
            fill: false,
            borderColor: 'rgba(75,192,192,1)',
            lineTension: 0.1,
        },
        {
            label: 'Category 2',
            data: [45, 49, 70, 71, 46, 45, 30],
            fill: false,
            borderColor: 'rgba(192,75,192,1)',
            lineTension: 0.1,
        },
    ],
};

export const weeklyWaterData = {
    labels: weeklyLabels,
    datasets: [
        {
            label: 'Water',
            data: [3, 2, 2, 1, 5, 2, 1],
            fill: false,
            borderColor: 'rgba(75,192,192,1)',
            lineTension: 0.1,
        },
    ],
};

export const weeklyCaloriesData = {
    labels: weeklyLabels,
    datasets: [
        {
            label: 'Calories',
            data: [2000, 1800, 1500, 1600, 1400, 1200, 1300],
            fill: false,
            borderColor: 'rgba(75,192,192,1)',
            lineTension: 0.1,
        },
    ],
};

export const monthlyCategoryData = {
    labels: monthlyLabels,
    datasets: [
        {
            label: 'Category 1',
            data: [65, 59, 80, 81, 56, 55],
            fill: false,
            borderColor: 'rgba(75,192,192,1)',
            lineTension: 0.1,
        },
        {
            label: 'Category 2',
            data: [45, 49, 70, 71, 46, 45],
            fill: false,
            borderColor: 'rgba(192,75,192,1)',
            lineTension: 0.1,
        },
    ],
};

export const monthlyWaterData = {
    labels: monthlyLabels,
    datasets: [
        {
            label: 'Water',
            data: [3, 2, 2, 1, 5, 2],
            fill: false,
            borderColor: 'rgba(75,192,192,1)',
            lineTension: 0.1,
        },
    ],
};

export const monthlyCaloriesData = {
    labels: monthlyLabels,
    datasets: [
        {
            label: 'Calories',
            data: [2000, 1800, 1500, 1600, 1400, 1200],
            fill: false,
            borderColor: 'rgba(75,192,192,1)',
            lineTension: 0.1,
        },
    ],
};
