import subprocess
import urllib.request
import time

def main():
    proc = subprocess.Popen(['gunicorn', '--reload', 'look.app_1'],
                             # shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

    try:
        time.sleep(1.2)
        resp = urllib.request.urlopen('http://127.0.0.1:8000/sayHello')
        # print(resp.read())
        assert b'{"msg"' in resp.read()
    finally:
        proc.terminate()
        try:
            outs, _ = proc.communicate(timeout=0.2)
            print('== subprocess exited with rc =', proc.returncode)
            print(outs.decode('utf-8'))
        except subprocess.TimeoutExpired:
            print('subprocess did not terminate in time')

if __name__ == '__main__':
    main()
