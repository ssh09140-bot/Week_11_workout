from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(BASE_DIR, 'project_data.json')

def load_project_data():
    """
    project_data.json 파일을 읽어서 파이썬 딕셔너리(dict)로 반환하는 함수
    """
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {"error": "데이터 파일(project_data.json)을 찾을 수 없습니다."}
    except json.JSONDecodeError:
        return {"error": "JSON 파일 형식이 올바르지 않습니다."}
    
@app.get("/api/project/all")
def get_all_data():
    """
    JSON 파일에 있는 *모든* 데이터를 반환합니다.
    """
    data = load_project_data()
    return jsonify(data)

@app.get("/api/<string:page_name>")
def get_page_data(page_name):
    """
    요청된 <page_name>에 해당하는 데이터를 JSON 파일에서 찾아 반환합니다.
    예: /api/team -> project_data.json의 "team" 키에 해당하는 값 반환
        /api/features -> project_data.json의 "features" 키에 해당하는 값 반환
    """
    print(f"요청 받은 페이지 키: {page_name}") # (디버깅용 로그)
    data = load_project_data()

    # 1. 파일 로드 시 에러가 있었는지 확인
    if 'error' in data:
        return jsonify(data), 500 # 서버 내부 오류 (파일 없음)

    # 2. 요청된 page_name이 JSON 데이터의 키(key)로 존재하는지 확인
    if page_name in data:
        # 3. 키가 존재하면, 해당 키의 값(value)을 JSON으로 반환
        return jsonify(data[page_name])
    else:
        # 4. 키가 존재하지 않으면, 404 Not Found 에러 반환
        return jsonify({"error": f"'{page_name}'에 해당하는 데이터를 찾을 수 없습니다."}), 404

@app.get("/")
def main_page():
    """ 메인 페이지 (index.html)를 렌더링합니다. """
    data = load_project_data()
    # 'main' 키의 값(객체)을 'data' 변수로 전달합니다.
    return render_template('index.html', data=data.get('main', {}))

@app.get("/team")
def team_page():
    """ 팀 구성 및 역할 페이지 (team.html)를 렌더링합니다. """
    data = load_project_data()
    # 'team' 키의 값(객체)을 'data' 변수로 전달합니다. (기본값 [] -> {})
    return render_template('team.html', data=data.get('team', {}))

@app.get("/features")
def features_page():
    """ 핵심 기능 페이지 (features.html)를 렌더링합니다. """
    data = load_project_data()
    # 'features' 키의 값(객체)을 'data' 변수로 전달합니다. (기본값 [] -> {})
    return render_template('features.html', data=data.get('features', {}))

@app.get("/subject")
def subject_page():
    """ 작품주제 페이지 (subject.html)를 렌더링합니다. """
    data = load_project_data()
    # 'subject' 키의 값(객체)을 'data' 변수로 전달합니다. (기본값 [] -> {})
    return render_template('subject.html', data=data.get('subject', {}))

@app.get("/rationale")
def rationale_page():
    """ 실용적 근거 페이지 (rationale.html)를 렌더링합니다. """
    data = load_project_data()
    # 'rationale' 키의 값(객체)을 'data' 변수로 전달합니다. (기본값 [] -> {})
    return render_template('rationale.html', data=data.get('rationale', {}))

@app.get("/environment")
def environment_page():
    """ 구현 환경 페이지 (environment.html)를 렌더링합니다. """
    data = load_project_data()
    # 'environment' 키의 값(객체)을 'data' 변수로 전달합니다. (기본값 [] -> {})
    return render_template('environment.html', data=data.get('environment', {}))

@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/api/hello")
def hello():
    return jsonify({"message": "Hello from API!"})

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000)