import { EventEmitter } from './event-emitter.js';
export const unauthorizedEvent = new EventEmitter();

let hostUrl = 'http://192.168.10.29:8000/';

export async function request(
    method = 'GET',
    endpoint,
    body = null,
    queryParameters = null,
    isFormData = false,
) {
    let url = hostUrl + endpoint;

    if (queryParameters) {
        url += '?' + new URLSearchParams(queryParameters);
    }

    let headers = {
        Authorization: localStorage.getItem('sessionKey'),
    };

    let options = {
        method: method,
        headers: headers,
    };

    if (body) {
        if (isFormData) {
            options.body = body;
        } else {
            headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(body);
        }
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
    await request('GET', 'user/logout_current_device');
}

export async function userLogoutFromAllDevices() {
    await request('GET', 'user/logout_all_devices');
}

export async function addWaterIntake(volume, createdAt) {
    await request('POST', 'user/water_intakes/create', {
        volume,
        created_at: createdAt,
    });
}

export async function getWaterIntakesTotal(dateTime) {
    return await request('POST', 'user/water_intakes/get_total_volume', {
        date_time: dateTime,
    });
}

export async function addFoodIntake(name, calories, consumedAt, timeCategory) {
    return await request('POST', 'user/food_intakes/create', {
        name,
        calories,
        consumed_at: consumedAt,
        time_category: timeCategory,
    });
}

export async function getFoodIntakesTotal(startDate, endDate) {
    return await request('POST', 'user/food_intakes/get_food_intakes', {
        start_date: startDate,
        end_date: endDate,
    });
}

export async function updateFoodIntake(
    uid,
    name,
    calories,
    consumedAt,
    timeCategory,
) {
    return await request('POST', 'user/food_intakes/update', {
        uid,
        name,
        calories,
        consumed_at: consumedAt,
        time_category: timeCategory,
    });
}

export async function deleteFoodIntake(uid) {
    await request('Delete', 'user/food_intakes/delete', {
        uid,
    });
}

export async function uploadFoodImage(uid, imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile);

    await request(
        'POST',
        'user/food_intakes/images/' + uid,
        formData,
        null,
        true,
    );
}

export function getFoodImageUrl(uid) {
    return (
        hostUrl +
        'user/food_intakes/images/' +
        uid +
        '?auth=' +
        localStorage.getItem('sessionKey')
    );
}

export async function addExercise(
    exerciseId,
    category,
    date,
    duration,
    burnedCalories,
) {
    return await request('POST', 'user/exercises/create', {
        exercise_id: exerciseId,
        category,
        date,
        duration,
        burned_calories: burnedCalories,
    });
}

export async function getExercisesTotal(startDate, endDate) {
    return await request('POST', 'user/exercises/get_exercises', {
        start_date: startDate,
        end_date: endDate,
    });
}

export async function updateExercise(
    uid,
    exerciseId,
    category,
    date,
    duration,
    burnedCalories,
) {
    return await request('POST', 'user/exercises/update', {
        uid,
        exercise_id: exerciseId,
        category,
        date,
        duration,
        burned_calories: burnedCalories,
    });
}

export async function deleteExercise(uid) {
    await request('Delete', 'user/exercises/delete', {
        uid,
    });
}

export async function uploadUserWeight(weight) {
    await request('POST', 'user/weight/upload', {
        weight,
    });
}

export async function getUserWeight() {
    return await request('GET', 'user/weight/get');
}
