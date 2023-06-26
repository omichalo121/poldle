@app.get('/logged')
async def logged(request: Request):
    token = request.session.get('token')
    if not token:
        return FileResponse('static/index.html', media_type="text/html")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub1")
        permission: int = payload.get("sub2")
        if not username:
            return FileResponse('static/index.html', media_type="text/html")

    except (JWTError, KeyError):
        return FileResponse('static/index.html', media_type="text/html")

    print(username, permission)

    return FileResponse('static/loggedIndex.html', media_type="text/html")