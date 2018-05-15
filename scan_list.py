#__*__ encoding:utf-8
import requests
import bs4
import sqlite3
from copy import deepcopy

list_url = 'https://etherscan.io/contractsVerified/%d'
code_url = 'https://etherscan.io/address/%s'
db_file = 'contract.db'


def scan_list():
    for i in range(1040, 1044):
        print('page', i)
        url = list_url % i
        while True:
            try:
                resp = requests.get(url, verify = False)
                break
            except:
                time.sleep(30)
            
        html = resp.content.decode('utf-8')
        contracts = get_ctrs(html)
        save_ctrs(contracts)

def get_ctrs(html):
    contracts = []
    html = bs4.BeautifulSoup(html, 'html')
    table = html.find(name='table', attrs={'class':'table table-hover '})
    trs = table.find_all(name='tr')[1:]
    for tr in trs:
        ctr = [td.text.strip(' ') for td in tr.find_all(name='td')]
        ctr[3] = float(ctr[3].replace(' Ether', '').replace(',', '')) if 'Ether' in ctr[3] else ctr[3]
        contracts.append(deepcopy(ctr))
    return contracts

def save_ctrs(contracts):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    for ctr in contracts:
        if is_exist(cur, ctr):
            update(cur, ctr)
        else:
            insert(cur, ctr)
        conn.commit()
    cur.close()
    conn.commit()
    conn.close()
    
def is_exist(cur, ctr):
    sql = 'select count(id) from list where address = ?'
    cur.execute(sql, (ctr[0],))
    values = cur.fetchone()
    if values[0] > 0:
        return True
    return False

def update(cur, ctr):
    sql = 'update list set balance=?,txcount=? where address=?'
    cur.execute(sql, (ctr[3], ctr[4], ctr[0]))
    
def insert(cur, ctr):
    sql = 'insert into list (address, name, compiler, balance, txcount, date_verified) values (?, ?, ?, ?, ?, ?)'
    cur.execute(sql, (ctr[0], ctr[1], ctr[2], ctr[3], ctr[4], ctr[6]))
    

if __name__ == '__main__':
    
    scan_list()




