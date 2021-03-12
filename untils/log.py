import logging
class Log():
    def __init__(self,filename):
        logging.basicConfig(
            level=logging.INFO  ,
            format='%(asctime)s%(levelname)s%(message)s',
            datefmt='%Y-%m-%d %H %M %S',
            filename=filename,
            filemode='a'
        )
        # './../report/log/2021-02-03/log.log'
    def add_log(self,page,func,des):
        out_str=page+':'+func+':'+des
        logging.info(out_str)

