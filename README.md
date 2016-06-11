# YEEasy Portal

This is a linux command line tool. It can easily to operate [Yuan Ze University](https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx) portal. It is fast and have more powerful function.

This project use Python 2.7 write.

## How To Install?

First, you need to clone this project

```
git clone https://github.com/wjs09211/YEEasy_Portal
```
Then, you need to install something. I write a setup script. Execute it!

```
cd YEEasy_Portal # need to move
bash setup.sh
alias yee="python Main.py" # can easy to use
```

## How To Use?

*yee --login* can login the yzu portal
```
yee -l
yee --login
``` 
*yee --class* can look what class you study this semester
```
yee -c
yee --class
```
*yee -cs* can look your school timetable
```
yee -cs
yee --class_schedule
```
*yee -i "classname" "number"* print class infomation.
```
yee -i CS312 # print all infomation
yee -i CS312 5 # print only 5 infomation
```