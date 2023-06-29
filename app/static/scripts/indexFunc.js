const dataBlock = document.getElementById('data');
const statsBlock = document.getElementById('statsUser');
function showInfo() {
    fetch('/getToken')
    .then(res => {
        res.json().then(response => {
            if(response.logged === 1){
                if (statsBlock.style.display === 'none') {
                statsBlock.style.display = 'flex';
                statsBlock.style.width = '600px';
                statsBlock.style.marginLeft = '-90px';
                }
                else {
                    statsBlock.style.display = 'none';
                }
            }
        })
    })
    .catch(err => {
        console.log(err)
    });
};

    fetch('/getToken')
    .then(res => {
        res.json().then(response => {
            if(response.logged === 1){
                dataBlock.style.display = 'flex';
            }
        })
    })
    .catch(err => {
        console.log(err)
    });