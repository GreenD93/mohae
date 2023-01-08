import os

# 메인 이미지 6개 및 해당 프로젝트 이름 가져오기
def get_main_source():

    path = "./static/assets/img/project_main"
    file_list = os.listdir(path)

    response = {}
    items = []

    for img_nm in file_list:
        # 이미지 경로 생성
        img_path = path+"/"+ img_nm

        # 프로젝트명 찾기
        remove_type = img_nm.split('.')
        project_name = remove_type[0][2:].replace('_', ' ')

        item = {
            "imgs": img_path,
            "project_name" : project_name
        }
        items.append(item)

    return items


# 전체 프로젝트 리스트 가져오기
def get_project_source():

    path = "./static/assets/img/project"
    file_list = os.listdir(path)

    project_list = []
    for project_nm in file_list:
        project_nm = project_nm.replace('_', ' ')
        item = {
            "project_name" : project_nm
        }
        project_list.append(item)

    return project_list
