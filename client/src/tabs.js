import { writable } from 'svelte/store';

export const currentTab = writable(
    localStorage.getItem('currentTab') ?? 'home',
);

currentTab.subscribe((value) => {
    localStorage.setItem('currentTab', value);
});

globalThis.currentTab = currentTab;

const urlSearchParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlSearchParams.entries());
export let paramsInviteCode = params.inviteCode;

if (paramsInviteCode) {
    currentTab.set('community');
}

export function clearParamsInviteCode() {
    paramsInviteCode = null;
    history.replaceState({}, '', window.location.href.split('/?')[0]);
}
