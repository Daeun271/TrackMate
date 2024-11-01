import {
    updateUserEmail,
    validateUserPassword,
    updateUserPassword,
} from '../../api';

export async function updateEmail(newEmail) {
    try {
        const res = await updateUserEmail(newEmail);
        return res.email;
    } catch (e) {
        if (e.detail === 'empty email') {
            throw new Error('Please enter an email address');
        } else if (e.detail === 'invalid email') {
            throw new Error('Please enter a valid email address');
        } else if (e.detail === 'email already in use') {
            throw new Error('This email address is invalid');
        }
    }
}

export async function validatePassword(password) {
    try {
        const res = await validateUserPassword(password);
        return res;
    } catch (e) {
        if (
            e.detail === 'Password must be at least 8 characters' ||
            e.detail === 'Password must have at least one numeral' ||
            e.detail === 'Password must have at least one letter'
        ) {
            throw new Error('invalid password');
        } else if (e.detail === 'wrong password') {
            throw new Error('wrong password');
        }
    }
}

export async function updatePassword(newPassword) {
    try {
        await updateUserPassword(newPassword);
    } catch (e) {
        if (
            e.detail === 'Password must be at least 8 characters' ||
            e.detail === 'Password must have at least one numeral' ||
            e.detail === 'Password must have at least one letter'
        ) {
            throw new Error('invalid password');
        } else if (e.detail === 'same password') {
            throw new Error('same password');
        }
    }
}
