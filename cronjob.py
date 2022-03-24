import requests, os, datetime, time, sys
import mysql.connector
USER = os.getenv("DB_USERNAME")
PW = os.getenv("DB_PW")
NAME = os.getenv("DB_NAME")
HOST = os.getenv("DB_HOST")

conn = mysql.connector.connect(user=USER, password=PW, host=HOST, database=NAME)

def sendEveryoneEmails():
    print("--SENDING EVERYONE EMAILS--", time.time(), os.getpid())
    cursor = conn.cursor()
    query = ("SELECT * FROM tbl_user;")
    cursor.execute(query)

    for u in cursor:
        time.sleep(3)
        id, fn, ln, netid, choice = u
        if choice == "weekday" and datetime.date.today().weekday() < 5:
            sendMail(fn, ln, netid)
        else:
            sendMail(fn, ln, netid)

    cursor.close()

def sendLeoEmail():
    print("--SENDING LEO EMAIL--", time.time(), os.getpid())
    cursor = conn.cursor()
    query = ("SELECT * FROM tbl_user;")
    cursor.execute(query)

    for u in cursor:
        print(u)
        id, fn, ln, netid, choice = u
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
