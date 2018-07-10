#!/usr/bin/python27
import os, re, sys, glob, time, random, threading, sqlite3
from urlparse import urlparse
from Queue import Queue

try:
    import requests
except ImportError:
    print '---------------------------------------------------'
    print '[*] pip install requests'
    print '   [-] you need to install requests Module'
    sys.exit()


class Dorker(object):
    def __init__(self):
        self.cls()
        try:
            os.mkdir('logs')
        except:
            pass
        try:
            os.mkdir('results')
        except:
            pass
        self.concurrent = 500
        self.r = '\033[31m'
        self.g = '\033[32m'
        self.y = '\033[33m'
        self.b = '\033[34m'
        self.m = '\033[35m'
        self.c = '\033[36m'
        self.w = '\033[37m'
        self.rr = '\033[39m'
        self.Header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0'}
        self.domains = ['ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao',
                        'aq', 'ar', 'as', 'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb',
                        'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bo',
                        'br', 'bs', 'bt', 'bv', 'bw', 'by', 'bz', 'ca', 'cc', 'cd',
                        'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr',
                        'cu', 'cv', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do',
                        'dz', 'ec', 'ee', 'eg', 'eh', 'er', 'es', 'et', 'eu', 'fi',
                        'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gb', 'gd', 'ge', 'gf',
                        'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'gs',
                        'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu',
                        'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'is', 'it',
                        'je', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn',
                        'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk',
                        'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me',
                        'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr',
                        'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc',
                        'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz',
                        'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn',
                        'pr', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru',
                        'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj',
                        'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'su', 'sv', 'sy',
                        'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm',
                        'tn', 'to', 'tp', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug',
                        'uk', 'um', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi',
                        'vn', 'vu', 'wf', 'ws', 'ye', 'yt', 'za', 'zm', 'zw', 'com',
                        'net', 'org', 'biz', 'gov', 'mil', 'edu', 'info', 'int', 'tel',
                        'name', 'aero', 'asia', 'cat', 'coop', 'jobs', 'mobi', 'museum',
                        'pro', 'travel']
        try:
            self.Get_list = raw_input(self.r + '    [+]' + self.c + ' Enter List Dork: ' + self.y)
        except IOError:
            print self.r + '--------------------------------------------'
            print self.r + '    [' + self.y + '-' + self.r + '] ' + self.c + ' List Not Found in Directory!'
            sys.exit()
        self.q = Queue(self.concurrent * 2)
        for i in range(self.concurrent):
            self.t = threading.Thread(target=self.doWork)
            self.t.daemon = True
            self.t.start()
        try:
            for url in open(self.Get_list):
                self.q.put(url.strip())
            self.q.join()
        except:
            sys.exit()

    def cls(self):
        linux = 'clear'
        windows = 'cls'
        os.system([linux, windows][os.name == 'nt'])

    def cur_execute(self, data, args=()):
        connection = sqlite3.connect("Database.sqlite3")
        with connection:
            cur = connection.cursor()
            cur.execute(data, args)
            connection.commit()

    def duplicate_remover(self, x):
        urls3 = glob.glob(x)
        domains = {}
        for line in urls3:
            with open(line, "r") as infile:
                for line1 in infile:
                    if line1.startswith("http://"):
                        line1 = line1.replace("http://", "")
                    elif line1.startswith("https://"):
                        line1 = line1.replace("https://", "")
                    else:
                        pass
                    x = 'http://' + line1
                    parse = urlparse(x)
                    domains[parse[1]] = line1
            with open('results/MyBeSqliVulnLists.txt', "a") as outfile:
                for line1 in domains:
                    outfile.write(domains[line1])
            domains.clear()
        os.unlink('results/MyBeSqliVulnList.txt')

    def doWork(self):
        try:
            while True:
                dork = self.q.get()
                for domain in self.domains:
                    next = 0
                    while next <= 500:
                        url = 'http://www.bing.com/search?q=' + dork + ' site:' + domain + '&first=' + str(
                            next) + '&FORM=PORE'
                        sess = requests.session()
                        cnn = sess.get(url, timeout=5)
                        next = next + 10
                        finder = re.findall(
                            '<h2><a href="((?:https://|http://)[a-zA-Z0-9-_]+\.*[a-zA-Z0-9][a-zA-Z0-9-_]+\.[a-zA-Z]{2,11})',
                            cnn.text)
                        for url in finder:
                            if url.startswith('http://'):
                                url = url.replace('http://', '')
                            elif url.startswith('https://'):
                                url = url.replace('https://', '')
                            else:
                                pass
                            if url.startswith('www.'):
                                url = url.replace('www.', '')
                            else:
                                pass
                            with open("logs/logs.txt", 'a') as f:
                                if 'go.microsoft.com' in url:
                                    pass
                                elif '.wordpress.' in url:
                                    pass
                                elif '.blogspot.' in url:
                                    pass
                                else:
                                    connection = sqlite3.connect("Database.sqlite3")
                                    cursor = connection.cursor()
                                    try:
                                        self.cur_execute("INSERT INTO dorker_db('url') VALUES(?)", ('www.' + url,))
                                        print self.c + '       [' + self.y + '+' + self.c + '] ' + self.y + url +\
                                              self.g + ' --> ADDED TO Database'
                                    except sqlite3.IntegrityError:
                                        print self.c + '       [' + self.y + '+' + self.c + '] ' + self.y + url + \
                                              self.r + ' --> Was in Database'
                                    cursor.close()
                                    connection.close()
                self.q.task_done()
        except:
            pass


class RowDataBAse(object):
    def __init__(self):
        self.r = '\033[31m'
        self.g = '\033[32m'
        self.y = '\033[33m'
        self.b = '\033[34m'
        self.m = '\033[35m'
        self.c = '\033[36m'
        self.w = '\033[37m'
        self.rr = '\033[39m'
        connection = sqlite3.connect("Database.sqlite3")
        cursor = connection.cursor()
        cursor.execute("SELECT id, url FROM dorker_db;")
        results = cursor.fetchall()
        for r in results:
            with open('results/urls.txt', 'a') as xxx:
                xxx.write(r[1] + '\n')
        print self.c + '       [' + self.y + '+' + self.c + '] ' + self.y + 'Saved In' + self.g + ' results/urls.txt'
        cursor.close()
        connection.close()

class ClearDatabase(object):
    def __init__(self):
        self.r = '\033[31m'
        self.g = '\033[32m'
        self.y = '\033[33m'
        self.b = '\033[34m'
        self.m = '\033[35m'
        self.c = '\033[36m'
        self.w = '\033[37m'
        self.rr = '\033[39m'
        connection = sqlite3.connect("Database.sqlite3")
        cursor = connection.cursor()
        try:
            cursor.execute("delete from dorker_db;")
            print self.c + '       [' + self.y + '+' + self.c + '] ' + self.y + 'Successfully Cleared DataBase!'
            connection.commit()
        except:
            print self.c + '       [' + self.y + '+' + self.c + '] ' + self.y + 'cant delete Rows!'
            sys.exit()
        cursor.close()
        connection.close()



class Main():
    def __init__(self):
        self.gg = True
        self.r = '\033[31m'
        self.g = '\033[32m'
        self.y = '\033[33m'
        self.b = '\033[34m'
        self.m = '\033[35m'
        self.c = '\033[36m'
        self.w = '\033[37m'
        self.rr = '\033[39m'
        self.cls()
        self.print_logo()
        self.PrintOptions()
        while self.gg == True:
            Chose = raw_input(str('    @> '))
            if Chose == str(1):
                self.cls()
                self.print_logo()
                Dorker()
            elif Chose == str(2):
                self.cls()
                self.print_logo()
                RowDataBAse()
            elif Chose == str(3):
                self.cls()
                self.print_logo()
                ClearDatabase()
            elif Chose == str(99) or Chose == "Exit" or Chose == "exit":
                self.gg = False
                sys.exit()
            elif Chose == "help" or Chose == "Help" or Chose == "HELP":
                self.PrintOptions()
            elif Chose == "cls" or Chose == "clear":
                self.cls()
                self.print_logo()
                self.PrintOptions()
            else:
                print self.c + '[' + self.r + '-' + self.c + '] ' + self.w + str(Chose) + ' Commend Not Found!'
                continue

    def cls(self):
        linux = 'clear'
        windows = 'cls'
        os.system([linux, windows][os.name == 'nt'])

    def print_logo(self):
        clear = "\x1b[0m"
        colors = [36, 32, 34, 35, 31, 37]

        x = """
                    White Hat Hackers
                   _     _            _             
                  | |   | |          | | priv8 Dorker By Jok3r
                  | | __| | ___  _ __| | _____ _ __ 
              _   | |/ _` |/ _ \| '__| |/ / _ \ '__|
             | |__| | (_| | (_) | |  |   <  __/ |   
              \____/ \__,_|\___/|_|  |_|\_\___|_|   
                        Iran-cyber.Net    
                        
     Note! : We don't Accept any responsibility for any illegal usage.       
    """
        for N, line in enumerate(x.split("\n")):
            sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
            time.sleep(0.05)

    def PrintOptions(self):
        print(self.y + '        [1] ' + self.c + ' Dork Scanner')
        print(self.y + '        [2] ' + self.c + ' Get Domains From DataBase')
        print(self.y + '        [3] ' + self.c + ' Clear DAtabase')
        print(self.y + '        [99]' + self.c + ' Exit')

Main()
