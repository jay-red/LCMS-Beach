#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import jinja2
import os
from google.appengine.ext import db
from hmac import HMAC
from hashlib import sha256
from urllib2 import urlopen
from json import loads
from logging import error

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

SECRET = 'TaeKwonSplash'

class IPAssoc(db.Model):
    fname = db.StringProperty(required = False)
    addr = db.StringProperty(required = True)
    location = db.StringProperty(required = False)
    created = db.DateTimeProperty(auto_now_add = True)

class Admin(db.Model):
    uname = db.StringProperty(required = True) 
    pword = db.StringProperty(required = True)

def hashPass(pword):
    return sha256(pword).hexdigest()

def hashID(uid):
    return HMAC(SECRET, uid).hexdigest()

def checkCookie(cookie):
    uname, uid = cookie.split('|')
    userQuery = db.GqlQuery('SELECT * FROM Admin WHERE uname=:1', uname)
    userQuery = userQuery.get()
    if(userQuery!=None):
        if(hashID(userQuery.key().id())==uid):
            return True
        else:
            return False
    else:
        return False

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
class MainHandler(Handler):
    def get(self):
        self.render('home.html')

class InfoHandler(Handler):
    def get(self):
        self.render('info.html')

class RSVPHandler(Handler):
    def get(self):
        self.render('rsvp.html')

class MapHandler(Handler):
    def get(self):
        self.render('map.html')

class APIHandler(Handler):
    def get(self):
        IPAddr = str(self.request.remote_addr)
        self.response.headers.add_header('Content-Type', 'application/json')
        origins = self.request.get( 'origins' )
        url = urlopen('http://maps.googleapis.com/maps/api/distancematrix/json?origins=' + origins + '&destinations=Oceanside+Pier+CA+92054&language=en-EN&sensor=false')
        resp = url.read()
        addr = loads(resp)["origin_addresses"][0]
        existingEnt = db.GqlQuery('SELECT * FROM IPAssoc WHERE addr=:1', IPAddr)
        existingEnt = existingEnt.get()
        if(existingEnt != None):
            existingEnt.location = addr
            existingEnt.put()
        else:
            newEnt = IPAssoc(addr=IPAddr, location=addr)
            newEnt.put()
        self.write( resp )

class FormHandler(Handler):
    def get(self):
        fname = self.request.get('fname')
        IPAddr = str(self.request.remote_addr)
        if(fname):
            self.write('Data stored for ' +  str(IPAddr))
            existingEnt = db.GqlQuery('SELECT * FROM IPAssoc WHERE addr=:1', IPAddr)
            existingEnt = existingEnt.get()
            if(existingEnt != None):
                existingEnt.fname = fname
                existingEnt.put()
            else:
                newEnt = IPAssoc(addr=IPAddr, fname=fname)
                newEnt.put()
        else: 
            self.render('form.html')

class LoginHandler(Handler):
    def get(self):
        self.render("login.html")
    def post(self):
        uname = self.request.get("user")
        pword = self.request.get("pword")
        self.render("login.html", val="value="+uname)

class CreateHandler(Handler):
    def get(self):
        self.render("create.html")
    def post(self):
        self.render("create.html")

class AdminHandler(Handler):
    def get(self):
        assoc = db.GqlQuery("SELECT * FROM IPAssoc ORDER BY created")
        self.render("admin.html", assoc=assoc)
    
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/info', InfoHandler),
    ('/rsvp', RSVPHandler),
    ('/map', MapHandler),
    ('/api', APIHandler),
    ('/rsvpForm', FormHandler),
    ('/login', LoginHandler),
    ('/create', CreateHandler),
    ('/admin', AdminHandler)
], debug=True)
