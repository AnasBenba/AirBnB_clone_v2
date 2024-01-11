#!/usr/bin/python3
"""
Fabric script that creates and 
distributes an archive to your web servers
"""
from fabric.api import local, env, put, run
from datetime import datetime
import os

env.hosts = ['18.234.193.135', '52.23.245.52']


def do_pack():
    """
    Fabric script that generates a .tgz archive
    """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = f'versions/web_static_{date}.tgz'
    print(f'Packing web_static to {file_path}')
    try:
        local(f"tar -czvf {file_path} web_static")
        size = os.path.getsize(file_path)
        print(f'web_static packed: {file_path} -> {size}Bytes')
        return file_path
    except Exception:
        return None


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
        run("tar -xzvf /tmp/{} -C ".format(file_name) +
            "/data/web_static/releases/{}/".format(no_ext))
        run("rm -rf /tmp/{}".format(file_name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(no_ext))
        run("rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ ".format(no_ext) +
            "/data/web_static/current")
        return True
    except Exception:
        return False



def deploy():
    """
    Fabric script that creates and 
    distributes an archive to your web servers
    """
    file_name = do_pack()
    if file_name:
        return do_deploy(file_name)
    else:
        return False
