import requests, os, datetime, time
import sys
import mysql.connector
USER = os.getenv("DB_USERNAME")
PW = os.getenv("DB_PW")
NAME = os.getenv("DB_NAME")
HOST = os.getenv("DB_HOST")

conn = mysql.connector.connect(user=USER, password=PW, host=HOST, database=NAME)

def getIsSummer():
    year = datetime.date.today().year
    summer_start = datetime.date(year, 5, 20)
    summer_end = datetime.date(year, 8, 20)

    return summer_start <= datetime.date.today() <= summer_end

def sendEveryoneEmails():
    print("--SENDING EVERYONE EMAILS--", time.time(), os.getpid())
    cursor = conn.cursor()
    query = ("SELECT * FROM tbl_user;")
    cursor.execute(query)

    is_summer = getIsSummer()

    for u in cursor:
        id, fn, ln, netid, choice, send_summer = u
        send_summer = int(send_summer)

        if is_summer and not send_summer: # skip people that didnt opt in for summer.
            continue

        if choice == "weekday" and datetime.date.today().weekday() < 5: # 0 is mon, 6 is sunday
            sendMail(fn, ln, netid)
        elif choice == "day":
            sendMail(fn, ln, netid)
        elif str(datetime.date.today().weekday()) in choice: # choice could be like "01234" for weekdays
            sendMail(fn, ln, netid)

        time.sleep(2)

    cursor.close()

def sendLeoEmail():
    print("--SENDING LEO EMAIL--", time.time(), os.getpid())
    cursor = conn.cursor()
    query = ("SELECT * FROM tbl_user;")
    cursor.execute(query)

    is_summer = getIsSummer()

    for u in cursor:
        print(u)
        id, fn, ln, netid, choice, send_summer = u
        send_summer = int(send_summer)

        if is_summer and not send_summer:
            continue

        if netid == "zl3493":
            sendMail(fn, ln, netid)

    cursor.close()

def sendMail(fn, ln, netid):
    headers = {
        'authority': 'nyushc.iad1.qualtrics.com',
        'upgrade-insecure-requests': '1',
        'referer': 'https://nyu.qualtrics.com/',
    }
    fn = fn.capitalize()
    ln = ln.capitalize()

    response = requests.get(f"https://nyushc.iad1.qualtrics.com/jfe/form/SV_515wVHTcq6PLe5w?p_fn={fn}&p_ln={ln}&n_em={netid}@nyu.edu&is_vax=Y&last_screener=&p_afl=student", headers=headers)


runnow = sys.argv[1]
if runnow == "run":
    sendEveryoneEmails()
if runnow == "leo":
    sendLeoEmail()

conn.close()
