let hostUrl = 'http://127.0.0.1:8000/';

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
    };
    let options = {
        method: method,
        headers: headers,
    };
    if (body) {
        options.body = JSON.stringify(body);
    }
    let response = await fetch(url, options);
    let data = await response.json();
    return data;
}

export async function user(userId) {
    return request('GET', 'user/' + userId);
}

export async function userCreate(userName, email, password) {
    return request('POST', 'user/create', {
        user_name: userName,
        email,
        password,
    });
}

export async function waterIntakeCreate(volume, createdAt, userId) {
    return request('POST', 'user/water_intakes', {
        volume,
        created_at: createdAt,
        user_id: userId,
    });
}

export async function waterIntakeTotal(userId, date) {
    return request('POST', 'user/water_intakes_total', {
        user_id: userId,
        date,
    });
}
