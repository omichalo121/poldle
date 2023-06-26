function redirect() {
    const form = document.createElement('form');
    document.body.appendChild(form)
    form.method = 'GET';
    form.action = '/';

    form.submit();
}
const register = () => {
    const log = document.getElementById('username_r');
    const pass = document.getElementById('password_r');
    const passAcc = document.getElementById('password-accept_r');
    const inf = document.getElementById('passwordAcc-text');
    const infBlock = document.getElementById('password-info');
    const infBlock2 = document.getElementById('passwordAcc-info');
    const succ = document.getElementById('success');

    const u = log.value.trim();
    const space = u.includes(' ');
    const p = passValue;
    const pA = passAccValue;

    if(space) {
        return;
    }

    if(p !== pA) {
        [pass.value, passAcc.value] = ['', ''];
        [passAccValue, passValue, maskedAccPassword, maskedPassword] = [null, null, null, null];
        inf.textContent = 'Hasła muszą być takie same';
        infBlock2.style.display = 'flex';
        infBlock.style.display = 'none';
        return;
    } else if (p === pA) {
        fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: u,
            password: p
            })
        })
        .then(res => {
            res.json().then(response => {
                if (response.success) {
                    succ.textContent = 'Pomyślnie zarejestrowano! Zostaniesz przekierowany na stronę główną.';
                    setTimeout(redirect, 2500);
                    return;
                } else if (response.occupied) {
                    succ.textContent = 'Ten login jest już zajęty.';
                    return; }
            })
        })
    }
}