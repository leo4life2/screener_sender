from flask import Flask, request, render_template
import requests

app = Flask(__name__, static_folder="build/static", template_folder="build")

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/getOne', methods=['GET'])
def getOneEmail():
    fn, ln, netid = request.args.get('fn'), request.args.get('ln'), request.args.get('netid')
    print(request)
    sendMail(fn, ln, netid)
    return "Done"

def sendMail(fn, ln, netid):
    headers = {
        'authority': 'nyushc.iad1.qualtrics.com',
        'upgrade-insecure-requests': '1',
        'referer': 'https://nyu.qualtrics.com/',
    }

    response = requests.get(f"https://nyushc.iad1.qualtrics.com/jfe/form/SV_515wVHTcq6PLe5w?p_fn={fn}&p_ln={ln}&n_em={netid}@nyu.edu&is_vax=Y&last_screener=&p_afl=student", headers=headers)

if __name__ == "__main__":
  app.run()
