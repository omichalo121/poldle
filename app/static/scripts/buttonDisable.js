const input = document.getElementById('city');
const submitButton = document.getElementById('SB');

input.addEventListener('input', (event) => {
    if (input.value.trim() === '') {
        submitButton.disabled = true;
    }
    else {
        submitButton.disabled = false;
    }
});

function buttonDisableScriptFunction() {
    const submitButton = document.getElementById('SB');
    submitButton.disabled = true;
}