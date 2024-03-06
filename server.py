import sys
from gunicorn.app.wsgiapp import run
if __name__ == '__main__':
    sys.argv = "gunicorn -w 4 -b 0.0.0.0:3000 main:api".split()
    sys.exit(run())