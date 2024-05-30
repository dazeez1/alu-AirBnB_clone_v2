#!/usr/bin/python3
""" Function that deploys """
from datetime import datetime
from fabric.api import env, local, put, run
import os

env.hosts = ['18.234.81.62', '34.230.70.28']
env.user = "ubuntu"


def deploy():
    """ DEPLOYS """
    try:
        archive_path = do_pack()
        if not archive_path:
            return False
        return do_deploy(archive_path)
    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False


def do_pack():
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')
        t = datetime.now()
        f = "%Y%m%d%H%M%S"
        archive_path = 'versions/web_static_{}.tgz'.format(t.strftime(f))
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except Exception as e:
        print(f"An error occurred during packing: {e}")
        return None


def do_deploy(archive_path):
    """ Deploys """
    if not os.path.exists(archive_path):
        print("Archive does not exist.")
        return False
    try:
        name = os.path.basename(archive_path)
        wname = os.path.splitext(name)[0]
        releases_path = "/data/web_static/releases/{}/".format(wname)
        tmp_path = "/tmp/{}".format(name)

        put(archive_path, tmp_path)
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))
        print("New version deployed!")
        return True
    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False
