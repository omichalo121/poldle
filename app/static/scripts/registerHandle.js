const loginCheck = document.getElementById('username_r');
const loginBox = document.getElementById('login-info');
const loginText = document.getElementById('login-text');

const passwordCheck = document.getElementById('password_r');
const passwordBox = document.getElementById('password-info');
const passwordText = document.getElementById('password-text');

const passwordAccept = document.getElementById('password-accept_r');
const passAccBlock = document.getElementById('passwordAcc-info');

const RB = document.getElementById('register');

// Disabling the button

loginCheck.addEventListener('input', loginHandler);
passwordCheck.addEventListener('input', loginHandler);
passwordAccept.addEventListener('input', loginHandler);

function loginHandler() {
    if(loginCheck.value.trim() === '' || passwordCheck.value.trim() === '' || passwordAccept.value.trim() === '') {
        RB.disabled = true;
    }
    else {
        RB.disabled = false;
    }
}

const handleEnter = (event) => {
    if(event.key === 'Enter' && RB.disabled === false) {
        RB.click();
    }
}

loginCheck.addEventListener('keydown', handleEnter);
passwordCheck.addEventListener('keydown', handleEnter);
passwordAccept.addEventListener('keydown', handleEnter);

// Registering the appropiate password and login

loginCheck.addEventListener('input', (event) => {
    const logValue = loginCheck.value.trim();
    const invalidChar = logValue.match(/[!@#$%^&*()_+<>?{}:";\-=`[\]]/);
    const loginSpace = logValue.includes(' ');

    if(loginSpace) {
        loginText.textContent = 'Login nie powinien zawierać spacji ';
        loginBox.style.display = 'flex';
    }
    else if(!loginSpace) {
        if(logValue.length <= 2) {
            loginText.textContent = 'Login jest za krótki ';
            loginBox.style.display = 'flex';
        }
        else if (invalidChar !== null && invalidChar.length > 0) {
                loginText.textContent = 'Login zawiera niedozwolone znaki';
                loginBox.style.display = 'flex';
        }
        else {
            loginText.textContent = 'Login poprawny';
                loginBox.style.display = 'flex';
        }
    }
});


let passValue;

passwordCheck.addEventListener('keydown', (event) => {

    if (event.key === 'Backspace') {

        const selectionStart = passwordCheck.selectionStart;
        const selectionEnd = passwordCheck.selectionEnd;

        if (selectionStart !== selectionEnd) {
            passValue = passValue.slice(0, selectionStart) + passValue.slice(selectionEnd);
        } else {
            passValue = passValue.slice(0, -1);
        }
    }
});

passwordCheck.addEventListener('input', (event) => {

    const add = passwordCheck.value.slice(-1).trim();

    if (!passValue && add !== '*') {
        passValue = passwordCheck.value.slice(-1).trim();
    }
    else if (passValue && add !== '*') {
        passValue += passwordCheck.value.slice(-1).trim();
    }

    let maskedPassword = '*'.repeat(passValue.length);

    if(!passValue) {
        passwordText.textContent = 'Hasło jest za krótkie ';
        passwordBox.style.display = 'flex';
    }
    else {
        const bigLetter = passValue.match(/[A-Z]/);
        const smallLetter = passValue.match(/[a-z]/);
        const number = passValue.match(/[0-9]/);
        const invalidChar = passValue.match(/[!@#$%^&*()_+<>?{}:";\-=`[\]]/);

        if (invalidChar && invalidChar.length > 0) {
            passwordText.textContent = 'Hasło zawiera niedozwolone znaki';
            passwordBox.style.display = 'flex';
        } else if (!bigLetter) {
            passwordText.textContent = 'Hasło musi zawierać przynajmniej 1 dużą literę';
            passwordBox.style.display = 'flex';
        } else if (!smallLetter) {
            passwordText.textContent = 'Hasło musi zawierać przynajmniej 1 małą literę';
            passwordBox.style.display = 'flex';
        } else if (!number) {
            passwordText.textContent = 'Hasło musi zawierać przynajmniej 1 liczbę';
            passwordBox.style.display = 'flex';
        } else if (passValue.length <= 5) {
            passwordText.textContent = 'Hasło zbyt krótkie';
            passwordBox.style.display = 'flex';
        } else if (number && bigLetter && smallLetter) {
            passwordText.textContent = 'Hasło poprawne';
            passwordBox.style.display = 'flex';
        }
    }
    passwordCheck.value = maskedPassword;
});

let passAccValue;

passwordAccept.addEventListener('keydown', (event) => {
    if (event.key === 'Backspace') {

        const selectionStart2 = passwordAccept.selectionStart;
        const selectionEnd2 = passwordAccept.selectionEnd;

        if (selectionStart2 !== selectionEnd2) {
            passAccValue = passAccValue.slice(0, selectionStart2) + passAccValue.slice(selectionEnd2);
        } else {
            passAccValue = passAccValue.slice(0, -1);
        }
    }
});

passwordAccept.addEventListener('input', (event) => {
    const addAcc = passwordAccept.value.slice(-1).trim();
    passAccBlock.style.display = 'none';

    if (!passAccValue && addAcc !== '*') {
        passAccValue = passwordAccept.value.slice(-1).trim();
    }
    else if (passAccValue && addAcc !== '*') {
        passAccValue += passwordAccept.value.slice(-1).trim();
    }
    let maskedAccPassword = '*'.repeat(passAccValue.length);
    passwordAccept.value = maskedAccPassword;
});