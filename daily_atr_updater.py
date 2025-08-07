crontab -e
# Add: 0 8 * * * cd /home/ec2-user/project_lima && /home/ec2-user/project_lima/lima_env/bin/python daily_atr_updater.py >> /tmp/lima_outputs/daily_cron.log 2>&1
