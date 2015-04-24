#! python3
# -*- coding: utf-8 -*-
from flask.ext.script import Manager
import requests
from datetime import datetime

from ghiro import app
from ghiro.database import engine

manager = Manager(app)


@manager.command
@manager.option('-c', '--config', required=False, help='config file')
def runserver(config=None):
    app.run()


@manager.command
def import_pastafarian():
    """Imports the data from followers of the Pastafarian Church, in MongoDB"""
    import re

    URL = "http://registro.chiesapastafarianaitaliana.it/map.php"
    print('Requesting url %s..' % URL)
    content = requests.get(URL).text

    # All except the last one
    print('Scraping data from page...')
    followers = [{'nickname': each.split('\n')[2].split('"')[1:each.split('\n')[2].index('"')][0].strip(),
                  'lat': each.split('\n')[3].split('=')[1].strip(';').strip(),
                  'lon': each.split('\n')[4].split('=')[1].strip(';').strip()}
                 for each in re.findall(r'\{ label: nickname \}.*\n.*\n.*\n.*\n.*\n', content)[:-1]]
    rec = {
        '_id': datetime.today().strftime('%Y%m%d'),
        'followers': followers
    }
    print('Saving to Mongo...')
    db = engine.pastafarian
    db.followers.save(rec)
    print('Done.')


@manager.command
def import_discogs_sxm():

    from bs4 import BeautifulSoup

    URL = "http://www.discogs.com/Sangue-Misto-SXM/release/1483648"
    print('Requesting url %s..' % URL)
    content = requests.get(URL, headers={
                           'User-Agent': 'Mozilla/5.0 (Android; Mobile; rv:30.0) Gecko/30.0 Firefox/30.0'}).text
    soup = BeautifulSoup(content)

    condition = {
        '_id': 1483648,
        'title': 'SXM',
        'author': 'Sangue Misto'
    }

    print('Saving to Mongo...')
    db = engine.discogs
    db.releases.update(condition, {'$set': {'quotation.' + datetime.today().strftime(
        '%Y%m%d') + '.price': soup.find('span', {'class': 'price'}).text}}, upsert=True)
    print('Done.')


@manager.command
def update_weblogs():
    """Analyze weblogs for things, then put them in MongoDB."""
    from glob import glob
    from collections import Counter
    from dateutil.parser import parse
    import ipaddress

    SITE_NAME = 'ghiro.beatmatic.it'
    LOGS_DIR = 'logs/*.log'

    db = engine.ghiro
    rec = db.weblogs_analitics.find_one({'_id': SITE_NAME})

    if rec:
        retcode_count = Counter(rec.get('retcodes'))
        ip_count = Counter(rec.get('ips'))
        errors = rec.get('errors', [])
    else:
        rec = {'_id': SITE_NAME}
        retcode_count, ip_count, errors = Counter(), Counter(), []

    skipped_error, skipped_old = 0, 0
    i = 0
    for fn in glob(LOGS_DIR):
        print("Analyzing %s" % fn)
        with open(fn, 'r') as f:
            try:
                for line in f:
                    try:
                        # Try to parse timestamp field
                        ts = parse(
                            ("%s %s" % (line.split()[3], line.split()[4])).replace(':', ' ', 1)[1:-1])
                        #import pdb
                        # pdb.set_trace()
                        if not rec.get('last_timestamp') or ts > parse(rec.get('last_timestamp')):
                            rec['last_timestamp'] = ts.isoformat()
                            # count http return codes
                            try:
                                code = int(line.split()[8])
                                retcode_count[str(code)] += 1
                                if code >= 400:
                                    errors.append(line)
                            except ValueError:
                                errors.append(line)
                            # count ip occurrencies
                            ip_count[
                                str(int(ipaddress.ip_address(line.split()[0])))] += 1
                        else:
                            skipped_old += 1

                    except ValueError:
                        skipped_error += 1
                    except IndexError:
                        skipped_error += 1

            except UnicodeDecodeError:
                skipped_error += 1
        i += 1
        if i > 3 and False:
            break

    rec['ips'] = dict(ip_count)
    rec['retcodes'] = dict(retcode_count)
    rec['errors'] = errors

    print("Skipped %s lines." % skipped_error)
    print("Skipped %s old lines." % skipped_old)
    print('Saving to db..')
    db.weblogs_analitics.save(rec)


if __name__ == "__main__":
    manager.run()
