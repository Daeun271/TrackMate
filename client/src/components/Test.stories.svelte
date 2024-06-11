<script context="module">
    import Test from './Test.svelte';

    export const meta = {
        title: 'Test',
        component: Test,
    };
</script>

<script>
    import { Story, Template } from '@storybook/addon-svelte-csf';
</script>


<Template let:args>
    <Test {...args} />
</Template>


<Story name="Default" />
<Story name="Custom" args={{ text: 'Custom Text' }} />
