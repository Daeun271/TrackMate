import { writable, get } from 'svelte/store';
import * as api from './api.js';

export const user = writable(JSON.parse(localStorage.getItem('user')) ?? null);

user.subscribe((value) => {
    localStorage.setItem('user', JSON.stringify(value));
});

export async function signUp(userName, email, password) {
    validateFields([userName, email, password]);
    validateEmail(email);
    validatePassword(password);

    await api.userSignup(userName, email, password);
    const data = await api.user();
    user.set(data);
}

export async function logIn(email, password) {
    validateFields([email, password]);
    validateEmail(email);

    await api.userLogin(email, password);
    const data = await api.user();
    user.set(data);
}

function validateFields(fields) {
    for (const field of fields) {
        if (field.trim() === '') {
            throw new Error('Please fill in all fields');
        }
    }
}

function validateEmail(email) {
    const emailRegex =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!email.match(emailRegex)) {
        throw new Error('Please enter a valid email address');
    }
}

function validatePassword(password) {
    if (password.length < 8) {
        throw new Error('Password must be at least 8 characters long');
    } else if (!password.match(/[0-9]/)) {
        throw new Error('Password must contain at least one number');
    } else if (!password.match(/[a-zA-Z]/)) {
        throw new Error('Password must contain at least one letter');
    }
}
