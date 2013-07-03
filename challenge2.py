#!/usr/bin/env python

# -*- coding: utf-8 -*-


'''
Clones a server (takes an image and deploys the image as a new server).
'''

import pyrax
import os

# The usual setup
pyrax.set_setting("identity_type", "rackspace")
creds = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds)

cs = pyrax.cloudservers

def create_base():
    '''
    Creates a dummy base
    '''
    # Creating a dummy server that we'll clone from
    base_image = cs.images.list()[0]
    base_flavor = cs.flavors.list()[0]
    base_server = cs.servers.create(name="base", image=base_image.id,
            flavor=base_flavor.id)

    return base_server

def clone_machine(server):
    '''
    Creates an image of the server and returns a clone
    '''
    # Create the image, and get a reference to it
    im = server.create_image("base_image")
    image = cs.images.get(im)

    # Image will be in a "SAVING" state until ready -- wait for ACTIVE
    image = pyrax.wait_until(image, "status", "ACTIVE", attempts=0)

    # Time to clone
    clone_server = cs.servers.create(name="clone", image=image.id,
            flavor=server.flavor['id'])

    return clone_server

if __name__ == "__main__":
    base_server = create_base()
    pyrax.utils.wait_until(base_server, "status", ["ACTIVE", "ERROR"], attempts=0,
            callback=clone_machine)


