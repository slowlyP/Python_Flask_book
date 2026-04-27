from flask import Flask, Blueprint, jsonify, request, Response, render_template # render_template 추가
from flaskbook_api.api import calculation
from flaskbook_api.api.camara import generate_frames
from flaskbook_api.api.config import config 

# Blueprint 정의 (template_folder를 명시해야 html을 찾을 수 있습니다)
api = Blueprint("api", __name__, template_folder="templates")

@api.get("/")
def index():
    # [수정] 기존 jsonify 부분을 주석 처리하거나 지우고 HTML을 리턴합니다.
    # return jsonify({"column": "value"}), 201
    return render_template("index.html")

# 실시간 영상 스트리밍 엔드포인트
@api.get("/video_feed")
@api.get("/video_feed/<int:cam_id>")  # 숫자가 들어오는 주소도 허용!
def video_feed(cam_id=1):            # 기본값으로 1번 카메라 설정
    return Response(
        generate_frames(cam_id),      # camara.py에 cam_id 전달
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
    

@api.post("/detect")
def detection():
    return calculation.detection(request)