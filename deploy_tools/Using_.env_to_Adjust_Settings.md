
## 修改superlists/settings.py，适应把不同的环境
**Development, staging and live sites**
```python
if 'DJANGO_DEBUG_FALSE' in os.environ:  
    DEBUG = False
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']  
    ALLOWED_HOSTS = [os.environ['SITENAME']]  
else:
    DEBUG = True  
    SECRET_KEY = 'insecure-key-for-dev'
    ALLOWED_HOSTS = []
```


## source/下添加.env文件
```bash
echo DJANGO_DEBUG_FALSE=y >> .env
echo SITENAME=$SITENAME >>.env
echo DJANGO_SECRET_KEY=$(
python3.10 -c"import random; print(''.join(random.SystemRandom().
choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50)))"
) >> .env
```


## Gunicorn的配置文件定位.env
**/etc/systemd/system/gunicorn-superlists-staging.top.service**
```angular2html
EnvironmentFile=/home/elspeth/sites/superlists-staging.ottg.eu/.env
```