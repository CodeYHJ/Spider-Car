from scrapy import cmdline

# 运行模块
# name = 'sohu_company'
# name = 'sohu_cars'
name = '1688_factory'

cmd = 'scrapy crawl {0} -s FEED_EXPORT_ENCODING=utf-8'.format(name)
cmdline.execute(cmd.split())
