#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''
Creates a Rackspace/Akamai CDN-enabled container in Rackspace Cloud Files.
'''

import pyrax
import os
import argparse

# The usual setup
pyrax.set_setting("identity_type", "rackspace")
creds = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds)

cf = pyrax.cloudfiles


if __name__ == "__main__":
    # Accept a directory and a container name as arguments
    parser = argparse.ArgumentParser(description="Upload a directory to a "
                                    "container on Rackspace's Cloud Files and "
                                    "CDN enable the container.")
    parser.add_argument('directory')
    parser.add_argument('container')

    args = parser.parse_args()

    # Upload the contents of the directory to the container (or create it if it
    # doesn't exist)

    uuid, total_bytes = cf.upload_folder(folder_path=args.directory,
            container=args.container)

    container = cf.get_container(args.container)

    # Time to CDN Enable
    container.make_public()


