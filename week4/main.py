from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse 
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
import secrets

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key = secrets.token_urlsafe(32))


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Homepage",
            "user_status": "歡迎光臨，請輸入帳號密碼"
        }
    )
    
@app.post("/signin")
async def verify(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    request: Request):
    
    if not username or not password:
        return RedirectResponse("/error?message=請輸入帳號和密碼", status_code = 303)
    
    if username == "test" and password == "test":
        request.session["user"] = username
        return RedirectResponse("/member", status_code = 303)
    else:
        return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code = 303)
    
@app.get("/member")
async def member(request: Request):
    if request.session.get("user") == None:
        return RedirectResponse("/")

    return templates.TemplateResponse(
        "member.html",
        {
            "request": request,
            "title": "Login Successed",
            "user_status": "歡迎光臨，這是會員頁"
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



@app.get("/square/{number}")
async def calculate_square(request: Request, number: int):
    return templates.TemplateResponse(
        "square.html",
        {
            "request": request,
            "title": "Calculator",
            "user_status": "正整數平方計算結果",
            "result": number * number
        }
    )


app.mount("/static", StaticFiles(directory="static"), name="static")
