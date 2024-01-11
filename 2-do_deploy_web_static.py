#!/usr/bin/python3
"""
script that generates a .tgz archive
"""
from fabric.api import env, put, run
import os

env.hosts = ['18.234.193.135', '52.23.245.52']


def do_deploy(archive_path):
    """
    Fabric script that distributes
    an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = os.path.basename(archive_path)
        no_ext = os.path.splitext(file_name)[0]
        put(archive_path, '/tmp/')
        run("mkdir -p /data/web_static/releases/{}/".format(no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
    .format(file_name, no_ext))
        run("rm -rf /tmp/{}".format(file_name))
        run(("mv /data/web_static/releases/{}/web_static/* " +
    "/data/web_static/releases/{}/").format(no_ext, no_ext))
        run("rm -rf /data/web_static/releases/{}/web_static/"
    .format(no_ext))
        run("rm -rf /data/web_static/releases/{}/web_static".format(no_ext))
        run("rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ ".format(no_ext) +
            "/data/web_static/current")
        return True
    except Exception:
        return False
