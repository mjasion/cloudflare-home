import json
import warnings
import logging

import requests

import config


CLOUDFLARE_API_URL = 'https://www.cloudflare.com/api_json.html'


def get_ip():
    ip = requests.get('https://nettool.herokuapp.com/ip').text
    logging.info('My ip is ' + ip)
    return ip

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
            logging.info(config.home_domain + ' ip is ' + record['content'])
            return record

def update_record_if_changed(rec, ip):
    if (ip_changed(rec, ip)):
        logging.info('Changing DNS record')
        edit(rec, ip)
    else:
        logging.info('DNS record not changed')

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
        'ttl': 300
    }
    request = requests.post(CLOUDFLARE_API_URL, data)


def configure_loggers():
    warnings.filterwarnings("ignore")
    logging.basicConfig(filename='cloudflare-update.log', level=logging.INFO, format='%(asctime)s |  %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)


def main():
    configure_loggers()
    logging.info('Starting')
    ip = get_ip()
    rec = get_rec(config.home_domain)
    update_record_if_changed(rec, ip)
    logging.info('Finished')


if __name__ == "__main__":
    try:
        main()
    except:
        logging.exception('Got exception')
        raise
