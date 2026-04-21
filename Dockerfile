FROM python:3.11

# apt-get의 version을 갱신하고, SQLite3의 설치
RUN apt-get update && apt-get install -y sqlite3 && apt-get install -y libsqlite3-dev

# 컨테이너의 워킹 디렉터리의 지정
WORKDIR /usr/src/
# 디렉터리와 파일의 복사
COPY ./apps /usr/src/apps
COPY ./local.sqlite /usr/src/local.sqlite
COPY ./requirements.txt /usr/src/requirements.txt
COPY ./flaskbook_api/model.pt /usr/src/model.pt

# pip의 version 갱신
RUN pip install --upgrade pip

# 리눅스용 Pytorch 설치 명령어를 실행
RUN pip install torch torchvision opencv-python

# 필요한 라이브러리를 컨테이너 내의 환경에 설치
RUN pip install -r requirements.txt

# "building..."을 표시하는 처리
RUN echo "building..."

# 필요한 각 환경 변수를 설정
ENV FLASK_APP "apps.app:create_app('local')"
ENV IMAGE_URL "/storage/images/"

# 특정 네트워크 포트를 컨테이너가 실행 시에 리슨
EXPOSE 5000

# "docker run" 실행 시에 실행되는 처리
CMD ["flask", "run", "-h", "0.0.0.0"]