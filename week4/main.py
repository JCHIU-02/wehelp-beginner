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
async def home(request: Request): #Request = request 這個參數的型別提示，like str, int, Form，是一種型別提示
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request, #渲染模板的字典裡必須要有 request，模板才能正確接收 request 的資料並運作
            "title": "Homepage",
            "user_status": "歡迎光臨，請輸入帳號密碼"
        }
    )
    
@app.post("/signin")
async def verify(
    username: Annotated[str, Form()], #username 的型別提示為 Form
    password: Annotated[str, Form()],
    request: Request):
    
    #檢查是否為空值
    if not username or not password:
        return RedirectResponse("/error?message=請輸入帳號和密碼", status_code = 303)
        #導向至 /error 並帶上 message 參數
        #status_code 303 是為了要將 POST 方法在此改為 GET 方法，否則 request & response 會沿用裝飾器最初設定的方法。
    
    #檢查帳號密碼是否正確
    if username == "test" and password == "test":
        request.session["user"] = username #將 username 傳入 session 中名為 user（自定義） 的 key 
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
    message = request.query_params.get("message") #提取 message 參數
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

#Task 4 其實要把前後端做的事情分開來看，後端設置動態路由、計算結果，而前端要想辦法將 request 提交到動態路由
#前端預設的 request 會以 quert string 發送，比如 /square?number=5，但這樣並不會進到 /{number} 這個 path 中
#HTML request 是無法對 path 做任何更動的，除非使用 JS 中的 window.location.href = "target url" 直接指定 url

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