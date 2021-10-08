#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import cgi
import html

form = cgi.FieldStorage()
first_name = html.escape(form.getfirst("first-name", "empty"))
last_name = html.escape(form.getfirst("last-name", "empty"))
is_adult = form.getfirst("is-adult", "false")
state = form.getfirst("state", "male")

print(first_name)
print(last_name)
print(is_adult)
print(state)
