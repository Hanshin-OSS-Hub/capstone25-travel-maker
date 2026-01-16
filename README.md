
# capstone25-travel-maker
e Design (Python)

간단한 데모/프로토타입을 빠르게 만들 수 있도록 파이썬 기본 구조만 세팅해둔 상태.

## 실행 방법 (Windows PowerShell)
1) 가상환경 생성/활성화
   - `python -m venv .venv`
   - `.venv\\Scripts\\Activate.ps1`
2) 의존성 설치
   - `pip install -r requirements.txt`
3) 서버 실행
   - `python src/app/main.py`
4) 확인
   - `http://127.0.0.1:8000/health`
   - `http://127.0.0.1:8000/docs`

## 구조
- `src/app/main.py`: FastAPI 엔트리 포인트
- `requirements.txt`: 의존성 목록

## 주요 API (MVP 더미)
- `POST /analyze-url`
- `POST /optimize-route`
>>>>>>> 91cf654 (tmp: 첫 세팅)
