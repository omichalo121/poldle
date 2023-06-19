const cityRemove = document.querySelector('#city');
const DLR = document.querySelector('#countries');

cityRemove.addEventListener('change', (event) => {
    const cityToRemove = event.target.value;
    optionRM = Array.from(DLR.options).find((option) => option.value === cityToRemove);
    if (optionRM) {
        DLR.removeChild(optionRM);
    }
});