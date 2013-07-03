#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''
Builds three 512 MB servers that follow a similar naming convention
and returns the IP and login credentials for each server.
'''

import pyrax
import os

# The usual setup
pyrax.set_setting("identity_type", "rackspace")
creds = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds)

cs = pyrax.cloudservers

# Get the Fedora 17/Beefy Miracle image
beefy_images = (image for image in cs.images.list() if "Beefy" in image.name)
image = beefy_images.next()

# We want a 512 MB machine (could also just grab the first, but we'll go ahead
# and pick it out)
flav_gen = (flavor for flavor in cs.flavors.list() if flavor.ram == 512)
flav_512 = flav_gen.next()

# Set up a formatter
server_namer = "lv2srv_{server_id}"

my_servers = []

# Build each of the servers
for server_id in range(3):
    server_name = server_namer.format(server_id=server_id)
    print(u"Bringing {server_name} online".format(server_name=server_name))
    server = cs.servers.create(name=server_name, image=image.id,
            flavor=flav_512.id)
    my_servers.append(server)

# It takes a little while to come online, so we need to wait until they're
# available
for server in my_servers:
    # Done if ACTIVE or ERRORed
    print("")
    print("*"*28)
    print("Waiting on activity for {}".format(server.name))
    server = pyrax.utils.wait_until(server, "status", ["ACTIVE", "ERROR"],
            attempts=0)

    if(server.status == u'ERROR'):
        print("** Server creation failed **")
        print("**       CONTINUING       **")
        continue

    print("ACTIVE!")
    print("")

    print(u"Admin Password: {}".format(server.adminPass))

    private_ip = server.networks['private'][0]
    public_ips = server.networks['public']

    print("Private IP: {}".format(private_ip))
    print("Public IPs: {}, {}".format(public_ips[0],public_ips[1]))
    print("")
    print("Tearing down {}".format(server.name))
    server.delete()
    print("*"*28)


print("")
# Might as well delete the servers now too
for server in my_servers:
    print("Tearing down {}".format(server.name))
    server.delete()

