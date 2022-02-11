# applyhome

## Python 명령어
### 여러버전의 Python이 설치되어 있는 경우
```bash
$ py -3.8 -m pip install {packagename}
```

### 가상환경에서 개발
```bash
$ py -3.8 -m venv .venv
$ . .venv/Scripts/activate
(.venv)
```

### Python requirements.txt 파일로 install
```bash
$ pip install -r requirements.txt
```

### Python requirements.txt 파일로 설치된 모듈 저장
```bash
$ pip freeze > requirements.txt
```

### 실행
```bash
python applyhome.py
(.venv)
```
