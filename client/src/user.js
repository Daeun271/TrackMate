import { writable, get } from 'svelte/store';
import * as api from './api.js';

export const user = writable(null);

export function isLoggedIn() {
    return get(user) !== null;
}

export async function signUp(userName, email, password) {
    await api.userCreate(userName, email, password);
    const data = await api.user();
    user.set(data);
}

export async function logIn(email, password) {
    await api.userLogin(email, password);
    const data = await api.user();
    user.set(data);
}
