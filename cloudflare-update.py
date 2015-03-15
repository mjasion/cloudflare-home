import json
import warnings

import requests

import config


warnings.filterwarnings("ignore")

CLOUDFLARE_API_URL = 'https://www.cloudflare.com/api_json.html'

def get_ip():
    return requests.get('https://nettool.herokuapp.com/ip').text

def get_rec(domain):
    data = {
        'a': 'rec_load_all',
        'tkn': config.apiKey,
        'email': config.email,
        'z': config.zone_domain
    }
    records = json.loads(requests.post(CLOUDFLARE_API_URL, data).text)['response']['recs']['objs']
    for record in records:
        if (record['name'] == domain):
            return record

def update_record_if_changed(rec, ip):
    if(ip_changed(rec, ip)):
        print 'Changing DNS record'
        edit(rec, ip)
    else:
        print 'DNS record not changed'

def ip_changed(rec, ip):
    return rec['content'] != ip

def edit(rec, ip):
    data = {
        'a': 'rec_edit',
        'id': rec['rec_id'],
        'tkn': config.apiKey,
        'email': config.email,
        'z': config.zone_domain,
        'name': config.home_domain,
        'content': ip,
        'type': 'A',
        'service_mode': 0,
        'ttl': 120
    }
    request = requests.post(CLOUDFLARE_API_URL, data)

ip = get_ip()
print 'My ip is ' + ip
print 'Getting rec_id for ' + config.home_domain
rec = get_rec(config.home_domain)
print config.home_domain + 'record ip domain is ' + rec['content']
print config.home_domain + 'rec_id for domain is ' + rec['rec_id']
update_record_if_changed(rec, ip)
print 'Finished'