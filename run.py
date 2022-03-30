from flask import Flask, request, render_template, jsonify, make_response
from flaskext.mysql import MySQL
import requests, re, os, datetime, time, logging

app = Flask(__name__, static_folder="build/static", template_folder="build")

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("DB_USERNAME")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DB_PW")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DB_NAME")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DB_HOST")
mysql.init_app(app)

localmode = False

if os.getenv("DB_USERNAME") == "root" or os.getenv("DB_USERNAME") == "":
    print("-----LOCAL DEBUG MODE------")
    localmode = True

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

    regexOk = bool(nameOk and netidOk)
    fnok = all(x.isalpha() or x == "" for x in  fn)
    lnok = all(x.isalpha() or x == "" for x in  ln)
    return regexOk and fnok and lnok

@app.route('/getOne', methods=['GET'])
def getOneEmail():
    fn, ln, netid = request.args.get('fn'), request.args.get('ln'), request.args.get('netid')
    fn, ln, netid = preprocessInput(fn, ln, netid)

    if not validateData(fn, ln, netid):
        print(f"[Get One] -Illegal Input- {fn} {ln} {netid}")
        return "Illegal input. Please check your inputs."

    print(f"[Get One] {fn} {ln} {netid}")

    sendMail(fn, ln, netid)
    return "OK"

@app.route('/subscribe', methods=['GET'])
def subscribe():
    fn, ln, netid, choice = request.args.get('fn'), request.args.get('ln'), request.args.get('netid'), request.args.get('choice')
    fn, ln, netid = preprocessInput(fn, ln, netid)

    print(f"[Subscribe] {fn} {ln} {netid}")

    if not validateData(fn, ln, netid):
        response = makeJsonRspWithMsg("Illegal input. Please check your inputs.", 200)
        return response

    if choice not in ["day", "weekday"]:
        response = makeJsonRspWithMsg("You did not choose a day.", 200)
        return response

    print(f"[Subscribe] -Success- {fn} {ln} {netid}")

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(f"select * from tbl_user where user_netid = \"{netid}\"")
    data = cursor.fetchall()
    if len(data) > 0:
        response = makeJsonRspWithMsg("This Net ID has already subscribed to the service.", 200)
        return response
    try:
        sendMail(fn, ln, netid)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"insert into tbl_user(user_fn, user_ln, user_netid, mail_freq) values (\"{fn}\", \"{ln}\", \"{netid}\", \"{choice}\");")
        conn.commit()

        response = makeJsonRspWithMsg("Subscribe successful!", 200)
        return response
    except Exception as e:
        print(f"[Subscribe] -Fail- {fn} {ln} {netid}")
        response = makeJsonRspWithMsg(str(e), 500)
        return response

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    fn, ln, netid = request.args.get('fn'), request.args.get('ln'), request.args.get('netid')
    fn, ln, netid = preprocessInput(fn, ln, netid)

    print(f"[Unsubscribe] {fn} {ln} {netid}")

    if not validateData(fn, ln, netid):
        response = makeJsonRspWithMsg("Illegal input. Please check your inputs.", 200)
        return response

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        selectst = f'SELECT * FROM tbl_user WHERE user_netid="{netid}" AND user_fn="{fn}" AND user_ln="{ln}"'
        cursor.execute(selectst)
        data = cursor.fetchall()
        if len(data) > 0: # User exists
            delst = f'DELETE FROM tbl_user WHERE user_netid="{netid}" AND user_fn="{fn}" AND user_ln="{ln}"'
            cursor.execute(delst)
            conn.commit()
            print(f"[Unsubscribe] -Success- {fn} {ln} {netid}")
            return makeJsonRspWithMsg("Unsubscribe successful", 200)
        return makeJsonRspWithMsg(f"No user with ID {fn.capitalize()} {ln.capitalize()} {netid} found.", 500)

    except Exception as e:
        print(f"[Unsubscribe] -Fail- {fn} {ln} {netid}")
        response = makeJsonRspWithMsg(str(e), 500)
        return response

def makeJsonRspWithMsg(msg, status):
    response = make_response(
        jsonify(
            {"message": str(msg)}
        ),
        int(status)
    )
    response.headers["Content-Type"] = "application/json"
    return response

def sendMail(fn, ln, netid):
    if localmode:
        print(f"[Send Mail] Won't send mail for local testing.")
        return
    headers = {
        'authority': 'nyushc.iad1.qualtrics.com',
        'upgrade-insecure-requests': '1',
        'referer': 'https://nyu.qualtrics.com/',
    }
    fn = fn.capitalize()
    ln = ln.capitalize()

    response = requests.get(f"https://nyushc.iad1.qualtrics.com/jfe/form/SV_515wVHTcq6PLe5w?p_fn={fn}&p_ln={ln}&n_em={netid}@nyu.edu&is_vax=Y&last_screener=&p_afl=student", headers=headers)

if __name__ == "__main__":
    app.run()
