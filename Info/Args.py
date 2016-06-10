import argparse
from oauth2client import tools

parser = argparse.ArgumentParser(parents=[tools.argparser],
                                 description="YEEasy Portal linux command line operate yzu portal")

parser.add_argument('-l', '--login', action='store_true', help='login')
parser.add_argument('-c', '--classs', action='store_true')
parser.add_argument('-cs', '--class_schedule', action='store_true')
parser.add_argument('-i', '--class_info', nargs="+")
parser.add_argument('-t', '--teach_material', nargs="+")
parser.add_argument('-hw', '--homework', nargs="+")
parser.add_argument('-a', '--auto', type=int)
parser.add_argument('-f', '--find', nargs=2)
parser.add_argument('-avg', '--average', nargs='*')
parser.add_argument('-g', '--grade', nargs='*')
parser.add_argument('-goo', '--google_calendar', action='store_true')
args = parser.parse_args()
