#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf8')



define("port", default=8088, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/edit/([0-9Xx\-]+)", QuestionnaireEditHandler),
            (r"/add", QuestionnaireEditHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            )
        conn = pymongo.MongoClient("10.0.0.2", 27017)
        self.db = conn["trafficlist"]
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.render(
            "index.html",
        )

class QuestionnaireEditHandler(tornado.web.RequestHandler):
    def get(self, mark=None):
        question = dict()
        if mark:
            coll = self.application.db.questions
            question = coll.find_one({"mark": mark})
        self.render("questionnaire.html",
                    question=question)

    def post(self, mark=None):
        import time
        re=self.request.body
        print re
        question_fields = ['mark', 'Q20', 'Q21','Q22', 'Q23', 'Q24', 'Q30', 'Q31','Q32', 'Q33', 'Q34', 'Q35', 'Q36',
                           'Q37', 'Q38', 'Q39', 'Q40', 'Q41','Q42', 'Q43', 'Q44',  'QQ20', 'QQ21','QQ22', 'QQ23',
                           'QQ24', 'QQ30', 'QQ31','QQ32', 'QQ33', 'QQ34', 'QQ35', 'QQ36', 'QQ37', 'QQ38', 'QQ39',
                           'QQ40', 'QQ41','QQ42', 'QQ43', 'QQ44', 'age0', 'age1', 'age2','age3', 'age4', 'age5',
                           'occupation', "location", "placebegin", 'routestation0', 'routestation00', "checktitle",
                           'routestation1', 'routestation11', "sex0", "sex1", "date", "time", "placeend","occupation0",
                           "occupation1", "occupation2", "occupation3", "occupation4", "occupation5", "occupation6",
                           "path1", "path2","occupation7", "occupation8", "occupation9", "occupation10", "occupation11",
                           "passagetime", "reactpassagetime",'outpurpose0', 'outpurpose1', 'outpurpose2', 'outpurpose3',
                           'facttime0', 'facttime1', 'facttime2', 'facttime3', 'shouldtime0', 'shouldtime1', 'shouldtime2',
                           'shouldtime3', 'shouldtime4', "aa", "bb", "cc", "dd", "ee","ff", "gg","hh", "parkway0", "parkway1",
                           "parkway2", "parkway3", "parkmoney", "kaichecishu0", "kaichecishu1", "kaichecishu2", "kaichecishu3",
                           "kaichecishu4","kaichecishu5", "kaichecishu6", "gjcishu0", "gjcishu1", "gjcishu2", "gjcishu3",
                           "gjcishu4", "gjcishu5", "gjcishu6", "gjcishu7", "drivetime0","drivetime1", "drivetime2",
                           "drivetime3", "drivetime4",'weather0','weather1','weather2','weather3','weather4', "weather",
                           "facttime", "shouldtime","routestation", "routestations", "path1", "path2",
                           ]
        coll = self.application.db.questions
        question = dict()
        if mark:
            question = coll.find_one({"mark": mark})
        for key in question_fields:
            question[key] = self.get_argument(key, None)

        if mark:
            del question['_id']
            question['date_added'] = int(time.time())
            coll.insert(question)
        else:
            coll.save(question)
        
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
