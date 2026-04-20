# logging를 import한다
import logging

import os



from dotenv import load_dotenv

from email_validator import validate_email, EmailNotValidError
from flask import (
                Flask,
                current_app,
                render_template,
                url_for,
                request,
                redirect,
                g,
                flash,
                make_response,
                session,
            )

from flask_debugtoolbar import DebugToolbarExtension


from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBs"




# Mail 클래스의 config를 추가한다
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "True") == "True"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 확장을 등록한다
mail = Mail(app)





#로그 레벨을 설정한다
app.logging.setLevel(logging,DEBUG)

# 리다이렉트를 중단하지 않도록 한다
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# DebugToolbarExtension에 애플리케이션을 설정한다
toolbar = DebugToolbarExtension(app)





@app.route("/", endpoint="endpoint-name")
def index():
    return "Hello, Flaskbook!"

@app.route("/hello/<name>",
    methods=["GET", "POST"],
    endpoint="hello-endpoint")
def hello(name):
    # Python 3.6 부터 도입된  f-string 으로 문자열을 정의
    return f"Hello, {name}!"

# flask 2 부터는 @app.get("/hello"), @app.post("/hello")라고 기술하는것이 가능
# @app.get("/hello")
# @app.post("/hello")
# def hello():
#   return "Hello, World!"


@app.route("/name/<name>")
def show_name(name):
    # 변수를 템플릿 엔진에게 전달
    return render_template("index.html", name=name)


with app.test_request_context("/users?updated=true"):
    # true가 출력됨
    print(request.args.get("updated"))
    # /
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/AK?page=1
    print(url_for("show_name", name="AK", page="1"))

@app.route("/contact")
def contact():
    # 응답 객체를 가져온다. p84 추가
    response = make_response(render_template("contact.html"))

    # 쿠키를 설정한다.
    response.set_cookie("flaskbook key", "flaskbook value")

    # 세션을 설정한다.
    session["username"] = "AK"

    # 응답 객체를 반환한다.
    return response


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 이메일을 보낸다
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )

        #  입력 체크
        is_valid = True
        
        if not username:
            flash("사용자명은 필수입니다")
            is_valid = False
        
        if not email:
            flash("이메일 주소는 필수입니다 ")
            is_valid = False
        
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해 주세요")
            is_valid = False

        if not description:
            flash("문의 내용은 필수입니다")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        
        # 이메일을 보낸다( 나중에 구현할 부분 )

        # contact 엔드포인트로 리다이렉트한다
        flash("문의해 주셔서 감사합니다.")





        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    """메일을 송신하는 함수"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)



    