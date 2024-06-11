const config = {
    stories: ['../src/**/*.stories.*'],
    addons: ['@storybook/addon-svelte-csf'],
    framework: {
        name: '@storybook/svelte-vite',
        options: {},
    },
    docs: {
        autodocs: 'tags',
    },
    core: {
        disableTelemetry: true,
    },
};
export default config;
