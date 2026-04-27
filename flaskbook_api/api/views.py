from flask import render_template, Blueprint, Response # <--- Response를 추가해야 합니다!
from flaskbook_api.api.camara import generate_frames

# api라는 이름의 블루프린트가 정의되어 있다고 가정합니다.
@api.route('/')
def index():
    return render_template('index.html')

@api.route('/video_feed/<int:cam_id>')
def video_feed(cam_id):
    # 이제 Response가 정상적으로 임포트되어 에러 없이 작동합니다.
    return Response(
        generate_frames(cam_id), 
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )