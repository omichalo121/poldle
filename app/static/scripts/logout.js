function logout() {
    const form = document.createElement('form');
    form.method = 'GET';
    form.action = '/logout';

    document.body.appendChild(form)
    form.submit()
}