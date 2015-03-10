Перезапуск на чероки (если внесены изменения в код):
1) htop->kill ota process
2) /home/emercom/ota_web/env/bin/python /home/emercom/ota_web/manage.py runfcgi protocol=scgi host=0.0.0.0 port=43208 pidfile=/home/emercom/ota_web/ota.pid