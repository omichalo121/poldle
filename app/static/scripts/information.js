const openInfo = document.getElementById('info');
const infoBlock = document.getElementById('information');
const exit = document.getElementById('EXIT');

openInfo.addEventListener('click', (event) => {
    infoBlock.style.display = 'flex';
})

exit.addEventListener('click', (event) => {
    infoBlock.style.display = 'none';
})