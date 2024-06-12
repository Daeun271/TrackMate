import { writable } from 'svelte/store';

export const currentTab = writable(
    localStorage.getItem('currentTab') ?? 'home',
);

currentTab.subscribe((value) => {
    localStorage.setItem('currentTab', value);
});

globalThis.currentTab = currentTab;
