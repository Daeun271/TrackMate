<script context="module">
    import WaterCup from './WaterCup.svelte';

    export const meta = {
        title: 'WaterCup',
        component: WaterCup,
    };
</script>

<script>
    import { Story, Template } from '@storybook/addon-svelte-csf';
</script>

<Template let:args>
    <div class="bg">
        <div>
            <WaterCup {...args} />
        </div>
    </div>
</Template>

<Story name="Half" args={{ level: 0.5 }} />
<Story name="Empty" args={{ level: 0 }} />
<Story name="Full" args={{ level: 1.0 }} />

<style>
    .bg {
        background-color: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 75px;
    }
</style>
