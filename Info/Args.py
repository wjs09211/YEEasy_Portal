import argparse
from oauth2client import tools
import textwrap

parser = argparse.ArgumentParser(parents=[tools.argparser], formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=textwrap.dedent('''\
                                            YEEasy Portal
                                 ----------------------------------------
                                 linux command line operate yzu portal
                                        more easy more powerful !!!
                                 '''))

parser.add_argument('-l', '--login', action='store_true', help='login the yzu portal, need use this first')
parser.add_argument('-c', '--classs', action='store_true', help='can look what class you study this semester')
parser.add_argument('-cs', '--class_schedule', action='store_true', help='can look your school timetable')
parser.add_argument('-i', '--class_info', nargs="+", help='can look your class info')
parser.add_argument('-t', '--teach_material', nargs="+", help='can look and download your class teach material')
parser.add_argument('-hw', '--homework', nargs="+", help='can look and download and upload your class homework')
parser.add_argument('-a', '--auto', type=int, help='auto fill yzu question')
parser.add_argument('-f', '--find', nargs=2,
                    help='find keyword in all teach material, only support these file type: doc, docx, pptx, pdf, txt')
parser.add_argument('-avg', '--average', nargs='*', help='show average grade, use with --grade')
parser.add_argument('-g', '--grade', nargs='*', help='show grade up or down the number')
parser.add_argument('-goo', '--google_calendar', action='store_true',
                    help='import your school timetable to Google Calendar')
args = parser.parse_args()
