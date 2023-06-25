const LB = document.getElementById('login');
const username = document.getElementById('username');
const password = document.getElementById('password');

username.addEventListener('input', loginHandler);
password.addEventListener('input', loginHandler);

// handle the good work of login - hide password and work with enter

function loginHandler() {
    if(username.value.trim() === '' || password.value.trim() === '') {
        LB.disabled = true;
    }
    else {
        LB.disabled = false;
    }
}

const handleLogEnter = (event) => {
    if(event.key === 'Enter' && LB.disabled === false) {
        LB.click();
    }
}

username.addEventListener('keydown', handleLogEnter);
password.addEventListener('keydown', handleLogEnter);

// just for better work - smooth it baby

let passLogValue;

password.addEventListener('keydown', (event) => {
    if (event.key === 'Backspace') {

        const selectionStartLog = password.selectionStart;
        const selectionEndLog = password.selectionEnd;

        if (selectionStartLog !== selectionEndLog) {
            passLogValue = passLogValue.slice(0, selectionStartLog) + passLogValue.slice(selectionEndLog);
        } else {
            passLogValue = passLogValue.slice(0, -1);
        }
    }
});

password.addEventListener('input', (event) => {
    const addLog = password.value.slice(-1).trim();

    if (!passLogValue && addLog !== '*') {
        passLogValue = password.value.slice(-1).trim();
    }
    else if (passLogValue && addLog !== '*') {
        passLogValue += password.value.slice(-1).trim();
    }
    let maskedLogPassword = '*'.repeat(passLogValue.length);
    password.value = maskedLogPassword;
});