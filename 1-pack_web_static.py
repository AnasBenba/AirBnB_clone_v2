#!/usr/bin/python3
"""
script that generates a .tgz archive
"""
from fabric.api import local
from datetime import datetime
import os


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
