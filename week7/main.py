from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse 
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
import secrets
import mysql.connector
from pydantic import BaseModel

class UpdateName(BaseModel):
    name: str

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key = secrets.token_urlsafe(32))

def create_db_connection():
    return mysql.connector.connect(
    user= 'root',
    password = '1234',
    host = 'localhost',
    database = 'website'
    )

@app.get("/api/member")
async def get_member_data(username: str, request: Request):

    cnx = create_db_connection()

    with cnx.cursor(buffered=True) as cursor:
        cursor.execute("SELECT id, name FROM member WHERE username=%s",(username,))
        user_data = cursor.fetchone()
        cnx.close()
    
    if request.session.get("user") is None or user_data is None:
        return{
            "data": None
        }     
    
    else:
        return{
            "data":{
                "id":user_data[0],
                "name":user_data[1],
                "username":username
            }
        }
    
    
@app.patch("/api/member")
async def update_name(name_update: UpdateName, request: Request):

    new_name = name_update.name
    cnx = create_db_connection()
    username = request.session.get("user")

    try:
        with cnx.cursor(buffered=True) as cursor:
            cursor.execute("UPDATE member SET name=%s WHERE username=%s",(new_name, username))
            cnx.commit()
            cnx.close()

            return{
                "ok": True
            }
    
    except:
        return{
            "error": True
        }
    
    
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Homepage",
            "user_status": "歡迎光臨，請註冊登入系統"
        }
    )

@app.post("/signup")
async def create_username(
    name: Annotated[str, Form()],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
    ):

    cnx = create_db_connection()

    with cnx.cursor(buffered=True) as cursor:
        cursor.execute('SELECT username FROM member WHERE username = %s', (username,))
        existed_user = cursor.fetchone()
    
        if existed_user == None:
            cursor.execute('INSERT INTO member(name, username, password) VALUES(%s, %s, %s)', (name, username, password))
            cnx.commit()
            cnx.close()
            return RedirectResponse("/", status_code = 303)
        
        else:
            cnx.close()
            return RedirectResponse("/error?message=帳號已被註冊，請重新輸入", status_code = 303)
        

@app.post("/signin")
async def verify(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    request: Request
    ):
    
    if not username or not password:
        return RedirectResponse("/error?message=請輸入帳號和密碼", status_code = 303)
    
    cnx = create_db_connection()
    
    with cnx.cursor(buffered=True) as cursor:

        cursor.execute("SELECT id, name, username, password FROM member WHERE username = %s", (username,))
        match_user_data = cursor.fetchone()

        if match_user_data is not None:
            if username == match_user_data[2] and password == match_user_data[3]:
                request.session["user"] = match_user_data[2]
                request.session["name"] = match_user_data[1]
                request.session["member_id"] = match_user_data[0]
                cnx.close()
                return RedirectResponse("/member", status_code = 303)
            else:
                cnx.close()
                return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code = 303)
        else:
            return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code = 303)

        
    
@app.get("/member")
async def member(request: Request):
    if request.session.get("user") == None:
        return RedirectResponse("/")
    
    else:
        current_user = request.session.get("name")

        return templates.TemplateResponse(
            "member.html",
            {
                "request": request,
                "title": "Login Successed",
                "user_status": "歡迎光臨，這是會員頁",
                "name": current_user      
            }
        )
    

@app.get("/error")
async def member(request: Request):
    message = request.query_params.get("message")

    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "title": "Login Failed",
            "user_status": "失敗頁面",
            "message": message
        }
    )


@app.get("/signout")
async def signout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


app.mount("/static", StaticFiles(directory="static"), name="static")
