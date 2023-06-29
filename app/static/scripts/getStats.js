function stats(difficulty) {
    fetch('/getStats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(difficulty)
    })
    .then(response => response.json())
    .then(data => {
        const countBlock = document.getElementById('count');
        countBlock.textContent = data.tries;

        const avrgBlock = document.getElementById('avrg');
        avrgBlock.textContent = data.average;

        const miastoBlock = document.getElementById('miasto');
        miastoBlock.textContent = data.miasto;

        const winners = data.winners;

        const first = document.getElementById('1');
        first.textContent = winners[0];
        if (winners.length > 0 && winners[0] !== undefined) {
            first.style.marginLeft = '0.5em';
        }
        else {
            first.style.marginLeft = '0';
        }
        const second = document.getElementById('2');
        second.textContent = winners[1];
        if (winners.length > 0 && winners[1] !== undefined) {
            second.style.marginLeft = '0.5em';
        }
        else {
            second.style.marginLeft = '0';
        }
        const third = document.getElementById('3');
        third.textContent = winners[2];
        if (winners.length > 0 && winners[2] !== undefined) {
            console.log(winners[2])
            third.style.marginLeft = '0.5em';
        }
        else {
            third.style.marginLeft = '0';
        }
        const fourth = document.getElementById('4');
        fourth.textContent = winners[3];
        if (winners.length > 0 && winners[3] !== undefined) {
            fourth.style.marginLeft = '0.5em';
        }
        else {
            fourth.style.marginLeft = '0';
        }
        const fifth = document.getElementById('5');
        fifth.textContent = winners[4];
        if (winners.length > 0 && winners[4] !== undefined) {
            fifth.style.marginLeft = '0.5em';
        }
        else {
            fifth.style.marginLeft = '0';
        }
    })
    .catch(err => {
        console.log(err);
    });
}

stats('extreme');

function getUserStats(difficulty) {

    fetch('/getToken')
    .then(res => {
        res.json().then(response => {
            if(response.logged === 1){
                fetch('/userStats', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(difficulty)
                })
                .then(response => response.json())
                .then(dataMain => {
                    const userStatsBlock = document.getElementById('userStatsBlock');
                    const difficultyBlock = document.getElementById('difficultyBlock');
                    const hehe = document.getElementById('hehe');
                    hehe.style.display = 'none';

                    if (difficulty === 'user') {
                        userStatsBlock.style.display = 'block';
                        difficultyBlock.style.display = 'none';

                        const totalE = document.getElementById('totalE');
                        const totalM = document.getElementById('totalM');
                        const totalH = document.getElementById('totalH');
                        const totalEX = document.getElementById('totalEX');

                        totalE.textContent = dataMain.easy[0];
                        totalM.textContent = dataMain.medium[0];
                        totalH.textContent = dataMain.hard[0];
                        totalEX.textContent = dataMain.extreme[0];

                        const osE = document.getElementById('osE');
                        const osM = document.getElementById('osM');
                        const osH = document.getElementById('osH');
                        const osEX = document.getElementById('osEX');

                        osE.textContent = dataMain.easy[1];
                        osM.textContent = dataMain.medium[1];
                        osH.textContent = dataMain.hard[1];
                        osEX.textContent = dataMain.extreme[1];

                        const osE_per = document.getElementById('osE_per');
                        const osM_per = document.getElementById('osM_per');
                        const osH_per = document.getElementById('osH_per');
                        const osEX_per = document.getElementById('osEX_per');

                        osE_per.textContent = dataMain.easy[2];
                        osM_per.textContent = dataMain.medium[2];
                        osH_per.textContent = dataMain.hard[2];
                        osEX_per.textContent = dataMain.extreme[2];

                        const userFavCity2 = document.getElementById('userFavCity2');

                        userFavCity2.textContent = dataMain.city;
                    }
                    else {
                        userStatsBlock.style.display = 'none';
                        difficultyBlock.style.display = 'block';

                        const userWSN = document.getElementById('userWSN');
                        const userWSB = document.getElementById('userWSB');
                        const userTries = document.getElementById('userTries');
                        const userAVGTries = document.getElementById('userAVGTries');
                        const userFavCityDiff = document.getElementById('userFavCityDiff');

                        userWSN.textContent = dataMain.wsNow;
                        userWSB.textContent = dataMain.wsBest;
                        userTries.textContent = dataMain.todayT;
                        userAVGTries.textContent = dataMain.avgT;
                        userFavCityDiff.textContent = dataMain.city;
                        let fillV, colorV;

                        if (dataMain.turnOff === 1) {
                          colorV = 'transparent';
                          fillV = 'start';
                        } else {
                          colorV = '#4c8d53';
                          fillV = false;
                        }

                        const data = {
                          labels: dataMain.labels,
                          datasets: [{
                            label: 'Liczba prób na grę',
                            data: dataMain.values,
                            borderColor: colorV,
                            fill: fillV,
                            tension: 0.4
                          }]
                        };

                        const config = {
                          type: 'line',
                          data: data,
                          options: {
                            responsive: true,
                            plugins: {
                              legend: {
                                display: false
                              },
                              title: {
                                display: false,
                                text: 'Twoje dzienne próby na obecny miesiąc'
                              },
                              tooltip: {
                                callbacks: {
                                  label: function (context) {
                                    const label = context.dataset.label;
                                    const value = context.parsed.y;
                                    return `${label}: ${value}`;
                                  }
                                }
                              }
                            },
                            interaction: {
                              intersect: false
                            },
                            scales: {
                              x: {
                                display: true,
                                title: {
                                  display: true
                                }
                              },
                              y: {
                                display: true,
                                title: {
                                  display: true,
                                  text: 'Ilość prób'
                                },
                                suggestedMin: 0,
                                suggestedMax: 20
                              }
                            }
                          }
                        };

                        var chart = document.getElementById('userChart');
                        let chartStatus = Chart.getChart("userChart");

                        if (chartStatus != undefined) {
                            chartStatus.destroy();
                            const ctx = chart.getContext('2d');
                            userChart = new Chart(ctx, config);
                        }
                        else {
                            const ctx = chart.getContext('2d');
                            userChart = new Chart(ctx, config);
                        }
                    }
                })
            }
        })
    })
    .catch(err => {
        console.log(err)
    });

}

getUserStats('user');