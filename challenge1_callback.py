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

def summarize(server):
    '''
    For an ACTIVE server, prints IP and login credentials.

    If server has ERRORED, simply alerts and exits.

    If server is in any other state, function returns.

    >>> cs = pyrax.cloudservers
    >>> image, flavor = cs.images.list()[0], cs.flavors.list()[0]
    >>> server_name = "lv2srv"
    >>> server = cs.servers.create(name=server_name, image=image.id,
            flavor=flav_512.id)
    >>> server = pyrax.utils.wait_until(server, "status", ["ACTIVE", "ERROR"], attempts=0)
    >>> summarize(server) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    ****************************
    Server: lv2srv
    ACTIVE!

    Admin Password: ...
    Private IP: ...
    Public IPs: ...

    Tearing down lv2srv
    ****************************

    '''

    print("")
    print("*"*28)
    print(u"Server: {}".format(server.name))
    if(server.status == u'ERROR'):
        print("**         ERROR!         **")
        print("** Server creation failed **")
        return
    if(server.status != u'ACTIVE'):
        print("** Server in wrong state for summary **")
        return

    print("ACTIVE!")
    print("")

    print(u"Admin Password: {}".format(server.adminPass))

    private_ip = server.networks['private'][0]
    public_ipv4 = server.accessIPv4
    public_ipv6 = server.accessIPv6

    print("Private IP: {}".format(private_ip))
    print("Public IPv4: {}".format(server.accessIPv4))
    print("Public IPv6: {}".format(server.accessIPv6))
    print("")
    print("Tearing down {}".format(server.name))
    server.delete()
    print("*"*28)

    pyrax.utils.wait_until(server, "status", ["DELETE"], attempts=0,
            callback=declare_freedom)

def declare_freedom(server):
    #print("{} deleted".format(server.name))
    print("Deleted some server...")

if __name__ == "__main__":
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
        server = pyrax.utils.wait_until(server, "status", ["ACTIVE", "ERROR"],
                attempts=0, callback=summarize)

