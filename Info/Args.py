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

parser.add_argument('-l', '--login', action='store_true', help='Login the yzu portal')
parser.add_argument('-c', '--classs', action='store_true', help='Show what class you study this semester')
parser.add_argument('-cs', '--class_schedule', action='store_true', help='Show your school schedule')
parser.add_argument('-i', '--class_info', nargs="+", help='Show your class information')
parser.add_argument('-t', '--teach_material', nargs="+", help='Show and download your class teach material')
parser.add_argument('-hw', '--homework', nargs="+", help='Show and download and upload your class homework')
parser.add_argument('-a', '--auto', type=int, help='auto fill yzu question')
parser.add_argument('-f', '--find', nargs=2,
                    help='find keyword in all teach material, only support these file type: doc, docx, pptx, pdf, txt')
parser.add_argument('-avg', '--average', nargs='*', help='show average grade, use with --grade')
parser.add_argument('-g', '--grade', nargs='*', help='show grade up or down the number')
parser.add_argument('-goo', '--google_calendar', action='store_true',
                    help='import your school schedule to Google Calendar')

parser.add_argument('-r', '--rank', action='store_true', help="Show your rank form YeePortal server")
parser.add_argument('-u', '--upload', action='store_true', help='upload your grade to YeePortal server')

args = parser.parse_args()
