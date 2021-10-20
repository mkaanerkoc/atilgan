import time

def timeit(function):
    def timed(*args, **kwargs):
        ts = time.time()
        result = function(*args, **kwargs)
        te = time.time()
        print('{} {} - {} sec'.format(function.__name__, args[1:], te - ts))
        return result

    return timed
