import subprocess

cmd = '/usr/bin/google-chrome-stable --remote-debugging-port=9222 --user-data-dir=/home/feng/workspace/ChromeProfile'

subprocess.run(cmd)