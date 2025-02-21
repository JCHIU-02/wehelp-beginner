from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse 
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
import secrets
import mysql.connector

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key = secrets.token_urlsafe(32))

cnx = mysql.connector.connect(
    user= 'root',
    password = '1234',
    host = 'localhost',
    database = 'website'
    )

def create_user_list():
    with cnx.cursor(buffered=True) as cursor:
        cursor.execute("SELECT username FROM member")
        usernames = cursor.fetchall()
        existed_user = []
        for user in usernames:
            existed_user.append(user[0])
    return existed_user
    

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
async def create_account(
    name: Annotated[str, Form()],
    username: Annotated[str, Form()],
    new_password: Annotated[str, Form()]
    ):

    user_list = create_user_list()
    if username in user_list:
        return RedirectResponse("/error?message=帳號已被註冊，請重新輸入", status_code = 303)
    
    else:
        with cnx.cursor(buffered=True) as cursor:
            cursor.execute('INSERT INTO member(name, username, password) VALUES(%s, %s, %s)', (name, username, new_password))
            cnx.commit()
            return RedirectResponse("/", status_code = 303)
        

@app.post("/signin")
async def verify(
    account: Annotated[str, Form()],
    password: Annotated[str, Form()],
    request: Request
    ):
    
    if not account or not password:
        return RedirectResponse("/error?message=請輸入帳號和密碼", status_code = 303)
    
    with cnx.cursor(buffered=True) as cursor:

        cursor.execute("SELECT password FROM member WHERE username = %s", (account,))
        correct_password = cursor.fetchone()

        cursor.execute("SELECT name FROM member WHERE username = %s", (account,))
        current_name = cursor.fetchone()

        cursor.execute("SELECT id FROM member WHERE username = %s", (account,))
        current_id = cursor.fetchone()

        user_list = create_user_list()
        if account in user_list and password == correct_password[0]:
            request.session["user"] = account
            request.session["name"] = current_name[0]
            request.session["member_id"] = current_id[0]
            return RedirectResponse("/member", status_code = 303)
        else:
            return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code = 303)
        
    
@app.get("/member")
async def member(request: Request):
    if request.session.get("user") == None:
        return RedirectResponse("/")
    
    else:
        current_user = request.session.get("name")
        with cnx.cursor(buffered=True) as cursor:
            cursor.execute(
                """SELECT member.name, message.content, message.id 
                FROM member INNER JOIN message ON member.id = message.member_id
                ORDER BY message.time DESC""")
            history_comments = cursor.fetchall()
            commenter_list = []
            comment_list = []
            message_id_list = []
            for history_comment in history_comments:
                name = history_comment[0]
                comment = history_comment[1]
                id = history_comment[2]
                commenter_list.append(name)
                comment_list.append(comment)
                message_id_list.append(id)
            comments = list(zip(message_id_list, commenter_list, comment_list))

            return templates.TemplateResponse(
                "member.html",
                {
                    "request": request,
                    "title": "Login Successed",
                    "user_status": "歡迎光臨，這是會員頁",
                    "name": current_user,
                    "comments": comments                
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


@app.post("/createMessage")
async def add_comment(comment: Annotated[str, Form()], request: Request):
    # 將留言存入資料庫
    member_id = request.session.get("member_id")
    with cnx.cursor(buffered=True) as cursor:
        cursor.execute("INSERT INTO message(member_id, content) VALUES(%s, %s)", (member_id, comment))
        cnx.commit()

    return RedirectResponse("/member", status_code = 303)


@app.post("/deleteMessage")
async def delete_comment(message_id: Annotated[str, Form()]):
    with cnx.cursor(buffered=True) as cursor:
        cursor.execute("DELETE FROM message WHERE id = %s", (message_id,))
        cnx.commit()
    return RedirectResponse("/member", status_code = 303)


app.mount("/static", StaticFiles(directory="static"), name="static")