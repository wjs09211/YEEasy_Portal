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

**yee -l** login the yzu portal
```
yee -l
yee --login
``` 
**yee -c** look what class you study this semester
```
yee -c
yee --class
```
**yee -cs** look your school timetable
```
yee -cs
yee --class_schedule
```
**yee -i "classname" "number"** print class infomation.
```
yee -i CS312 # print all infomation
yee -i CS312 5 # print only 5 infomation
```
**yee -t "classname" "number"** look and download your class teach material.
```
yee -t CS312
yee -t CS312 1 # download first teach material
```
**yee -hw "classname" "number" "file_name"** look and download or upload homework.

One argument look homework infomation. 

Two argument download homework attachment. 

Three argument upload your homework file. 
```
yee -hw CS312
yee -hw CS312 1
yee -hw CS312 homework.txt
```
**yee -a "value"** Auto fill class question. Value has 1~5. 1 is very good. 2 is good. 3 is normal. 4 is bad. 5 is very bad.
```
yee -a 1
yee -a 2
``` 
**yee -f "classname" "keyword"** Find keyword appear in teach material. Can tell you keyword appear in witch file. And where in file.
```
yee -f CS312 "process"
```
**yee -goo** Import your school timetable to Google Calendar.
```
yee -goo
```
**yee -g** Show your grade.
```
yee -g -avg # Show your total average
yee -g -avg 102/2 # Show your semester average
yee -g 60 down # Show class grage which below 60 (fail)
yee -g 90 up # Show class grage which above 90
```
**yee -g -u** Upload your grade to YeePortal server. you can select anonymous or no anonymous.

**yee -g -r** Show your rank in YeePortal server.

If you want to look your class rank in Yuan Ze University, you need to paid 10 NTD. We write this function to save your money.
