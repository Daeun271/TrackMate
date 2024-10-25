export function buttonClick(node) {
    let timeout = null;

    const handleClick = () => {
        if (timeout) {
            clearTimeout(timeout);
        }

        node.classList.add('clicked');

        timeout = setTimeout(() => {
            node.classList.remove('clicked');
        }, 150);
    };

    node.addEventListener('click', handleClick);

    return {
        destroy() {
            node.removeEventListener('click', handleClick);
        },
    };
}
