const Sbmt = document.getElementById('city');
const Bttn = document.getElementById('SB');

Sbmt.addEventListener('keydown', (event) => {
    if (event.key === 'Enter')  {
        Bttn.click();
    }
});