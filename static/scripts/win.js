function winScriptFunction() {
    const win = document.querySelector('#win');
    win.style.display = 'flex';
    setTimeout(() => {
        win.style.display = 'none';
    }, 3000);

    const input = document.getElementById('city');
    input.disabled = true;
};