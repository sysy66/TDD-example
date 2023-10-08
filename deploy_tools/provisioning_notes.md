
配置新网站
=======================
## 需要的包：
* nginx
* Python 3.10..12
* virtualenv + pip
* Git
- 以Ubuntu为例：
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get install nginx git python3.10 python3.10-venv

## Nginx虚拟主机
* 参考nginx.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com

## Systemd服务
* 参考gunicorn-upstart.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com

## 文件夹结构：
假设有用户账户，家目录为/home/username
```bash
/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv
```

## 下面告诉Systemd，使用systemctl命令启动Gunicorn：
* 必须执行这个命令，让Systemd加载新的配置文件
  - elspeth@server:$ sudo systemctl daemon-reload
* 这个命令让Systemd在引导时加载服务
  - elspeth@server:$ sudo systemctl enable gunicorn-superlists-staging.ottg.eu
* 这个命令启动服务
  - elspeth@server:$ sudo systemctl start gunicorn-superlists-staging.ottg.eu


## 使用sed配置Nginx和Gunicorn
```bash
# 配置Nginx
cat ./deploy_tools/nginx.template.conf | sed "s/SITENAME/superlists-staging.top/g" | sudo tee /etc/nginx/sites-available/superlists-staging.top

sudo ln -s /etc/nginx/sites-available/superlists-staging.top /etc/nginx/sites-enabled/superlists-staging.top


# 配置Gunicorn
cat ./deploy_tools/gunicorn-systemd.template.service | sed "s/SITENAME/superlists-staging.top/g" | sudo tee /etc/systemd/system/gunicorn-superlists-staging.top.service

sudo systemctl daemon-reload
sudo systemctl reload nginx
sudo systemctl enable gunicorn-superlists-staging.top
sudo systemctl start gunicorn-superlists-staging.top
```
