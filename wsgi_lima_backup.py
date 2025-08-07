#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/home/ec2-user/project_lima')

# Import the new warehouse-enabled version
exec(open('web_app_with_warehouse.py').read())

if __name__ == "__main__":
    app.run()
