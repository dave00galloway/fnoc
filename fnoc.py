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


from flask import Flask, jsonify, request

FIBONACCI_SEQ_LIMIT = 999999

fnoc = Flask(__name__)

fnoc.config.from_envvar('FNOC_SETTINGS', silent=True)


def calc_fibonacci(x):
    if x < 0:
        return []
    flist = [0, 1, 1]
    y, z = 1, 1
    if x >= 2:
        for i in range(x - 2):
            z, y = y + z, z
            flist.append(z)
    del y
    del z
    try:
        return flist[0:x]
    finally:
        del flist


def call_fibons():
    error_message = "None"
    n = 0
    try:
        n = int(request.args.get('n'))
    except (TypeError, ValueError):
        error_message = "use: domain/fibonacci?n=N or last/fibonacci?n=N where N is a positive integer"
    if n is 0:
        error_message = "requested 0 length Fibonacci sequence"
    if n < 0:
        error_message = "requested negative length Fibonacci sequence"

    elif n > FIBONACCI_SEQ_LIMIT:
        error_message = "truncated Fibonacci sequence at %s", FIBONACCI_SEQ_LIMIT
        n = FIBONACCI_SEQ_LIMIT
    return error_message, n


@fnoc.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@fnoc.route("/fibonacci")
def fibonacci():
    error_message, n = call_fibons()
    if error_message == 'None':
        return jsonify({'error': error_message, 'Fibonacci': calc_fibonacci(n)})
    return jsonify({'error': error_message})


@fnoc.route("/last")
def last():
    error_message, n = call_fibons()
    if error_message == 'None':
        last_num = calc_fibonacci(n)[-1]
        try:
            return jsonify({'error': error_message, 'Last': last_num})
        finally:
            print('deleting')
            del last_num
    return jsonify({'error': error_message})


@fnoc.route("/testfnoc")
# five unit test cases: n=10, n=-1, no parameter, malformed parameters
def test_fnoc():
    f10 = {"Fibonacci": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]}
    return jsonify(f10)


if __name__ == "__main__":
    fnoc.run(host='0.0.0.0')
