import pymysql

from config.account import *



conn = pymysql.connect(host=HOST,
                       port=PORT,
                       user=USER,
                       password=PASSWORD,
                       db = DB,
                       charset=CHARSET)
cursor = conn.cursor()

form = ['name',
        'phone',
        'email',
        'building_type',
        'hid_address',
        'width',
        'work_date',
        'movein_Date',
        'category',
        'budget',
        'floor_type',
        'floor_type_etc',
        'bathroom_category',
        'facility_category',
        'facility_category_etc',
        'expand_type',
        'expand_type_etc',
        'sash_type',
        'sash_type_etc',
        'message']

result = {}


def insert_data(data, file_seq):

    result["file_seq"] = file_seq
    for i in form:
        if (i in data.keys()):
            if data[i] == "" or data[i] == None:
                result[i] = "-"
            else:
                result[i] = data[i]
        else:
            result[i] = '-'

    query = f"""
        INSERT INTO tb_consultant (name,phone,email,building_type,width,work_date,movein_Date,category,budget,floor_type,floor_type_etc,bathroom_category,facility_category,facility_category_etc,expand_type,expand_type_etc,sash_type,sash_type_etc,message,blueprint,address, regdate)
        VALUES (\'{result['name']}\', \'{result['phone']}\', \'{result['email']}\', \'{result['building_type']}\', \'{result['width']}\', \'{result['work_date']}\', \'{result['movein_Date']}\', \'{result['category']}\', \'{result['budget']}\', \'{result['floor_type']}\', \'{result['floor_type_etc']}\', \'{result['bathroom_category']}\', \'{result['facility_category']}\', \'{result['facility_category_etc']}\', \'{result['expand_type']}\', \'{result['expand_type_etc']}\', \'{result['sash_type']}\', \'{result['sash_type_etc']}\', \'{result['message']}\', \'{result['file_seq']}\', \'{result['hid_address']}\', SYSDATE())
    """
    print(query)
    # 3. 커서를 통해 SQL문들을 전달한다.
    cursor.execute(query)
    conn.commit()


def insert_attach_file(file, sys_file_name):

    file_name = file.filename
    file_path = './static/assets/img/uploads/'
    file_size = file.__sizeof__()
    sys_file_name = sys_file_name

    query = """
        INSERT INTO tb_file_info (sys_file_name, file_name, file_path, file_size, regdate)
        VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', SYSDATE())
    """.format(sys_file_name, file_name, file_path, file_size)

    # 3. 커서를 통해 SQL문들을 전달한다.
    cursor.execute(query)
    conn.commit()
    return cursor.lastrowid


def login(data):

    query = f"""
        SELECT  COUNT(USER_ID)
        FROM    TB_USER_INFO
        WHERE   USER_ID = \'{data['user_id']}\'
        AND     USER_PW = \'{data['user_pw']}\'
    """
    print(query)
    cursor.execute(query)
    chk = cursor.fetchone()

    return chk

def select_data(data):

    query = f"""
        SELECT  row_number() over(order by regdate desc) as rownum
				,A.name
				,A.phone
				,A.email
				,A.address
				,A.building_type
				,A.width
				,A.work_date
				,A.movein_Date
				,A.category
				,A.budget
				,A.floor_type
				,A.floor_type_etc
				,A.bathroom_category
				,A.facility_category
				,A.facility_category_etc
				,A.expand_type
				,A.expand_type_etc
				,A.sash_type
				,A.sash_type_etc
				,A.message
				,CASE
				    WHEN A.blueprint = '-' THEN 'N'
				    ELSE 'Y'
				END blueprint
				,A.regdate
                ,A.blueprint
                ,(  SELECT ROUND(COUNT(*)/10)
                    FROM    TB_CONSULTANT
                    WHERE   NAME LIKE \'{data['name']}\'
                    AND     REGDATE >= \'{data['regdate_from']}\'
                    AND     REGDATE <= \'{data['regdate_to']}\') as max_page
        FROM    TB_CONSULTANT A
        WHERE   NAME LIKE \'{data['name']}\'
        AND     REGDATE >= \'{data['regdate_from']}\'
        AND     REGDATE <= \'{data['regdate_to']}\'
        LIMIT 	10
        OFFSET 	{data['page']}
    """
    cursor.execute(query)
    cons_list = cursor.fetchall()

    return cons_list


def getfilepath(file_seq) :
    query ="""
        SELECT  CONCAT(file_path, sys_file_name)
        FROM    tb_file_info
        WHERE   SEQ IN ({0})
    """.format(file_seq['file_seq'])

    cursor.execute(query)
    cons_list = cursor.fetchall()

    return cons_list
