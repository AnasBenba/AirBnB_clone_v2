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
        run(f"mkdir -p /data/web_static/releases/{no_ext}/")
        run(f"tar -xzvf /tmp/{file_name} -C " +
            "/data/web_static/releases/{no_ext}/")
        run(f"rm -rf /tmp/{file_name}")
        run(f"mv /data/web_static/releases/{no_ext}/web_static/* " +
            f"/data/web_static/releases/{no_ext}/")
        run(f"rm -rf /data/web_static/releases/{no_ext}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"sudo ln -s /data/web_static/releases/{no_ext}/ " +
            "/data/web_static/current")
        return True
    except Exception:
        return False
