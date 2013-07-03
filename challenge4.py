#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''
This script uses Cloud DNS to create a new A record when passed a FQDN, IP
address, and email address as arguments.

The email address should be the domain administrator's.
'''

import argparse
import os

import pyrax

# The usual setup
pyrax.set_setting("identity_type", "rackspace")
creds = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds)

dns = pyrax.cloud_dns

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a new A record when "
                            "passed a FQDN, IP address, and email as arguments"
                            )
    parser.add_argument('FQDN')
    parser.add_argument('ip_address')
    parser.add_argument('email')

    args = parser.parse_args()

    # TODO: Check to see if domain exists first
    dom = dns.create(name=args.FQDN, emailAddress=args.email)
    recs = [{ "type": "A", "name": args.FQDN, "data": args.ip_address, "ttl": 6000}]
    dom.add_records(recs)

    # Bye bye domain
    dom.delete()

