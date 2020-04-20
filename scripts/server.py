#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Mohammad-AlYasfo

from time import sleep
import RPi.GPIO as G
import logging
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import json
from Manager import manager
from Config import BOARD

from tornado.options import define, options

define("port", default=5000, help="run on the given port", type=int)

def clean_output():
    for i in BOARD.values():
        G.setup(i,G.OUT)
        G.output(i,0)
    pass

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected to the car server.")
        self.motors = manager()
        self.FUNC_MAP = {
            'manual_speed': self.motors.changeSpeedMode,
            'change_speed':self.motors.change_speed,
            'direction': self.motors.move,
            'stop': self.motors.stop,
            # more and more ...
        }
        self.directions = {'F':'Forward','B':'Backward','R':'Right','L':'Left'}
        #speed = threading.Thread(target=self.motors.get_speed, args=())
        #speed.daemon = True
        #speed.start()

    def clean_output(self):
        for i in BOARD.values():
            G.setup(i,G.OUT)
            G.output(i,0)
        pass

    def on_close(self):
        logging.info("A client disconnected")

    def on_message(self, message):
        # print "in server : message from client: %s"%(message)
        data = json.loads(message, encoding='utf-8') # json object
        # result = {"success": func_name}
        for func_name, value in data.items():
            # try:
                # Execution of requested function
            if func_name in self.FUNC_MAP: # Mapping for Execution
                self.FUNC_MAP[func_name](value)
                result = {"success": "%s\t<i class='fa fa-arrow-circle-right'></i>\t%s" % (func_name,value)}
            else:
                result = {"failed": func_name,"error":"command not found"}
                clean_output()
            pass
            # except KeyError as e:
                # clean_output()
                # result = {"failed": func_name,"error":str(e)}
            print "---+"*15
            print result
            self.write_message(result)

def main():
    G.setmode(G.BOARD)
    G.setwarnings(False)
    clean_output()
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
