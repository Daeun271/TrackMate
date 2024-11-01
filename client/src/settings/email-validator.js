import { updateUserEmail } from '../api';

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
