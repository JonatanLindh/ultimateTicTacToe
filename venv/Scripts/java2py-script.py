#!C:\Users\Jonatan\PycharmProjects\ultimateTicTacToe\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pyjs==0.8.2','console_scripts','java2py'
__requires__ = 'pyjs==0.8.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pyjs==0.8.2', 'console_scripts', 'java2py')()
    )
