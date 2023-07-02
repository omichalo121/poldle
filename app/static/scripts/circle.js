function circleNormalScriptFunction(name) {
    const cityInput = document.querySelector('#city');
    const datalist = document.querySelector('#countries');
    const svgMap = document.querySelector('.MapImage svg');

    let xCoord, yCoord, DR, DS, S, P;

        const Circles = svgMap.querySelectorAll('.circle');
        if (Circles) {
            Circles.forEach(circle => {
                circle.setAttribute('fill', '#ff781f');
            });
        };

        const option = Array.from(datalist.options).find((option) => option.getAttribute('miasto') === name);
        if (option) {
            xCoord = parseFloat(option.getAttribute('szerokosc'));
            xCoord = (xCoord - 14.20255) * 50.31984;
            yCoord = parseFloat(option.getAttribute('dlugosc'));
            yCoord = (yCoord - 54.79012) * 81.54518;
            if (yCoord < 0) {
                yCoord = -yCoord;
            }
            yCoord += 35;

            const cityCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            cityCircle.setAttribute("cx", xCoord);
            cityCircle.setAttribute("cy", yCoord);
            cityCircle.setAttribute("r", 5);
            cityCircle.setAttribute("fill", "#f40606");
            cityCircle.setAttribute("name", option.getAttribute('value'));
            cityCircle.setAttribute("class", "circle");
            cityCircle.setAttribute("powierzchnia", option.getAttribute('powierzchnia'));
            cityCircle.setAttribute("ludnosc", option.getAttribute('ludnosc'));

            svgMap.appendChild(cityCircle);
        }
    return;
};


function circleWinScriptFunction(name) {
    let xCoord, yCoord, DR, DS, S, P;
    const cityInput = document.querySelector('#city');
    const DL4 = document.querySelector('#countries');
    const svgMap = document.querySelector('.MapImage svg');

    const Circles = svgMap.querySelectorAll('.circle');
    if (Circles) {
        Circles.forEach(circle => {
            circle.setAttribute('fill', '#ff781f');
        });
    };

    const option = Array.from(DL4.options).find((option) => option.getAttribute('miasto') === name);
    if (option) {
        xCoord = parseFloat(option.getAttribute('szerokosc'));
        xCoord = (xCoord - 14.20255) * 51.31984;
        yCoord = parseFloat(option.getAttribute('dlugosc'));
        yCoord = (yCoord - 54.79012) * 84.64518;
        if (yCoord < 0) {
            yCoord = -yCoord;
        }
        yCoord += 35;

        const cityCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        cityCircle.setAttribute("cx", xCoord);
        cityCircle.setAttribute("cy", yCoord);
        cityCircle.setAttribute("r", 5);
        cityCircle.setAttribute("fill", "#d000e5");
        cityCircle.setAttribute("name", option.getAttribute('value'));
        cityCircle.setAttribute("class", "circle");
        cityCircle.setAttribute("powierzchnia", option.getAttribute('powierzchnia'));
        cityCircle.setAttribute("ludnosc", option.getAttribute('ludnosc'));

        svgMap.appendChild(cityCircle);
    }
    return;
};
