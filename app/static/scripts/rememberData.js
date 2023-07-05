function rememberDataScriptFunction(difficulty) {
    const WON = document.getElementById('SB');
    const INP = document.getElementById('city');
    var key = 'responses_' + difficulty;

    fetch('/checkWon', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(difficulty)
    })
    .then(res => {
        res.json().then(response => {
            let CTXD = 0, countCheck, info;

            if (response.clear === 1) {
                console.log(storedResponses);
                localStorage.removeItem(key);
                storedResponses = []
                return;
            }

            if (response.user === 1) {
                countCheck = response.count;
            } else {
                countCheck = storedResponses.length;
            }

            if (response.won === 1 && response.clear === 0) {
                WON.disabled = true;
                INP.disabled = true;
                for (let i = 0; i < countCheck; i++) {
                    if (response.user === 1) {
                        info = response.tablica[i];
                    } else {
                        info = storedResponses[i];
                    }

                    if (info[0] === 'true') {
                        circleWinScriptFunction(info[1]);
                    } else {
                        circleNormalScriptFunction(info[1]);
                    }
                    tableScriptFunction(info);
                    CTXD = tableClearScriptFunction(CTXD);
                }
            } else if (response.clear === 0) {
                INP.disabled = false;
                for (let i = 0; i < countCheck; i++) {
                    if (response.user === 1) {
                        info = response.tablica[i];
                    } else {
                        info = storedResponses[i];
                    }
                    circleNormalScriptFunction(info[1]);
                    tableScriptFunction(info);
                    CTXD = tableClearScriptFunction(CTXD);
                }
            }
        });
    });
}