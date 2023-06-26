const login = () => {
    const unsuccessful = document.getElementById('badLogin');
    const log_login = document.getElementById('username');
    const pass_login = document.getElementById('password');

    const uLog = log_login.value.trim();
    const pLog = passLogValue;

    fetch('/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: uLog,
            password: pLog
            })
        })
        .then(resLog => {
            resLog.json().then(response => {
                if(response.access_token) {
                    location.reload();
                }
                else if(!response.access_token && LB.disabled === false) {
                    unsuccessful.textContent = 'Niepoprawny login bądź hasło';
                }
            })
        })
        .catch (err => {
            console.log(err);
        })
}