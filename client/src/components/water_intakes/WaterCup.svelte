<script>
    export let level = 0;

    /* empty: -24%- full: 71% */
    $: levelPercent = level * (71 + 24) - 24;
</script>

<div class="cup-wrap">
    <div class="cup" style="--water-level: {levelPercent}%">
        <div class="waterWave">
            <svg viewBox="0 0 500 500" preserveAspectRatio="none">
                <path
                    d="M0,100 C150,200 350,0 500,100 L500,500 L0,500 Z"
                    style="stroke: none; fill: #74ccf4;"
                >
                    <animate
                        attributeName="d"
                        dur="1.5s"
                        repeatCount="indefinite"
                        keyTimes="0;0.5;1"
                        values="M0,100 C150,200 350,0 500,100 L500,500 L0,500 Z;M0,100 C150,0 350,200 500,100 L500,500 L0,500 Z;M0,100 C150,200 350,0 500,100 L500,500 L0,500 Z"
                    >
                    </animate></path
                >
            </svg>
        </div>
        <div class="waterBody"></div>
    </div>
</div>

<style>
    .cup-wrap {
        filter: drop-shadow(0 0 1px #3338);
        height: 40dvh;
        aspect-ratio: 1/1.3;
    }

    .cup {
        position: relative;
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, #fff 0%, #eee 90%, #ddd 100%);
        border-radius: 5px;
        clip-path: polygon(0 0, 100% 0%, 80% 100%, 20% 100%);
        overflow: hidden;
    }

    .waterWave {
        position: absolute;
        left: 0;
        bottom: var(--water-level);
        width: 100%;
        height: 40%;
        transition: bottom 0.3s ease;
    }

    .waterBody {
        position: absolute;
        left: 0;
        top: calc(100% - var(--water-level));
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, #74ccf4, #00adf1);
    }

    @keyframes wave {
        0% {
            d: path('M0,100 C150,200 350,0 500,100 L500,500 L0,500 Z');
        }
        50% {
            d: path('M0,100 C150,0 350,200 500,100 L500,500 L0,500 Z');
        }
        100% {
            d: path('M0,100 C150,200 350,0 500,100 L500,500 L0,500 Z');
        }
    }

    path {
        animation: wave 2s infinite;
    }
</style>
