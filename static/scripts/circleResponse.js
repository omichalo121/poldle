const DL2 = document.querySelector('#countries');
const map = document.getElementById('map');
const cityInfo = document.getElementById('city-info');
const miejsceElement = document.getElementById('miejsce');
const ludnoscElement = document.getElementById('ludnosc');
const powierzchniaElement = document.getElementById('powierzchnia');
const rowsData = [];
let C1 = -1;

map.addEventListener('mouseover', (event) => {
    if (event.target.classList.contains('circle')) {
        const city = event.target;
        const cityId = city.getAttribute('name');
        const ludn = city.getAttribute('ludnosc');
        const powierz = city.getAttribute('powierzchnia');

        // Get the position of the hovered circle
        const circleRect = city.getBoundingClientRect();
        const circleCenterX = circleRect.left + circleRect.width / 2;
        const circleCenterY = circleRect.top + circleRect.height / 2;

        // Calculate the position of the city-info block
        const cityInfoWidth = cityInfo.offsetWidth;
        const cityInfoHeight = cityInfo.offsetHeight;
        const cityInfoLeft = (circleCenterX - cityInfoWidth / 2) + 10;
        const cityInfoTop = circleCenterY - cityInfoHeight - 10;

        // Update the position of the city-info block
        cityInfo.style.left = cityInfoLeft + 'px';
        cityInfo.style.top = cityInfoTop + 'px';

        miejsceElement.textContent = cityId;
        ludnoscElement.textContent = ludn;
        powierzchniaElement.textContent = powierz;

        cityInfo.style.display = 'block';
    }
});

map.addEventListener('mouseout', () => {
    cityInfo.style.display = 'none';
});