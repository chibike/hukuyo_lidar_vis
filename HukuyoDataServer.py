from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import json
import re
import cgi

import HokuyoLidarObject

class LocalData(object):
  records = {"data":"Hello everybody"}
 
class HTTPRequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    if None != re.search('/api/v1/addrecord/*', self.path):
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'application/json':
        length = int(self.headers.getheader('content-length'))
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        recordID = self.path.split('/')[-1]
        LocalData.records[recordID] = data
        print "record %s is added successfully" % recordID
      else:
        data = {}
      self.send_response(200)
      self.end_headers()
    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    return
 
  def do_GET(self):
    if None != re.search('/api/v1/getrecord/*', self.path):
      recordID = self.path.split('/')[-1]
      print dir(self)
      if LocalData.records.has_key(recordID):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(LocalData.records[recordID])
      else:
        self.send_response(400, 'Bad Request: record does not exist')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    elif None != re.search('/api/v1/getlidardata/*', self.path):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        device = HokuyoLidarObject.HokuyoLidarObject('/dev/ttyACM0', 115200);
        self.wfile.write(json.dumps(device.getSample()))
        device.close()
    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    return
 
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  allow_reuse_address = True
 
  def shutdown(self):
    self.socket.close()
    HTTPServer.shutdown(self)
 
class SimpleHttpServer():
  def __init__(self, ip, port):
    self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)
 
  def start(self):
    self.server_thread = threading.Thread(target=self.server.serve_forever)
    self.server_thread.daemon = True
    self.server_thread.start()
 
  def waitForThread(self):
    self.server_thread.join()
 
  def addRecord(self, recordID, jsonEncodedRecord):
    LocalData.records[recordID] = jsonEncodedRecord
 
  def stop(self):
    self.server.shutdown()
    self.waitForThread()
 
if __name__=='__main__':
  server = SimpleHttpServer("127.0.0.1", 9999)
  print 'HTTP Server Running...........'
  server.start()
  server.waitForThread()

##import SocketServer
##
##d = '''HTTP/1.x 200 OK
##Transfer-Encoding: chunked
##Date: Sat, 28 Nov 2009 04:36:25 GMT
##Server: LiteSpeed
##Connection: close
##Expires: Sat, 28 Nov 2009 05:36:25 GMT
##Content-Type: text/html; charset=UTF-8
## 
##<!DOCTYPE html>
##<html>
##<head>
##<title>Sample Page</title>
##</head>
##</html>'''
##
##class MyTCPHandler(SocketServer.BaseRequestHandler):
##    def handle(self):
##        self.data = self.request.recv(1024).strip()
##        print "Client Add:",self.client_address
##        print "Data:",self.data
##        print "-"*20
##        self.request.send(d)
##        #print "SELF",dir(self)
##        #print "REQUEST",dir(self.request)
##
##if __name__ == '__main__':
##    HOST, PORT = "localhost", 9999
##
##    # Create the server, binding to localhost on port 9999
##    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
##    #print "SERVER: ",dir(server)
##
##    # Activate the server; this will keep running until interrupted
##    # with Ctrl-c
##    server.serve_forever()
