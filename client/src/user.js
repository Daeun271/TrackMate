import { writable, get } from 'svelte/store';
import * as api from './api.js';

export const user = writable(null);

export function isLoggedIn() {
    return get(user) !== null;
}

export async function signUp(userName, email, password) {
    const data = await api.userCreate(userName, email, password);
    user.set(data);
}

export async function addWaterIntake(volume, createdAt, userId) {
    await api.waterIntakeCreate(volume, createdAt, userId);
}

export async function getWaterIntakesTotal(userId, date) {
    return await api.waterIntakeTotal(userId, date);
}

/*
export async function addWaterIntake(volume, created_at) {
    await api.waterIntakeCreate(volume, created_at, get(user).user_id);
}

export async function getWaterIntakesTotal(date) {
    return await api.waterIntakeTotal(get(user).user_id, date);
}
*/
