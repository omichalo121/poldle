let C = 0;

function tableScriptFunction(info) {

    C++;
    const table = document.getElementById('TBL');
    const newRow =document.createElement('tr');
    const DL3 = document.querySelector('#countries');
    let DR, DS, P, S, sign, A1, A2, arrP, arrL, P2, S2;
    let countCell, cityCell, wayCell, disCell, popCell, surCell;

    countCell = document.createElement('td');
    countCell.classList.add('row-text-try');
    countCell.innerHTML = C;
    newRow.appendChild(countCell);

    DR = info[2], DS = Math.round(info[3]), P = info[4], S = info[5], arrS = info[6], arrP = info[7], S2 = info[8], P2 = info[9];
    const optionName = Array.from(DL3.options).find(option => option.getAttribute('miasto') === info[1]);
    miejsce = optionName.getAttribute('value');

    cityCell = document.createElement('td');
    cityCell.classList.add('row-items');
    cityCell.innerHTML = miejsce;
    newRow.appendChild(cityCell)

    if (info[0] === false) {
        wayCell = document.createElement('td');
        wayCell.classList.add('row-items');
        wayCell.innerHTML = `<img src="static/icons/table-rows/${DR}.png" class="icon">`;
        newRow.appendChild(wayCell);

        disCell = document.createElement('td');
        disCell.classList.add('row-items');
        disCell.innerHTML = DS + ' km';
        newRow.appendChild(disCell);

        sign = Math.sign(P)

        popCell = document.createElement('td');
        popCell.classList.add('row-items');

        if (arrP >= 1.5 || arrP <= 0.5) {
            A1 = 'MUCH_';
        } else {
            A1 = '';
        };

        if (sign < 0) {
            if (0.95 <= arrP && arrP <= 1.05) {
                P = Math.abs(P);
                popCell.innerHTML = `<img src="static/icons/table-rows/DONE.png" class="icon"></img><div></div><span>${P2}</span>`;
            }
            else {
                P = Math.abs(P);
                popCell.innerHTML = `<img src="static/icons/table-rows/${A1}MORE.png" class="icon"></img><div></div><span>${P2}</span>`;
            }
        }
        else if (sign > 0) {
            if (0.95 <= arrP && arrP <= 1.05) {
                popCell.innerHTML = `<img src="static/icons/table-rows/DONE.png" class="icon"></img><div></div><span>${P2}</span>`;
            }
            else {
                popCell.innerHTML = `<img src="static/icons/table-rows/${A1}LESS.png" class="icon"></img><div></div><span>${P2}</span>`;
            }
        }
        else {
            popCell.innerHTML = '<img src="static/icons/table-rows/DONE.png" class="icon"></img>';
        };
        newRow.appendChild(popCell);



        sign = Math.sign(S);
        surCell = document.createElement('td');
        surCell.classList.add('row-items');

        if (arrS >= 1.5 || arrS <= 0.5) {
            A2 = 'MUCH_';
        } else {
            A2 = '';
        };

        if (sign < 0) {
            if (0.95 <= arrS && arrS <= 1.05) {
                P = Math.abs(S);
                surCell.innerHTML = `<img src="static/icons/table-rows/DONE.png" class="icon"></img><div></div><span>${S2} km²</span>`;
            }
            else {
                P = Math.abs(S);
                surCell.innerHTML = `<img src="static/icons/table-rows/${A2}MORE.png" class="icon"></img><div></div><span>${S2} km²</span>`;
            }
        }
        else if (sign > 0) {
            if (0.95 <= arrS && arrS <= 1.05) {
                surCell.innerHTML = `<img src="static/icons/table-rows/DONE.png" class="icon"></img><div></div><span>${S2} km²</span>`;
            }
            else {
                surCell.innerHTML = `<img src="static/icons/table-rows/${A2}LESS.png" class="icon"></img><div></div><span>${S2} km²</span>`;
            }
        }
        else {
            surCell.innerHTML = '<img src="static/icons/table-rows/DONE.png" class="icon"></img>';
        };
        newRow.appendChild(surCell);


        newRow.classList.add('row');
        table.appendChild(newRow);

        DL3.removeChild(optionName);
        return;
    }
    else if(info[0] === true) {
        wayCell = document.createElement('td');
        wayCell.classList.add('row-items');
        wayCell.innerHTML = '<img src="static/icons/table-rows/DONE.png" class="icon">';
        newRow.appendChild(wayCell);

        disCell = document.createElement('td');
        disCell.classList.add('row-items');
        disCell.innerHTML = '<img src="static/icons/table-rows/DONE.png" class="icon">';
        newRow.appendChild(disCell);

        popCell = document.createElement('td');
        popCell.classList.add('row-items');
        popCell.innerHTML = '<img src="static/icons/table-rows/DONE.png" class="icon"></img>';
        newRow.appendChild(popCell);

        surCell = document.createElement('td');
        surCell.classList.add('row-items');
        surCell.innerHTML = '<img src="static/icons/table-rows/DONE.png" class="icon"></img>';
        newRow.appendChild(surCell);

        newRow.classList.add('row')
        table.appendChild(newRow);

        DL3.removeChild(optionName);
        return;
    }
};