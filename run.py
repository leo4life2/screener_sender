from flask import Flask, request, render_template, jsonify, make_response
from flaskext.mysql import MySQL
import requests, re, os, datetime, schedule, time

app = Flask(__name__, static_folder="build/static", template_folder="build")
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("DB_USERNAME")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DB_PW")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DB_NAME")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DB_HOST")
mysql.init_app(app)

def sendEveryoneEmails():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_getAllUsers',())
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

    print(fn, ln, netid, choice)

    if not validateData(fn, ln, netid):
        return "Illegal input. Please check your inputs."

    if choice not in ["day", "weekday"]:
        return "Bad Input."

    print("subscribe", fn, ln, netid, choice)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_createUser',(fn, ln, netid, choice))
    data = cursor.fetchall()
    print("from sql: ", data)

    if len(data) == 0:
        conn.commit()
        sendMail(fn, ln, netid)
        response = make_response(
            jsonify(
                {"message": 'Subscribe Successful!'}
            ),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response(
            jsonify(
                {"message": str(data[0][0])}
            ),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response

def sendMail(fn, ln, netid):
    headers = {
        'authority': 'nyushc.iad1.qualtrics.com',
        'upgrade-insecure-requests': '1',
        'referer': 'https://nyu.qualtrics.com/',
    }

    response = requests.get(f"https://nyushc.iad1.qualtrics.com/jfe/form/SV_515wVHTcq6PLe5w?p_fn={fn}&p_ln={ln}&n_em={netid}@nyu.edu&is_vax=Y&last_screener=&p_afl=student", headers=headers)

if __name__ == "__main__":
    app.run()
    schedule.every().day.at("06:30").do(sendEveryoneEmails)
    while True:
        schedule.run_pending()
        time.sleep(1)
