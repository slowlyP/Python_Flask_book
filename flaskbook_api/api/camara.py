import cv2
import os
from ultralytics import YOLO

# 모델 로드 (전역 변수)
model = YOLO("yolo11n.pt")

def generate_frames(cam_id):
    # 카메라 소스 리스트
    cameras = {
        0: 0,
        1: r"rtsp://admin:Mbc320!!@192.168.0.48:554/stream_ch0",
        2: r"rtsp://admin:Mbc320!!@192.168.0.38:554/stream_ch0",
        3: r"rtsp://admin:Mbc320!!@192.168.0.43:554/stream_ch0"
    }
    
    source = cameras.get(cam_id)
    if source is None:
        return

    # [수정 핵심] 일단 카메라 객체(cap)부터 먼저 생성합니다!
    if cam_id != 0:
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
        cap = cv2.VideoCapture(source) 
    else:
        # 웹캠(0번)인 경우
        cap = cv2.VideoCapture(source)
        # 생성된 후에 설정을 적용해야 에러가 안 납니다.
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG')) 
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)

    # 연결 확인 루프
    if not cap.isOpened():
        print(f"⚠️ 카메라 {cam_id} ({source}) 연결 실패")
        return

    count = 0 
    detect_interval = 10 # 4개 동시 구동을 위해 인터벌을 조금 더 늘림
    annotated_frame = None
    
    try:
        while True:
            success, frame = cap.read()
            if not success:
                # 연결이 일시적으로 끊겼을 때 재시도 로직이 없으면 break
                break
            
            count += 1
            if count % detect_interval == 0:
                results = model(frame, verbose=False)
                annotated_frame = results[0].plot()
                count = 0 

                for result in results:
                    if len(result.boxes) > 0: # 감지된 물체가 있을 때만 출력
                        # 감지된 클래스 번호를 이름(person, car 등)으로 변환
                        detected_names = [result.names[int(cls)] for cls in result.boxes.cls]
                        print(f"[{cam_id}번 카메라] 감지 결과: {', '.join(detected_names)}")
            
            display_frame = annotated_frame if annotated_frame is not None else frame
            ret, buffer = cv2.imencode('.jpg', display_frame)
            if not ret:
                continue
                
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    finally:
        # [중요] 프로세스 종료 시 자원 해제를 확실히 하여 'terminate' 에러 방지
        cap.release()