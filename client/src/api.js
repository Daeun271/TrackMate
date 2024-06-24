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
    let data = await response.json();
    return data;
}

export async function user() {
    return request('GET', 'user');
}

export async function userCreate(userName, email, password) {
    const sessionKey = await request('POST', 'user/register', {
        user_name: userName,
        email,
        password,
    });

    localStorage.setItem('sessionKey', sessionKey.key);
}

export async function userLogin(email, password) {
    const sessionKey = await request('POST', 'user/login', {
        email,
        password,
    });

    localStorage.setItem('sessionKey', sessionKey.key);
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
