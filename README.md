# limit
Simple parental tools, manage child or teens screentime on ubuntu.


Set your user time out in file limit.dat
eg:
john;40

This means user 'john' only allow to login via desktop for 40 minutes per day.


Run limit.py as root in the background.

Optional
You can use supervisor (apt get supervisor) makesure limit.py always run in background.


Test on Ubuntu 18.10, python3