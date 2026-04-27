# p306 추가 config 읽어들이고 플라스크 앱 만들기
import os

from flask import Flask  # p307 추가

# from flaskbook_api.api import create_app p307 수정
from flaskbook_api.api import api
from flaskbook_api.api.config import config

config_name = os.environ.get("CONFIG", "local")


app = Flask(__name__)
app.config.from_object(config[config_name])

app.register_blueprint(api, url_prefix="/api")



# [추가] Flask 서버 실행 설정
if __name__ == "__main__":
    # host='0.0.0.0'으로 설정해야 외부(브라우저)에서 접속이 가능합니다.
    app.run(host='0.0.0.0', port=5000, debug=True)