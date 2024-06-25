import { EventEmitter } from './EventEmitter.js';
export const unauthorizedEvent = new EventEmitter();

let hostUrl = 'http://192.168.10.29:8000/';

export async function request(
    method = 'GET',
    endpoint,
    body = null,
    queryParameters = null,
) {
    let url = hostUrl + endpoint;

    if (queryParameters) {
        url += '?' + new URLSearchParams(queryParameters);
    }

    let headers = {
        'Content-Type': 'application/json',
        Authorization: localStorage.getItem('sessionKey'),
    };

    let options = {
        method: method,
        headers: headers,
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    let response = await fetch(url, options);
    if (response.status === 401) {
        unauthorizedEvent.emit();
    }

    let data = await response.json();
    if (!response.ok) {
        throw new Error(data.detail);
    }
    return data;
}

export async function user() {
    return request('GET', 'user');
}

export async function userSignup(userName, email, password) {
    return await request('POST', 'user/register', {
        user_name: userName,
        email,
        password,
    });
}

export async function userLogin(email, password) {
    return await request('POST', 'user/login', {
        email,
        password,
    });
}

export async function userLogoutFromCurrentDevice() {
    request('GET', 'user/logout_current_device');
}

export async function userLogoutFromAllDevices() {
    request('GET', 'user/logout_all_devices');
}

export async function addWaterIntake(volume, createdAt) {
    request('POST', 'user/water_intakes', {
        volume,
        created_at: createdAt,
    });
}

export async function getWaterIntakesTotal(date) {
    return request('POST', 'user/water_intakes_total', {
        date,
    });
}
