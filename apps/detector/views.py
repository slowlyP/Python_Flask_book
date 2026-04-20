from apps.app import db
from apps.crud.models import User
from apps.detector.models import UserImage
from flask import Blueprint, render_template


# template_folder를 지정한다(static는 지정하 지않는다)
dt = Blueprint("detector", __name__, template_folder="templates")


# dt 애플리케이션을 사용하여 엔드포인트를 작성한다
@dt.route("/")
def index():
    # User와 UserImage를 Join 해서 이미지 일람을 취득한다
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )
    return render_template("detector/index.html", user_images=user_images)
