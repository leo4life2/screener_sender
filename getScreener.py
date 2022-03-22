import requests


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('netid')
parser.add_argument('fn')
parser.add_argument('ln')
args = parser.parse_args()

headers = {
    'authority': 'nyushc.iad1.qualtrics.com',
    'upgrade-insecure-requests': '1',
    'referer': 'https://nyu.qualtrics.com/',
}

response = requests.get(f"https://nyushc.iad1.qualtrics.com/jfe/form/SV_515wVHTcq6PLe5w?p_fn={args.fn}&p_ln={args.ln}&n_em={args.netid}@nyu.edu&is_vax=Y&last_screener=&p_afl=student", headers=headers)
