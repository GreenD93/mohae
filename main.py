import time
import os, datetime
from flask import Flask, render_template, jsonify, make_response, request, send_file, send_from_directory

from mohae import mail_send, mohae_sql
from mohae.web_utils import get_main_source, get_project_source

app = Flask(__name__)

# 메인 페이지 이동
@app.route('/')
def main():
    mainitems = get_main_source()
    project_list = get_project_source()
    return render_template('main.html', items=mainitems, project_list=project_list)


# 프로젝트 클릭 시 상세 이미지 조회
@app.route('/project_description')
def project_description():

    project_list = get_project_source()

    screen = 'project_description'

    # 선택된 프로젝트 내 이미지 가져오기
    project_name = request.args.get('project_name')
    project_name = project_name.replace(' ', '_')
    path = f"./static/assets/img/project/{project_name}"

    file_list = os.listdir(path)
    file_list = [ file_nm for file_nm in file_list if file_nm.endswith('.jpg') or file_nm.endswith('.png')]

    response = {}
    items = []

    for img_nm in file_list:
        imgs = path + '/' + img_nm
        item = {
            "imgs": imgs
        }
        items.append(item)

    response['items'] = items
    response = jsonify(response)
    make_response(response, 200)
    return render_template('project_description.html', items=items, project_name=project_name, screen=screen, project_list=project_list)


# 로그인 페이지 이동 / 관리자 페이지 이동 및 데이터 조회
@app.route('/admin', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        data = request.form
        today = datetime.date.today()
        if len(data) == 0:
            data = {
                "name": '%',
                "regdate_from": '1990-01-01',
                "regdate_to": today,
                "page": 0
            }

        cons_list = mohae_sql.select_data(data)
        if len(cons_list) == 0:
            page_cnt = 0
        else:
            page_cnt = int(cons_list[0][-1])
        return render_template('admin.html', cons_list=cons_list, page_cnt=page_cnt)


# 로그인 데이터 확인
@app.route('/login', methods=['POST'])
def admin_page():
    data = request.form
    chk = mohae_sql.login(data)
    response = {}
    if (chk[0] == 0):
        response['login_result'] = 'fail'
    else:
        response['login_result'] = 'success'
    response = jsonify(response)
    return make_response(response, 200)


#업로드한 파일 다운로드
@app.route('/file_download', methods=['POST'])
def file_download():
    data = request.form
    print(data)
    file_path = mohae_sql.getfilepath(data)
    print(file_path)
    response = jsonify(file_path)
    print(response)

    return make_response(response, 200)


# 견적문의 화면으로 이동
@app.route('/consultant')
def consultant():
    screen = 'consultant'
    project_list = get_project_source() # 전체 프로젝트 리스트 가져오기
    return render_template('consultant.html', screen=screen, project_list=project_list)


@app.route('/submit-consultant', methods=['POST'])
def submitconsultant():
    # 견적문의 제출은 POST 호출
    if request.method == 'POST':

        result = request.form
        file = request.files.getlist("file")

        save_list = []
        # 파일 업로드를 한 경우에만 file 테이블에 insert
        if file[0].filename != '':
            file_seq = ""
            for item in file:
                now = datetime.datetime.now()
                nowStr = "{:%Y%m%d%H%M%S}".format(now)
                sys_file_name = item.filename + nowStr

                file_save = './static/assets/img/uploads/' + item.filename + nowStr
                save_list.append(file_save)
                item.save(file_save)  # 파일 실제 위치(uploads) 저장
                file_seq += str(mohae_sql.insert_attach_file(item, sys_file_name)) + ','  # 첨부 테이블 입서트 후 시퀀스 가져오기
        else:
            # 업로드 파일이 없는 경우 '-'값 입력
            file_seq = "--"

        mohae_sql.insert_data(result, file_seq[:-1])  # DB 저장
        mail_send.sendmail(result, save_list)  # 메일 전송
        return render_template('main.html')


if __name__ == '__main__':
    app.run(host='172.30.1.15', debug=True, port=5000)
