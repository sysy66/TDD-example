from fabric.contrib.files import append, exists
from fabric.api import env, local, run, cd
import random

REPO_URL = "https://github.com/sysy66/TDD-example.git"


def deploy():
    # site_folder = f"/home/{env.user}/sites/{env.host}"
    site_folder = f"/home/{env.user}/sites/superlists-staging.top"
    run(f'mkdir -p {site_folder}')
    _create_directory_structure_if_necessary(site_folder)
    source_folder = site_folder + "/source"
    with cd(source_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ("database", "static", "virtualenv", "source"):
        run(f"mkdir -p {site_folder}/{subfolder}")


def _get_latest_source():
    if exists(".git"):
        run(f"git fetch")
    else:
        run(f"git clone {REPO_URL}")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"git reset --hard {current_commit}")


def _update_virtualenv():
    virtualenv_folder = "../virtualenv"
    if not exists(virtualenv_folder + "/bin/pip"):
        run(f"python3.10 -m venv {virtualenv_folder}")
    run(f"{virtualenv_folder}/bin/pip install -r requirements.txt "
        f"-i http://mirrors.aliyun.com/pypi/simple/ "
        f"--trusted-host mirrors.aliyun.comt")


def _create_or_update_dotenv():
    append(".env", "DJANGO_DEBUG_FALSE=y")
    # append(".env", f"SITENAME={env.host}")
    append(".env", "SITENAME=superlists-staging.top")
    current_contents = run("cat .env")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append(".env", f"DJANGO_SECRET_KEY={new_secret}")


def _update_static_files():
    run("../virtualenv/bin/python manage.py collectstatic --noinput")


def _update_database():
    run("../virtualenv/bin/python manage.py migrate --noinput")
