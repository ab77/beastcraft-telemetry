#!/usr/bin/env python

import inspect, traceback, time
from functools import wraps
from subprocess import Popen, PIPE
from flask import abort

from application import application
from config import (DEFAULT_TRIES, DEFAULT_DELAY, DEFAULT_BACKOFF,
                    API_VERSION, WORKDIR, DEBUG)


def retry(ExceptionToCheck, tries=DEFAULT_TRIES, delay=DEFAULT_DELAY, backoff=DEFAULT_BACKOFF, cdata=None):
    '''Retry calling the decorated function using an exponential backoff.
    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    '''
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    print '%s, retrying in %d seconds (mtries=%d): %s' % (repr(e), mdelay, mtries, str(cdata))
                    if DEBUG == 1: traceback.print_exc()
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry


@retry(Exception, cdata='method=%s()' % inspect.stack()[0][3])
def run_shell_cmd(cmd):
    p = Popen(cmd.split(' '),
              stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
    output, err = p.communicate()
    return p.returncode, output, err


@application.route('/api/v%s/mobile/<string:cmd>' % API_VERSION, methods=['GET'])
def cmd_mobile(cmd):
    if cmd in ['start', 'stop']:
        try:
            res = run_shell_cmd('%s/%s-mobile.sh' % (WORKDIR, cmd))
        except Exception as e:
            print repr(e)
            abort(500)
    else:
        abort(404)
        
    return res[1]


if __name__ == '__main__': 
    application.run()
