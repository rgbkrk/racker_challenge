#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''
Creates a Cloud Database instance with one database and one user that can
connect to it.
'''

import argparse
import os

import pyrax

import string
import random

def passgen(size=8, chars=string.letters+string.digits):
    return ''.join(random.choice(chars) for x in range(size))

# The usual setup
pyrax.set_setting("identity_type", "rackspace")
creds = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds)

cdb = pyrax.cloud_databases

# Create an instance to hold our database (could hold more)
print("Creating instance for databases")
inst = cdb.create("inst.db", flavor="1GB Instance", volume=2)

# Wait for the instance to come online
print("Waiting for instance to come online")
inst = pyrax.utils.wait_until(inst, "status", ["ACTIVE", "ERROR"])

# Add a database
print("Creating a database")
db = inst.create_database("mmmData")

# Add user
print("Adding a user")
username = "imadba"
password = passgen()
user = inst.create_user(name=username, password=password, database_names=[db])

print("User: {}".format(username))
print("Password: {}".format(password))

#TODO: Figure out how one would connect to this...

