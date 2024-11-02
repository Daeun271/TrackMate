import { EventEmitter } from './event-emitter.js';
export const unauthorizedEvent = new EventEmitter();

let hostUrl = '/';

class ApiError extends Error {
    constructor(detail) {
        super(detail);
        this.name = 'ApiError';
        this.detail = detail;
    }
}

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
        throw new ApiError(data.detail);
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
    await request('GET', 'user/logout/current_device');
}

export async function userLogoutFromAllDevices() {
    await request('GET', 'user/logout/all_devices');
}

export async function addWaterIntake(volume, createdAt) {
    await request('POST', 'user/water_intakes/create', {
        volume,
        created_at: createdAt,
    });
}

export async function getWaterIntakesTotal(dateTime) {
    return await request('POST', 'user/water_intakes/get', {
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
    return await request('POST', 'user/food_intakes/get', {
        start_date: startDate,
        end_date: endDate,
    });
}

export async function searchFoodIntakes(searchDate) {
    return await request('POST', 'user/food_intakes/search', {
        search_date: searchDate,
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
    return await request('POST', 'user/exercises/get', {
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

export async function getStats() {
    return await request('GET', 'user/stats/get');
}

export async function createGroup(name) {
    return await request('POST', 'user/groups/create', {
        name: name,
    });
}

export async function getGroups() {
    return await request('GET', 'user/groups/get');
}

export async function getMembers(groupId) {
    return await request('POST', 'user/groups/members/get', {
        id: groupId,
    });
}

export async function createPost(groupId, title, content, createdAt) {
    return await request('POST', 'user/groups/posts/create', {
        id: groupId,
        title,
        content,
        created_at: createdAt,
    });
}

export async function getPosts(groupId, startDate, endDate) {
    return await request('POST', 'user/groups/posts/get', {
        id: groupId,
        start_date: startDate,
        end_date: endDate,
    });
}

export async function searchPosts(groupId, searchDate) {
    return await request('POST', 'user/groups/posts/search', {
        id: groupId,
        search_date: searchDate,
    });
}

export async function updatePost(postId, title, content) {
    return await request('POST', 'user/groups/posts/update', {
        id: postId,
        title,
        content,
    });
}

export async function deletePost(postId) {
    await request('Delete', 'user/groups/posts/delete', {
        id: postId,
    });
}

export async function addMember(groupCode) {
    return await request('POST', 'user/groups/invite', {
        group_code: groupCode,
    });
}

export async function createComment(postId, content, createdAt) {
    return await request('POST', 'user/groups/posts/comments/create', {
        post_id: postId,
        content,
        created_at: createdAt,
    });
}

export async function getComments(postId) {
    return await request('POST', 'user/groups/posts/comments/get', {
        post_id: postId,
    });
}

export async function updateComment(commentId, content) {
    await request('POST', 'user/groups/posts/comments/update', {
        comment_id: commentId,
        content,
    });
}

export async function deleteComment(commentId) {
    await request('Delete', 'user/groups/posts/comments/delete', {
        comment_id: commentId,
    });
}

export async function getUserName() {
    return await request('GET', 'user/name/get');
}

export async function updateUserName(name) {
    return await request('POST', 'user/name/update', {
        user_name: name,
    });
}

export async function getUserEmail() {
    return await request('GET', 'user/email/get');
}

export async function updateUserEmail(email) {
    return await request('POST', 'user/email/update', {
        email,
    });
}

export async function validateUserPassword(password) {
    return await request('POST', 'user/password/validate', {
        password,
    });
}

export async function updateUserPassword(password) {
    await request('POST', 'user/password/update', {
        password,
    });
}

export async function deleteUserAccount() {
    await request('Delete', 'user/delete');
}
