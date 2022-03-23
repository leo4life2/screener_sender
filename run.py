from flask import Flask, request, render_template, jsonify, make_response
from flaskext.mysql import MySQL
from apscheduler.schedulers.background import BackgroundScheduler
import requests, re, os, datetime, time

app = Flask(__name__, static_folder="build/static", template_folder="build")
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("DB_USERNAME")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DB_PW")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DB_NAME")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DB_HOST")
mysql.init_app(app)

def sendEveryoneEmails():
    print("--SENDING EVERYONE EMAILS--")
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from tbl_user;")
    allusers = cursor.fetchall()
    for u in allusers:
        id, fn, ln, netid, choice = u
        if choice == "weekday" and datetime.date.today().weekday() < 5:
            sendMail(fn, ln, netid)
        else:
            sendMail(fn, ln, netid)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/screenerPage')
def screenerPage():
    fn, ln = request.args.get('fn'), request.args.get('ln')
    fn, ln = fn.capitalize(), ln.capitalize()
    name = fn + " " + ln
    now = datetime.date.today().strftime("%d %b %Y")
    return render_template('screener.html', personName=name, todayDate=now)

def preprocessInput(fn, ln, netid):
    return fn.lower().strip(), ln.lower().strip(), netid.lower().strip()

def validateData(fn, ln, netid):
    name_regex = '[A-Za-z]{2,25}||\s[A-Za-z]{2,25}'
    netid_regex = '[A-Za-z]{2,3}[0-9]{3,4}'
    if len(netid) > 7:
        return False
    nameOk = re.findall(name_regex, fn) and re.findall(name_regex, ln)
    netidOk = re.findall(netid_regex, netid)
    return bool(nameOk and netidOk)

@app.route('/getOne', methods=['GET'])
def getOneEmail():
    fn, ln, netid = request.args.get('fn'), request.args.get('ln'), request.args.get('netid')
    fn, ln, netid = preprocessInput(fn, ln, netid)
    if not validateData(fn, ln, netid):
        return "Illegal input. Please check your inputs."

    print("getOne", fn, ln, netid)

    sendMail(fn, ln, netid)
    return "OK"

@app.route('/subscribe', methods=['GET'])
def subscribe():
    fn, ln, netid, choice = request.args.get('fn'), request.args.get('ln'), request.args.get('netid'), request.args.get('choice')
    fn, ln, netid = preprocessInput(fn, ln, netid)

    print("subscribe1", fn, ln, netid, choice)

    if not validateData(fn, ln, netid):
        response = make_response(
            jsonify(
                {"message": "Illegal input. Please check your inputs."}
            ),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response

    if choice not in ["day", "weekday"]:
        response = make_response(
            jsonify(
                {"message": "You did not choose a day."}
            ),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response

    print("subscribe", fn, ln, netid, choice)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(f"select * from tbl_user where user_netid = \"{netid}\"")
    data = cursor.fetchall()
    if len(data) > 0:
        response = make_response(
            jsonify(
                {"message": "This Net ID has already subscribed to the service."}
            ),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    try:
        sendMail(fn, ln, netid)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"insert into tbl_user(user_fn, user_ln, user_netid, mail_freq) values (\"{fn}\", \"{ln}\", \"{netid}\", \"{choice}\");")
        conn.commit()

        response = make_response(
            jsonify(
                {"message": "Subscribe successful!"}
            ),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    except Exception as e:
        print(e)
        response = make_response(
            jsonify(
                {"message": str(e)}
            ),
            500
        )
        response.headers["Content-Type"] = "application/json"
        return response


def sendMail(fn, ln, netid):
    headers = {
        'authority': 'nyushc.iad1.qualtrics.com',
        'upgrade-insecure-requests': '1',
        'referer': 'https://nyu.qualtrics.com/',
    }
    fn = fn.capitalize()
    ln = ln.capitalize()

    response = requests.get(f"https://nyushc.iad1.qualtrics.com/jfe/form/SV_515wVHTcq6PLe5w?p_fn={fn}&p_ln={ln}&n_em={netid}@nyu.edu&is_vax=Y&last_screener=&p_afl=student", headers=headers)


sched = BackgroundScheduler(daemon=True)
sched.add_job(sendEveryoneEmails, 'cron', hour='06', minute='30')
sched.start()

if __name__ == "__main__":
    app.run()
