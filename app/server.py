from fastapi import FastAPI, Response, Depends, HTTPException, status, Header
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import FileResponse
from starlette.requests import Request
import sqlite3, random, math, time, threading
from sqlite3.dbapi2 import *
from pydantic import BaseModel
from datetime import date, datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Annotated

SECRET_KEY = "177c743305fc21a93dd66dd13d972723b26367b90cd603d9328b585cf43eb40a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 60

class TokenGiven(BaseModel):
    token: str

class Guess(BaseModel):
    city: str

class Registration(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None
    permission: int or None = None

class User(BaseModel):
    id: int
    username: str
    permission: int
    email: str or None = None
    created: str or None = None
    activity: str or None = None

class UserInDB(User):
    password: str

cx = sqlite3.connect('data.db')
db = cx.cursor()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scheme_name="JWT")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.mount("/static", StaticFiles(directory="static"), name="static")


idOTD = random.randint(393, 979)
idOTD_HARD = random.randint(109, 392)
idOTD_MEDIUM = random.randint(1, 108)
idOTD_EASY = random.randint(1, 37)
today = date.today()
dayToday = today.day
todayInsert = today.strftime("%d/%m/%Y")

# Wybierz random miasto dnia
info = []; infoH = []; infoM = []; infoE = []
cityOTD_info = []; cityOTDH_info = []; cityOTDM_info = []; cityOTDE_info = []

def getInfo(db):
    global cityOTD_info, cityOTDH_info, cityOTDM_info, cityOTDE_info
    cityOTD_info = []; cityOTDH_info = []; cityOTDM_info = []; cityOTDE_info = []

    db.execute("SELECT * FROM miasta WHERE id = ?", (idOTD,))
    info = db.fetchone()
    db.execute("SELECT * FROM miasta WHERE id = ?", (idOTD_HARD,))
    infoH = db.fetchone()
    db.execute("SELECT * FROM miasta WHERE id = ?", (idOTD_MEDIUM,))
    infoM = db.fetchone()
    db.execute("SELECT * FROM miasta WHERE id = ?", (idOTD_EASY,))
    infoE = db.fetchone()


    for i in range(1, 8):
        cityOTD_info.append(info[i])

    for i in range(1, 8):
        cityOTDH_info.append(infoH[i])

    for i in range(1, 8):
        cityOTDM_info.append(infoM[i])

    for i in range(1, 8):
        cityOTDE_info.append(infoE[i])

    print(cityOTD_info)
    print(cityOTDH_info)
    print(cityOTDM_info)
    print(cityOTDE_info)

getInfo(db)

def changeNumbers():
    global idOTD, idOTD_HARD, idOTD_MEDIUM, idOTD_EASY

    while True:
        tomorrow = date.today()
        dayTomorrow = tomorrow.day
        if dayToday != dayTomorrow:
            cx = sqlite3.connect('data.db')
            db = cx.cursor()
            print('it works')
            idOTD = random.randint(393, 979)
            idOTD_HARD = random.randint(109, 392)
            idOTD_MEDIUM = random.randint(1, 108)
            idOTD_EASY = random.randint(1, 37)
            getInfo(db)
        time.sleep(180)

thread = threading.Thread(target=changeNumbers)
thread.start()

def distance_calc(longDAY, longGIVEN, latDAY, latGIVEN):

    # distance calculator
    R = 6371
    lat2_rad = math.radians(latDAY)
    long2_rad = math.radians(longDAY)
    lat1_rad = math.radians(latGIVEN)
    long1_rad = math.radians(longGIVEN)

    dlat = lat2_rad - lat1_rad
    dlon = long2_rad - long1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = round((R * c), 2)

    return distance


def calculate_angle(lat2, lon2, lat1, lon1):
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate the differences in coordinates
    delta_lon = lon2_rad - lon1_rad

    # Calculate the angle using the haversine formula
    y = math.sin(delta_lon) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
    angle_rad = math.atan2(y, x)

    # Convert radians to degrees
    angle_deg = math.degrees(angle_rad)

    # Ensure the angle is within the range of 0 to 360 degrees
    angle_deg = (angle_deg + 360) % 360

    return angle_deg

def rest(infoOTD, info):

    powOTD = infoOTD[4]
    pow = info[4]
    diffpow = round((powOTD - pow), 2)
    arrowPow = round((powOTD / pow), 2)


    ludnOTD = infoOTD[3]
    ludn = info[3]
    diffludn = ludnOTD - ludn
    arrowLudn = round((ludnOTD / ludn), 2)
    return diffpow, diffludn, arrowPow, arrowLudn

def angle_to_direction(angle):

    directions = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE', 'E']
    index = round(angle / 45) % 8
    return directions[index]

# AUTHENTICATION

def verify_password(plainPassword, hashedPassword):
    return pwd_context.verify(plainPassword, hashedPassword)

def getPasswordHash(password):
    return pwd_context.hash(password)

def getUser(username: str):
    db.execute('SELECT * FROM user_data WHERE username = ?', (username,))
    logged = db.fetchone()
    if logged:
        column_names = [description[0] for description in db.description]
        logged_dict = dict(zip(column_names, logged))
        return UserInDB(**logged_dict)

def authUser(username: str, password: str):
    user = getUser(username)
    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user

def createAccessToken(data: dict, expiresDelta: timedelta or None = None):
    toEncode = data.copy()
    if expiresDelta:
        expire = datetime.today() + expiresDelta
    else:
        expire = datetime.today() + timedelta(minutes=15)

    toEncode.update({"exp": expire})
    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT

async def getCurrentUser(token: str = Depends(oauth2_scheme)):
    credentialException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub1")
        permission: int = payload.get("sub2")
        if username is NONE:
            raise credentialException

        token_data = TokenData(username=username, permission=permission)
    except JWTError:
        raise credentialException

    user = getUser(username=token_data.username)
    if user is None:
        raise credentialException

    return user

async def getCurrentActiveUser(currentUser: UserInDB = Depends(getCurrentUser)):
    if currentUser.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return currentUser

@app.post("/token", response_model=Token)
async def loginForAccessToken(login: Login, request: Request):
    user = authUser(login.username, login.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    accessToken = createAccessToken(data={"sub1": user.username, "sub2": user.permission}, expiresDelta=accessTokenExpires)

    db.execute('UPDATE user_data SET activity = ? WHERE username = ?', (todayInsert, user.username))
    db.connection.commit()

    request.session['token'] = accessToken

    return {"access_token": accessToken, "token_type": "bearer"}

@app.get('/register')
async def register():
    return FileResponse('static/register.html', media_type="text/html")

@app.post('/register')
async def reg(register: Registration):
    user = register.username
    passw = getPasswordHash(register.password)

    db.execute('SELECT * FROM user_data WHERE username = ?', (user,))
    exists = db.fetchone()

    if exists:
        return JSONResponse(
            content={
                'success': False,
                'occupied': True
            }
        )
    elif not exists:
        db.execute('SELECT id FROM user_data ORDER BY id DESC LIMIT 1;')
        fetchNumber = db.fetchone()
        (maxId,) = fetchNumber
        maxId += 1

        db.execute('INSERT INTO user_data (id, username, password, permission, created) VALUES (?, ?, ?, ?, ?)', (maxId, user, passw, 0, todayInsert))
        db.connection.commit()

    return JSONResponse(
        content={
            'success': True
        }
    )

@app.get('/extreme')
async def extreme():
    return FileResponse('static/extreme.html', media_type="text/html")

@app.get('/hard')
async def extreme():
    return FileResponse('static/hard.html', media_type="text/html")

@app.get('/medium')
async def extreme():
    return FileResponse('static/medium.html', media_type="text/html")

@app.get('/easy')
async def extreme():
    return FileResponse('static/easy.html', media_type="text/html")

@app.get('/css')
async def css():
    return FileResponse('static/style.css', media_type="text/css")

@app.get('/')
@app.get('/index')
async def root():
    return FileResponse('static/index.html', media_type="text/html")

@app.post('/extreme')
async def guess(guess: Guess):
    CI = []
    CITY = guess.city
    CITY = CITY.title()
    CITY = CITY.replace("Nad", "nad")

    db.execute("SELECT * FROM miasta where nazwa = ?", (CITY,))
    check = db.fetchone()
    if check:
        for i in range(1, 8):
            CI.append(check[i])

        pow, lud, arrP, arrL = rest(cityOTD_info, CI)
        distance = distance_calc(cityOTD_info[5], CI[5], cityOTD_info[6], CI[6])
        angle = calculate_angle(cityOTD_info[6], cityOTD_info[5], CI[6], CI[5])
        dir = angle_to_direction(angle)

        return JSONResponse(
            content={
                'name': CITY,
                'success': True,
                'dir': dir,
                'distance': distance,
                'pow': pow,
                'lud': lud,
                'guessed': distance == 0,
                'arrowP': arrP,
                'arrowL': arrL,
                'powDoTablicy': CI[4],
                'ludDoTablicy': CI[3]
            }
        )
    else:
        return JSONResponse(
            content={
                'success': False
            }
        )

@app.post('/hard')
async def guess(guess: Guess):
    CI = []
    CITY = guess.city
    CITY = CITY.title()
    CITY = CITY.replace("Nad", "nad")

    db.execute("SELECT * FROM miasta where nazwa = ?", (CITY,))
    check = db.fetchone()
    if check:
        for i in range(1, 8):
            CI.append(check[i])

        pow, lud, arrP, arrL = rest(cityOTDH_info, CI)
        distance = distance_calc(cityOTDH_info[5], CI[5], cityOTDH_info[6], CI[6])
        angle = calculate_angle(cityOTDH_info[6], cityOTDH_info[5], CI[6], CI[5])
        dir = angle_to_direction(angle)

        return JSONResponse(
            content={
                'name': CITY,
                'success': True,
                'dir': dir,
                'distance': distance,
                'pow': pow,
                'lud': lud,
                'guessed': distance == 0,
                'arrowP': arrP,
                'arrowL': arrL,
                'powDoTablicy': CI[4],
                'ludDoTablicy': CI[3]
            }
        )
    else:
        return JSONResponse(
            content={
                'success': False
            }
        )



@app.post('/medium')
async def guess(guess: Guess):
    CI = []
    CITY = guess.city
    CITY = CITY.title()
    CITY = CITY.replace("Nad", "nad")

    db.execute("SELECT * FROM miasta where nazwa = ?", (CITY,))
    check = db.fetchone()
    if check:
        for i in range(1, 8):
            CI.append(check[i])

        pow, lud, arrP, arrL = rest(cityOTDM_info, CI)
        distance = distance_calc(cityOTDM_info[5], CI[5], cityOTDM_info[6], CI[6])
        angle = calculate_angle(cityOTDM_info[6], cityOTDM_info[5], CI[6], CI[5])
        dir = angle_to_direction(angle)

        return JSONResponse(
            content={
                'name': CITY,
                'success': True,
                'dir': dir,
                'distance': distance,
                'pow': pow,
                'lud': lud,
                'guessed': distance == 0,
                'arrowP': arrP,
                'arrowL': arrL,
                'powDoTablicy': CI[4],
                'ludDoTablicy': CI[3]
            }
        )
    else:
        return JSONResponse(
            content={
                'success': False
            }
        )


@app.post('/easy')
async def guess(guess: Guess):
    CI = []
    CITY = guess.city
    CITY = CITY.title()
    CITY = CITY.replace("Nad", "nad")

    db.execute("SELECT * FROM miasta where nazwa = ?", (CITY,))
    check = db.fetchone()
    if check:
        for i in range(1, 8):
            CI.append(check[i])

        pow, lud, arrP, arrL = rest(cityOTDE_info, CI)
        distance = distance_calc(cityOTDE_info[5], CI[5], cityOTDE_info[6], CI[6])
        angle = calculate_angle(cityOTDE_info[6], cityOTDE_info[5], CI[6], CI[5])
        dir = angle_to_direction(angle)

        return JSONResponse(
            content={
                'name': CITY,
                'success': True,
                'dir': dir,
                'distance': distance,
                'pow': pow,
                'lud': lud,
                'guessed': distance == 0,
                'arrowP': arrP,
                'arrowL': arrL,
                'powDoTablicy': CI[4],
                'ludDoTablicy': CI[3]
            }
        )
    else:
        return JSONResponse(
            content={
                'success': False
            }
        )

@app.get('/country')
async def country():
    db.execute("SELECT id, nazwa, powiat, szerokosc, dlugosc, powierzchnia, ludnosc FROM miasta")
    rows = db.fetchall()

    columns = [desc[0] for desc in db.description]
    list = [dict(zip(columns, row)) for row in rows]
    return list

@app.get('/city')
async def city(C):
    db.execute("SELECT dlugosc, szerokosc FROM miasta WHERE nazwa = ?", (C,))
    coordinates = db.fetchone()
    return coordinates

@app.get('/getToken')
async def getToken(request: Request):
    token = request.session.get('token')
    logged = 0
    if not token:
        return JSONResponse(
            content={
                'logged': logged,
            })
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub1")
        permission: int = payload.get("sub2")
        if not username:
            return JSONResponse(
                content={
                    'logged': logged,
                })

    except (JWTError, KeyError):
        return JSONResponse(
            content={
                'logged': logged,
            })
    if token:
        logged = 1
        return JSONResponse(
            content={
                'logged': logged,
                'username': username,
                'permission': permission
            })
    return

@app.get("/logout")
async def del_ses(request: Request):
    if 'token' in request.session:
        del request.session['token']

    return RedirectResponse(url="/")

@app.middleware("http")
async def addCacheControlHeader(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response