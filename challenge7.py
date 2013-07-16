#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''
Builds n Cloud Servers and adds them as nodes to a new Cloud Load Balancer.
'''

import pyrax
import os
import sys

# The usual setup
pyrax.set_setting("identity_type", "rackspace")
creds = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds)

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

    num_servers = int(sys.argv[1])
    print("Building {} servers".format(num_servers))

    # Build each of the servers
    for server_id in range(num_servers):
        server_name = server_namer.format(server_id=server_id)
        print(u"Bringing {server_name} online".format(server_name=server_name))
        server = cs.servers.create(name=server_name, image=image.id,
                flavor=flav_512.id)
        my_servers.append(server)


    nodes = []
    clb = pyrax.connect_to_cloud_loadbalancers()

    # It takes a little while to come online, so we need to wait until they're
    # available
    for server in my_servers:
        # Done if ACTIVE or ERRORed
        server = pyrax.utils.wait_until(server, "status", ["ACTIVE", "ERROR"],
                attempts=0)

        server_ip = server.networks["private"][0]
        print("IP {} ready".format(server_ip))
        node = clb.Node(address=server_ip, port=80, condition="ENABLED")
        nodes.append(node)

    vip = clb.VirtualIP(type="PUBLIC")

    lb = clb.create("example_lb", port=80, protocol="HTTP", nodes=nodes,
            virtual_ips=[vip])

    print([(lb.name, lb.id) for lb in clb.list()])



