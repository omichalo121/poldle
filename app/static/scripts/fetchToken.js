const regLog = document.getElementById('regLog');
const logOut = document.getElementById('logoutButt');
fetch('/getToken')
.then(res => {
    res.json().then(response => {
        if(response.logged === 1){
            logOut.style.display = 'flex';
            console.log(response.logged);
        }
        else {
            regLog.style.display = 'flex'
        }
    })
})
.catch(err => {
    console.log(err)
});