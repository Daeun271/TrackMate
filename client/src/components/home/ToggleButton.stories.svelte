<script context="module">
    import ToggleButton from './ToggleButton.svelte';

    export const meta = {
        title: 'ToggleButton',
        component: ToggleButton,
    };
</script>

<script>
    import { Story, Template } from '@storybook/addon-svelte-csf';
</script>

<Template let:args>
    <div>
        <ToggleButton {...args} />
    </div>
</Template>

<Story name="Daily" args={{ isMonthly: false }} />
<Story name="Monthly" args={{ isMonthly: true }} />
