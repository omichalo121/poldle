from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import FileResponse, HTMLResponse
from starlette.requests import Request
import sqlite3, random, math, time, threading, pytz, calendar
from sqlite3.dbapi2 import *
from pydantic import BaseModel
from datetime import date, datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "177c743305fc21a93dd66dd13d972723b26367b90cd603d9328b585cf43eb40a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 60

class TokenGiven(BaseModel):
    token: str

class Guess(BaseModel):
    city: str
    diff: str

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
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, session_cookie='PoldleCookie')
app.mount("/static", StaticFiles(directory="static"), name="static")

idOTD = random.randint(393, 979)
idOTD_HARD = random.randint(109, 392)
idOTD_MEDIUM = random.randint(38, 108)
idOTD_EASY = random.randint(1, 37)

timezone = pytz.timezone('Europe/Warsaw')
today = datetime.now(timezone)

today = today.date()
dayToday = today.day
todayInsert = today.strftime("%d/%m/%Y")

# Wybierz random miasto dnia
info = []; infoH = []; infoM = []; infoE = []
cityOTD_extreme_info = []; cityOTD_hard_info = []; cityOTD_medium_info = []; cityOTD_easy_info = []
cityOYD = []; cityOYDH = []; cityOYDM = []; cityOYDE = []

def getInfo(db):
    global cityOTD_extreme_info, cityOTD_hard_info, cityOTD_medium_info, cityOTD_easy_info
    cityOTD_extreme_info = []; cityOTD_hard_info = []; cityOTD_medium_info = []; cityOTD_easy_info = []

    db.execute("SELECT * FROM miasta WHERE id = ?", (idOTD,))
    info = db.fetchone()
    db.execute("SELECT * FROM miasta WHERE id = ?", (idOTD_HARD,))
    infoH = db.fetchone()
    db.execute("SELECT * FROM miasta WHERE id = ?", (idOTD_MEDIUM,))
    infoM = db.fetchone()
    db.execute("SELECT * FROM miasta WHERE id = ?", (idOTD_EASY,))
    infoE = db.fetchone()


    for i in range(1, 8):
        cityOTD_extreme_info.append(info[i])

    for i in range(1, 8):
        cityOTD_hard_info.append(infoH[i])

    for i in range(1, 8):
        cityOTD_medium_info.append(infoM[i])

    for i in range(1, 8):
        cityOTD_easy_info.append(infoE[i])

    print(cityOTD_extreme_info)
    print(cityOTD_hard_info)
    print(cityOTD_medium_info)
    print(cityOTD_easy_info)

getInfo(db)

def changeDay():
    global idOTD, idOTD_HARD, idOTD_MEDIUM, idOTD_EASY
    global cityOYD, cityOYDH, cityOYDM, cityOYDE, dayToday
    while True:
        tomorrow = datetime.now(timezone)
        tomorrow = tomorrow.date()
        dayTomorrow = tomorrow.day
        if dayToday != dayTomorrow:
            cityOYD = []; cityOYDH = []; cityOYDM = []; cityOYDE = []
            cityOYD.append(cityOTD_extreme_info[0])
            cityOYDH.append(cityOTD_hard_info[0])
            cityOYDM.append(cityOTD_medium_info[0])
            cityOYDE.append(cityOTD_easy_info[0])

            dayToday = dayTomorrow

            cx = sqlite3.connect('data.db')
            db = cx.cursor()

            db.execute('UPDATE infoOTD SET sum_of_tries = 0, winnersCount  = 0, averageTry  = 0, `1st` = NULL, `2nd` = NULL, `3rd` = NULL, `4th` = NULL, `5th` = NULL')
            db.execute('UPDATE userIndividual SET todayTries = 0, won = 0')
            db.execute('DELETE FROM tablica')
            db.connection.commit()

            db.execute('SELECT id from user_data ORDER BY id DESC LIMIT 1')
            (max,) = db.fetchone()

            if dayToday == 1:
                db.execute('SELECT username from user_data')
                check = db.fetchone()
                if check is not None:
                    db.execute('UPDATE userIndividual SET averageTries = 0, `1` = NULL, `2` = NULL, `3` = NULL, `4` = NULL, `5` = NULL, `6` = NULL, `7` = NULL, `8` = NULL, `9` = NULL, `10` = NULL, `11` = NULL, `12` = NULL, `13` = NULL, `14` = NULL, `15` = NULL, `16` = NULL, `17` = NULL, `18` = NULL, `19` = NULL, `20` = NULL, `21` = NULL, `22` = NULL, `23` = NULL, `24` = NULL, `25` = NULL, `26` = NULL, `27` = NULL, `28` = NULL, `29` = NULL, `30` = NULL, `31` = NULL')
                    db.connection.commit()

            c = 1
            while c != max + 1:
                db.execute('SELECT username from user_data WHERE id = ?', (c,))
                check = db.fetchone()
                if check is not None:
                    difficulties = ['easy', 'medium', 'hard', 'extreme']
                    for i in range(0, 4):
                        db.execute('SELECT winstreakNow, winstreakYest FROM userIndividual WHERE difficulty = ? COLLATE BINARY AND id = ?', (difficulties[i], c))
                        check = db.fetchone()
                        if check is not None:
                            (tod, yes) = check

                            if tod == yes:
                                db.execute('UPDATE userIndividual SET winstreakNow = 0, winstreakYest = 0 WHERE difficulty = ? COLLATE BINARY AND id = ?', (difficulties[i], c))
                                db.connection.commit()
                            else:
                                db.execute('UPDATE userIndividual SET winstreakYest = ? WHERE difficulty = ? COLLATE BINARY AND id = ?', (tod, difficulties[i], c))
                                db.connection.commit()

                    c += 1
                else:
                    c += 1

            idOTD = random.randint(393, 979)
            idOTD_HARD = random.randint(109, 392)
            idOTD_MEDIUM = random.randint(38, 108)
            idOTD_EASY = random.randint(1, 37)
            getInfo(db)

        time.sleep(180)

thread = threading.Thread(target=changeDay)
thread.start()

def tableUpdater(number, difficulty, user):

    db.execute('SELECT sum_of_tries, winnersCount FROM infoOTD WHERE difficulty = ? COLLATE BINARY', (difficulty,))
    data = db.fetchone()
    (tries, people) = data
    tries += number
    people += 1
    countDays = 0
    numberSum = 0
    average = round((tries / people), 1)
    db.execute('UPDATE infoOTD SET sum_of_tries = ?, winnersCount = ?, averageTry = ? WHERE difficulty = ? COLLATE BINARY', (tries, people, average, difficulty))
    db.connection.commit()

    if user != 'noUser':
        db.execute(f'UPDATE userIndividual SET `{dayToday}` = ? WHERE difficulty = ? COLLATE BINARY AND id = (SELECT id FROM user_data WHERE username = ? COLLATE BINARY)', (number, difficulty, user))
        db.connection.commit()

        db.execute('SELECT `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31` FROM userIndividual WHERE difficulty = ? COLLATE BINARY AND id = (SELECT id FROM user_data WHERE username = ?)', (difficulty, user))
        average = db.fetchone()
        average = list(average)
        for i in range(len(average)):
            if average[i] is None:
                continue
            if average[i] != 'NULL' or average[i] == 0:
                print(average[i])
                countDays += 1
                numberSum += int(average[i])

        averageFinal = round((numberSum / countDays), 2)
        db.execute('UPDATE userIndividual SET averageTries = ? WHERE difficulty = ? AND id = (SELECT id FROM user_data WHERE username = ? COLLATE BINARY)', (averageFinal, difficulty, user))
        db.connection.commit()

        db.execute('SELECT guessed, winstreakNow, winstreakBest, oneshotTries FROM userIndividual WHERE difficulty = ? COLLATE BINARY and id = (SELECT id FROM user_data WHERE username = ? COLLATE BINARY)', (difficulty, user))
        numbers = db.fetchone()
        (guessed, wsNow, wsBest, oneshotTry) = numbers
        guessed += 1
        wsNow += 1

        if wsBest < wsNow:
            wsBest = wsNow

        if number == 1:
            oneshotTry += 1

        db.execute(f'UPDATE userIndividual SET `{dayToday}` = ?, guessed = ?, winstreakNow = ?, winstreakBest = ?, todayTries = ?, oneshotTries = ? WHERE difficulty = ? COLLATE BINARY and id = (SELECT id FROM user_data WHERE username = ? COLLATE BINARY)', (number, guessed, wsNow, wsBest, number, oneshotTry, difficulty, user))
        db.connection.commit()

        db.execute('SELECT `1st`, `2nd`, `3rd`, `4th`, `5th` FROM infoOTD WHERE difficulty = ? COLLATE BINARY', (difficulty,))
        podium = db.fetchone()
        columns = ['1st', '2nd', '3rd', '4th', '5th']
        for i in range(len(podium)):
            if podium[i] == user:
                return
            elif not podium[i]:
                column = columns[i]
                db.execute(f'UPDATE infoOTD SET `{column}` = ? WHERE difficulty = ? COLLATE BINARY', (user, difficulty))
                db.connection.commit()
                return
    return

def addToFavCity(city, powiat, difficulty, user):

    db.execute('SELECT count from userFavCity WHERE city = ? AND powiat = ? AND difficulty = ? COLLATE BINARY AND id = (SELECT id from user_data WHERE username = ?)', (city, powiat, difficulty, user))
    count = db.fetchone()
    if count is not None:
        count = list(count)[0]
        count += 1
        db.execute('UPDATE userFavCity SET count = ? WHERE city = ? AND powiat = ? AND difficulty = ? COLLATE BINARY AND id = (SELECT id from user_data WHERE username = ?)', (count, city, powiat, difficulty, user))
        db.connection.commit()
    else:
        db.execute('SELECT id from user_data where username = ?', (user,))
        id = list(db.fetchone())[0]
        db.execute('INSERT INTO userFavCity (id, difficulty, city, powiat, count) VALUES (?, ?, ?, ?, ?)', (id, difficulty, city, powiat, 1))
        db.connection.commit()

    return

def getChart(difficulty, user):

    db.execute('SELECT `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31` FROM userIndividual WHERE difficulty = ? COLLATE BINARY AND id = (SELECT id FROM user_data WHERE username = ?)', (difficulty, user))
    info = db.fetchone()

    column_names = [description[0] for description in db.description]
    infoGot = dict(zip(column_names, info))

    keys = list(infoGot.keys())
    month = int(today.month)
    year = int(today.year)
    _, length = calendar.monthrange(year, month)

    infoNew = {}
    Cx = 0

    for i in range(length):
        if month >= 10:
            keys[i] = f'{keys[i]}/{month}'
        else:
            keys[i] = f'{keys[i]}/0{month}'

    for items in infoGot.items():
        if items[1] == 'NULL':
            value = 0
        else:
            value = items[1]

        new_key = keys[Cx]
        infoNew[new_key] = value
        Cx += 1

    difference = 31 - length
    for i in range(difference):
        del infoNew[f'{31 - i}']

    labels = list(infoNew.keys())
    values = list(infoNew.values())

    first_number = next((index for index, num in enumerate(values) if num != 0 or num is not None), None)
    last_number = next((index for index, num in enumerate(values[::-1]) if num != 0), None)
    if last_number == None:
        last_number = 0

    if first_number == 0 and last_number == 0:
        turnOff = 1
        todday = 1
        return values[first_number:last_number], labels[todday-1:], turnOff
    else:
        last_number = length - last_number
        turnOff = 0
        return values[first_number:last_number+1], labels[first_number:last_number+1], turnOff


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
    db.execute('SELECT * FROM user_data WHERE username = ? COLLATE BINARY', (username,))
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
        if username is None:
            raise credentialException

        token_data = TokenData(username=username, permission=permission)
    except JWTError:
        raise credentialException

    user = getUser(username=token_data.username)
    if user is None:
        raise credentialException

    return user.username

@app.post("/token", response_model=Token)
async def loginForAccessToken(login: Login, request: Request):
    user = authUser(login.username, login.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    accessToken = createAccessToken(data={"sub1": user.username, "sub2": user.permission}, expiresDelta=accessTokenExpires)

    db.execute('UPDATE user_data SET activity = ? WHERE username = ? COLLATE BINARY', (todayInsert, user.username))
    db.connection.commit()

    request.session['token'] = accessToken

    return {"access_token": accessToken, "token_type": "bearer"}

@app.get('/register')
async def register(request: Request):
    if 'token' in request.session:
        return RedirectResponse(url="/")
    else:
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
        if fetchNumber is not None:
            (maxId,) = fetchNumber
            maxId += 1
        else:
            maxId = 1

        db.execute('INSERT INTO user_data (id, username, password, permission, created) VALUES (?, ?, ?, ?, ?)', (maxId, user, passw, 0, todayInsert))
        db.execute('INSERT INTO userIndividual (id, difficulty, guessed, winstreakNow, winstreakBest, todayTries, averageTries, oneshotTries, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, winstreakYest, won) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (maxId, 'easy', 0, 0, 0, 0, 0, 0, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 0, 0))
        db.execute('INSERT INTO userIndividual (id, difficulty, guessed, winstreakNow, winstreakBest, todayTries, averageTries, oneshotTries, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, winstreakYest, won) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (maxId, 'medium', 0, 0, 0, 0, 0, 0, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 0, 0))
        db.execute('INSERT INTO userIndividual (id, difficulty, guessed, winstreakNow, winstreakBest, todayTries, averageTries, oneshotTries, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, winstreakYest, won) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (maxId, 'hard', 0, 0, 0, 0, 0, 0, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 0, 0))
        db.execute('INSERT INTO userIndividual (id, difficulty, guessed, winstreakNow, winstreakBest, todayTries, averageTries, oneshotTries, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, winstreakYest, won) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (maxId, 'extreme', 0, 0, 0, 0, 0, 0, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 0, 0))
        db.connection.commit()

    return JSONResponse(
        content={
            'success': True
        }
    )
@app.get('/privacy')
async def privacy():
    return FileResponse('static/privacy.html', media_type="text/html")

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

@app.post('/checkCity')
async def guess(guess: Guess, request: Request):
    CI = []
    diff = guess.diff
    name = f"cityOTD_{diff}_info"
    cityOTD_info = globals().get(name)
    CITY = guess.city
    CITY = CITY.title()
    CITY = CITY.replace("Nad", "nad")
    session = request.session

    if 'token' in request.session:
        username = await getCurrentUser(request.session['token'])
        if not username:
            return
        else:
            db.execute('SELECT won FROM userIndividual WHERE difficulty = ? COLLATE BINARY AND id = (SELECT id from user_data WHERE username = ?)', (diff, username))
            (wonCheck,) = db.fetchone()
    else:
        wonCheck = 0
        username = 0

    if session.get(f"won_game_{diff}", False) and 'token' not in request.session or wonCheck == 1:
        return JSONResponse(
            content={
                'success': False
            }
        )

    db.execute("SELECT * FROM miasta where nazwa = ?", (CITY,))
    check = db.fetchone()
    if check:
        for i in range(1, 8):
            CI.append(check[i])

        pow, lud, arrP, arrL = rest(cityOTD_info, CI)
        distance = distance_calc(cityOTD_info[5], CI[5], cityOTD_info[6], CI[6])
        angle = calculate_angle(cityOTD_info[6], cityOTD_info[5], CI[6], CI[5])
        dir = angle_to_direction(angle)

        if 'token' in request.session:
            if username:
                powiat = check[2]
                addToFavCity(CITY, powiat, diff, username)

                db.execute('SELECT id FROM user_data WHERE username = ?', (username,))
                (id,) = db.fetchone()
                db.execute('SELECT count FROM tablica WHERE difficulty = ? COLLATE BINARY AND id = ? ORDER BY count DESC LIMIT 1', (diff, id))
                cnt2 = db.fetchone()
                if cnt2 is None:
                    cnt2 = 1
                    db.execute('INSERT INTO tablica (id, difficulty, count, name, dir, distance, pow, lud, arrowP, arrowL, powDoTablicy, ludDoTablicy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, diff, cnt2, CITY, dir, distance, pow, lud, arrP, arrL, CI[4], CI[3]))
                    db.connection.commit()
                else:
                    (cnt2,) = cnt2
                    cnt2 += 1
                    db.execute('INSERT INTO tablica (id, difficulty, count, name, dir, distance, pow, lud, arrowP, arrowL, powDoTablicy, ludDoTablicy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, diff, cnt2, CITY, dir, distance, pow, lud, arrP, arrL, CI[4], CI[3]))
                    db.connection.commit()
        else:
            request.session['day'] = dayToday

        if distance == 0 and 'token' in request.session:
            db.execute('UPDATE userIndividual SET won = ? WHERE difficulty = ? AND id = (SELECT id FROM user_data WHERE username = ?)', (1, diff, username))
            db.connection.commit()
        elif distance == 0 and 'token' not in request.session:
            data_name = f"won_game_{diff}"
            request.session[data_name] = True

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
                'ludDoTablicy': CI[3],
                'username': username
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

@app.post("/averageCount")
async def countAVRG(request: Request):
    data = await request.json()
    number = data.get('number')
    difficulty = data.get('difficulty')

    if 'token' in request.session:
        username = await getCurrentUser(request.session['token'])
        if not username:
            username = 'noUser'
    else:
        username = 'noUser'

    tableUpdater(number, difficulty, username)
    return

@app.post("/getStats")
async def getStats(request: Request):
    difficulty = await request.json()

    if difficulty == 'easy':
        city = cityOYDE
    elif difficulty == 'medium':
        city = cityOYDM
    elif difficulty == 'hard':
        city = cityOYDH
    else:
        city = cityOYD

    db.execute('SELECT winnersCount, averageTry, `1st`, `2nd`, `3rd`, `4th`, `5th` FROM infoOTD WHERE difficulty = ? COLLATE BINARY', (difficulty,))
    data = db.fetchone()
    (sumOfTries, averageTry) = data[0:2]
    winners = data[2:7]

    return JSONResponse(
        content={
            'tries': sumOfTries,
            'average': averageTry,
            'miasto': city,
            'winners': winners
        }
    )

@app.post("/userStats")
async def getUserStats(request: Request):
    difficulty = await request.json()

    if 'token' not in request.session:
        return
    else:
        username = await getCurrentUser(request.session['token'])
        if not username:
            return

    if difficulty == 'user':
        db.execute('SELECT guessed, oneshotTries FROM userIndividual WHERE id = (SELECT id from user_data WHERE username = ? COLLATE BINARY)', (username,))
        (easyU, mediumU, hardU, extremeU) = db.fetchall()

        easyU = list(easyU)
        if easyU[1] != 0:
            percentE = round(((easyU[1] / easyU[0]) * 100), 1)
            easyU.append(f'({percentE}% wszystkich strzałów)')
        else:
            easyU.append('(Jeszcze ci się nie udało!)')

        mediumU = list(mediumU)
        if mediumU[1] != 0:
            percentM = round(((mediumU[1] / mediumU[0]) * 100), 1)
            mediumU.append(f'({percentM}% wszystkich strzałów)')
        else:
            mediumU.append('(Jeszcze ci się nie udało!)')

        hardU = list(hardU)
        if hardU[1] != 0:
            percentH = round(((hardU[1] / hardU[0]) * 100), 1)
            hardU.append(f'({percentH}% wszystkich strzałów)')
        else:
            hardU.append('(Jeszcze ci się nie udało!)')

        extremeU = list(extremeU)
        if extremeU[1] != 0:
            percentEX = round(((extremeU[1] / extremeU[0]) * 100), 1)
            extremeU.append(f'({percentEX}% wszystkich strzałów)')
        else:
            extremeU.append('(Jeszcze ci się nie udało!)')

        db.execute('SELECT city FROM userFavCity WHERE id = (SELECT id from user_data WHERE username = ? COLLATE BINARY) ORDER BY count DESC LIMIT 1', (username,))
        city = db.fetchone()
        if city is not None:
            (city,) = city
        else:
            city = 'Odziwo jeszcze nie masz!'

        return JSONResponse(
            content= {
                'easy': easyU,
                'medium': mediumU,
                'hard': hardU,
                'extreme': extremeU,
                'city': city
            }
        )
    else:
        db.execute('SELECT winstreakNow, winstreakBest, todayTries, averageTries from userIndividual WHERE difficulty = ? COLLATE BINARY AND id = (SELECT id from user_data WHERE username = ?)', (difficulty, username))
        (wsNow, wsBest, todayT, avgT) = db.fetchone()

        db.execute('SELECT city FROM userFavCity where difficulty = ? COLLATE BINARY AND id = (SELECT id from user_data WHERE username = ?)', (difficulty, username))
        cityUser = db.fetchone()
        if cityUser is not None:
            (cityUser,) = cityUser
        else:
            cityUser = 'Jeszcze nie ma!'

        (values, labels, turnOff) = getChart(difficulty, username)

        return JSONResponse(
            content={
                'wsNow': wsNow,
                'wsBest': wsBest,
                'todayT': todayT,
                'avgT': avgT,
                'city': cityUser,
                'values': values,
                'labels': labels,
                'turnOff': turnOff
            }
        )

@app.post("/checkWon")
async def checkIfWon(request: Request):
    diff = await request.json()
    session = request.session
    tablicaChanged = []
    if session.get('token') != None:
        response = 0
        logged = 1
        try:
            payload = jwt.decode(request.session['token'], SECRET_KEY, algorithms=[ALGORITHM])
            username : str = payload.get("sub1")
        except:
            username = "noUser"
            del request.session['token']

        if username != "noUser":
            db.execute('SELECT won FROM userIndividual WHERE difficulty = ? COLLATE BINARY AND id = (SELECT id from user_data WHERE username = ?)', (diff, username))
            (wonCheck,) = db.fetchone()

            db.execute('SELECT count FROM tablica WHERE difficulty = ? COLLATE BINARY and id = (SELECT id from user_data where username = ?) ORDER BY count DESC LIMIT 1', (diff, username))
            count = db.fetchone()
            if count is not None:
                (count,) = count
            else:
                count = 0

            db.execute('SELECT name, dir, distance, pow, lud, arrowP, arrowL, powDoTablicy, ludDoTablicy FROM tablica WHERE difficulty = ? COLLATE BINARY AND id = (SELECT id from user_data where username = ?) ORDER BY count ASC', (diff, username))
            tablica = db.fetchall()
            if tablica is not None:
                tablicaChanged = [
                    (('false', item[0]) + item[1:]) if item[2] != 0 else (('true', item[0]) + item[1:])
                    for item in tablica
                ]
        else:
            wonCheck = 0
            count = 0
            tablicaChanged = 0
    else:
        wonCheck = 0
        count = 0
        tablicaChanged = 0

    tomorrow = datetime.now(timezone)
    tomorrow = tomorrow.date()
    dayTomorrow = tomorrow.day
    if session.get('day') is not None and session.get('token') == None or session.get('day') is not None and wonCheck == 0:
        tokenDate = request.session['day']
    else:
        tokenDate = dayToday
        request.session[f"won_game_{diff}"] = False

    if 'token' not in request.session:
        logged = 0
        if dayTomorrow != tokenDate:
            response = 1
            if request.session[f'won_game_{diff}'] == True:
                request.session[f"won_game_{diff}"] = False
        else:
            response = 0

    if session.get(f"won_game_{diff}", False) and session.get('token') == None or wonCheck == 1:
        won = 1
    else:
        won = 0

    return JSONResponse(
        content={
            'won': won,
            'tablica': tablicaChanged,
            'count': count,
            'clear': response,
            'user': logged
        }
    )

@app.middleware("http")
async def addCacheControlHeader(request: Request, call_next):

    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response