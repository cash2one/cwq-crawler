# -*- coding: utf-8 -*-

import httplib2
import lockfile
import sys
import os.path
from utils import read_config

class Merchant:
    def __init__(self, name, crawlEntryUrl=None):
        self.name = name
        self.crawlEntryUrl = crawlEntryUrl if crawlEntryUrl else None
        self.distributedFetch = False
        self.headersFile = None
        self.parser = None

class CategoryInfo:
    pass

class ProductInfo:
    pass

class Fetch:
    def fetch(self, task):
        h = httplib2.Http()
        response, content = h.request(uri=task.url, method='GET', headers=task.headers)
        return response.status, content
    
    def getHtmlDoc(self, fetchTask):
        pass

class Parser:
    def parseCategories(self, homepage_content):
        pass


class Crawler:
    def __init__(self, merchant, parser):
        self.merchant = merchant
        self.parser = parser
    
    def crawl(self):
        pass
        

def crawl(merchantName):
    merchant = init_merchant(merchantName)
    #该步主要是获取parser
    moduleName, parserClass = merchant.parser.split('.')
    module = __import__(moduleName)
    parser = getattr(module, parserClass)
    #得到crawler的实例
    crawler = Crawler(merchant, parser)
    crawler.crawl()
    

def init_merchant(merchantName):
    cfgFilename = './config/' + merchantName + '.cfg'  #config文件放在config文件夹下
    config = read_config(cfgFilename)
    m = Merchant(merchantName)
    m.distributedFetch = config.get('default', 'distributedFetch')
    m.headersFile = config.get('default', 'headersFile')
    m.crawlEntryUrl = config.get('default', 'crawlEntryUrl')
    m.parser = config.get('default', 'parser')
    return m

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >> sys.stderr, 'Usage: python %s merchantName' % os.path.split(sys.argv[0])[1]
        sys.exit(1)
    merchantName = sys.argv[1]
    #一种情形下没法自动解锁, 那就是程序运行之前就存在锁, 即本次完整运行本次解锁
    lock = lockfile.FileLock(merchantName + '-lock')
    try:
        lock.acquire(10)
    except Exception, e:
        print e #Timeout waiting to acquire lock for merchantName-lock
        sys.exit(1)
    try:
        crawl(merchantName)
    except Exception, e:
        print e
    finally:
        lock.release()
        
    

