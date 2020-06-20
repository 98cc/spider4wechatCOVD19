import sys
import io
from urllib import request
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

#登录后才能访问的网站
url = 'https://www.douban.com/'

#浏览器登录后得到的cookie，也就是刚才复制的字符串
cookie_str = r'_vwo_uuid_v2=E2101833D21905A3CAA38D502851BC57|66ad7e9ac7c72527ab071c14c17dc807; gr_user_id=91651177-0a18-412f-830a-678541ff16dd; douban-fav-remind=1; __gads=ID=43b38dca7af0950b:T=1557990923:S=ALNI_MbURjGY1DceDDgsrmhe_YiQsC_ADg; bid=KAKwSRNoRp8; __yadk_uid=nRgk5VpG5qtfoqjA6Itx1hMRCsaKJ7ot; ll="118318"; trc_cookie_storage=taboola%2520global%253Auser-id%3D21636db6-6480-4c7c-a72a-ffa6438e8c68; viewed="26792376_4063119_26826548"; ct=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16658; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1584087504%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DoT7qtrD557LA5hemIKVgMIxCajwdnQ6s7zmhqAggWowZqhKoArVHCzQYnOFPJQH-%26wd%3D%26eqid%3Dad8d3bee0026c0d5000000035e6b41cc%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.1893406972.1490418682.1584082999.1584087506.90; __utmc=30149280; __utmz=30149280.1584087506.90.89.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmb=30149280.2.10.1584087506; dbcl2="166587851:QJCPWJ43QY8"; ck=HY-x; _pk_id.100001.8cb4=ccacbdd515ff3271.1490418682.45.1584088909.1584083018.; ap_v=0,6.0'

#登录后才能访问的网页
url = 'https://www.douban.com/'

req = request.Request(url)
#设置cookie
req.add_header('cookie', cookie_str)
#设置请求头
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')

resp = request.urlopen(req)

print(resp.read().decode('utf-8'))