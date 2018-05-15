# -*- coding:utf-8
import requests
import bs4
import sqlite3
from copy import deepcopy
# import HTMLParser
import os
import sys
import time

#file_name = '%s_%s' % (contract_name, address)
list_url = 'https://etherscan.io/contractsVerified/%d'
code_url = 'https://etherscan.io/address/%s'
db_file = 'contract.db'


def get_addrs():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    sql = 'select address, name from list'
    cur.execute(sql)
    res = cur.fetchall()
    
    cur.close()
    conn.commit()
    conn.close()
    return res
    
def dump(url, file_name):
    resp = requests.get(url, verify=False)
    html = resp.content.decode('utf-8')
    html = bs4.BeautifulSoup(html, 'html')
    
    code = html.find(name='pre', attrs={'class':'js-sourcecopyarea', 'id':'editor', 'style':'margin-top: 5px;'}).text
    code = code.replace('\xa0', '@')
    open('dump/%s' % file_name, 'w', encoding='utf-8').write(code)


def file_exist(file_name):
    if os.path.isfile('dump/%s' % file_name):
        return True
    return False

if __name__ == "__main__":
    addrs = get_addrs()
    for addr in addrs:
        file_name = '%s_%s.sol' % (addr[1], addr[0].split(' ')[0])
        print(file_name)
        if file_exist(file_name):
            pass
        else:
            time.sleep(1)
            url = code_url % addr[0].split(' ')[0]
            dump(url, file_name)
