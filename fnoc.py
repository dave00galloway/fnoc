##############################################################
# 
# fnoc.py
#
# calculates a Fibonacci sequence using a web service
# takes a single integer on the URL and reports the 
# series as JSON so people might actually use it
#
#    a call URL http://domain.com/fibonacci?n=10
#
#    should return the following JSON document:
#
#    { "Fibonacci": [ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34 ] }
#
#
##############################################################

FIBONACCI_SEQ_LIMIT = 999999

from flask import Flask, jsonify, request

fnoc = Flask(__name__)

fnoc.config.from_envvar('FNOC_SETTINGS', silent=True)


def fibons(x):
    if x < 0: return []
    flist = [0, 1, 1]
    y, z = 1, 1
    if x >= 2:
        for i in range(x - 2):
            z, y = y + z, z
            flist.append(z)
    return flist[0:x]


@fnoc.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@fnoc.route("/fibonacci")
def fibonacci():
    error_message = "None"

    try:
        n = int(request.args.get('n'))
    except:
        error_message = "use: domain/fibonacci?n=N where N is a positive integer"
        return jsonify({'error': error_message})

    if n < 0:
        error_message = "requested negative length Fibonacci sequence"
        return jsonify({'error': error_message})

    elif n > FIBONACCI_SEQ_LIMIT:
        error_message = "truncated Fibonacci sequence at 20000"
        n = FIBONACCI_SEQ_LIMIT

    return jsonify({'error': error_message, 'Fibonacci': fibons(n)})


@fnoc.route("/last")
def last():
    error_message = "None"

    n = int(request.args.get('n'))

    last = fibons(n)[-1]
    return jsonify({'error': error_message, 'Last': last})


@fnoc.route("/testfnoc")
# five unit test cases: n=10, n=-1, no parameter, malformed parameters
def testfnoc():
    F10 = {"Fibonacci": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]}
    return (jsonify(F10))


if __name__ == "__main__":
    fnoc.run(host='0.0.0.0')
