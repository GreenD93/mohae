import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


code_name = {
    "name":"성함"
    , "phone":"연락처"
    , "email":"E-mail"
    , "building_type":"건물 유형"
    , "width":"평수"
    , "work_date":"공사 예정일"
    , "movein_Date":"입주 예정일"
    , "category":"구분"
    , "budget":"예산"
    , "floor_type":"바닥 공사"
    , "bathroom_category":"욕실공사"
    , "facility_category":"설비공사"
    , "facility_category_etc":"설비공사_기타"
    , "expand_type":"확장"
    , "expand_type_etc":"확장_기타"
    , "sash_type":"샷시"
    , "sash_type_etc":"샷시_기타"
    , "message":"기타 문의"
    , "blueprint":"도면 및 현장 사진"
    , "hid_address":"주소"
}

mail_frame_front = """
        <html>
        <body>
            <table class="type03" style="border-collapse: collapse; text-align: left; line-height: 1.5; border-top: 1px solid #ccc; border-left: 3px solid #369; margin : 20px 10px;">
"""
mail_frame_end = """
            </table>
        </body>
        </html>
"""
mail_td_front = """
    <tr style="   width: 147px; padding: 10px; font-weight: bold; vertical-align: middle; color: #153d73; border-right: 1px solid #ccc; border-bottom: 1px solid #ccc;">
        <th scope="row" style="100px">
"""
mail_td_middle = """
        </th>
        <td style="  width: 349px; padding: 10px; vertical-align: top; border-right: 1px solid #ccc; border-bottom: 1px solid #ccc;">
"""
mail_td_end = """
        </td>
    </tr>
"""

def sendmail(data, fileList):
    recipients = ["gksdlf147@naver.com"]

    message = MIMEMultipart()
    message['Subject'] = data["name"] + " 고객 견적 문의 (연락처 : " + data["phone"] + ")"
    message['From'] = "mohaedesign@naver.com"
    message['To'] = ",".join(recipients)

    # 첨부파일 추가
    if len(fileList) != 0:
        for item in fileList:
            etcFileName = item
            with open(etcFileName, 'rb') as etcFD:
                etcPart = MIMEApplication(etcFD.read())
                # 첨부파일의 정보를 헤더로 추가
                etcPart.add_header('Content-Disposition', 'attachment', filename=etcFileName[28:-14])
                message.attach(etcPart)

    mail_text = ""

    for key in data:
        if "etc" in key:
            continue
        value = data.getlist(key)
        if "기타" in value[-1]:
            etcKey = key+"_etc"
            etcText = value.pop() + " : " + "".join(data[etcKey])
            mail_text += mail_td_front + code_name[key] + mail_td_middle + ", ".join(value) + etcText + mail_td_end
            continue
        mail_text += mail_td_front + code_name[key] + mail_td_middle + ", ".join(value) + mail_td_end
        content = (mail_frame_front+mail_text+mail_frame_end)

    mimetext = MIMEText(content, 'html')
    message.attach(mimetext)

    email_id = 'mohaedesign@naver.com'
    email_pw = 'mohae2022!!'

    server = smtplib.SMTP('smtp.naver.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_id, email_pw)
    server.sendmail(message['From'], recipients, message.as_string())
    server.quit()
