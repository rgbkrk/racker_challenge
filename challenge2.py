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

    # Creating a dummy server that we'll clone from
    base_image = cs.images.list()[0]
    base_flavor = cs.flavors.list()[0]
    base_server = cs.servers.create(name="base", image=base_image.id,
            flavor=base_flavor.id)

    return base_server

def clone_machine(server):
    im = server.create_image("base_image")

    # Note: need to wait for image to be created before the cloning will work
    # TODO: Figure out how to catch this. Add it to the docs on pyrax as well
    #           pyrax.wait_until

    clone_server = cs.servers.create(name="clone", image=im,
            flavor=server.flavor['id'])

if __name__ == "__main__":
    base_server = create_base()
    pyrax.utils.wait_until(base_server, "status", ["ACTIVE", "ERROR"], attempts=0,
            callback=clone_machine)


