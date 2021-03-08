import threading
import logging
import datetime

logger = logging.getLogger()


def schedule_function(interval: int, worker_func: callable, args: [] = None, kwargs: {} = None, iterations: int = 0):
    try:
        if iterations != 1:
            threading.Timer(
                interval,
                schedule_function, [interval, worker_func, args, kwargs, 0 if iterations == 0 else iterations - 1]
            ).start()
    except Exception as e:
        logger.error(e, exc_info=True)

    try:
        logger.info("Scheduled to run {func} at interval {interval}\n\
         args: {args} \n\
          kwargs: {kwargs}".format(
            func=worker_func.__name__,
            interval=interval,
            args=args,
            kwargs=kwargs)
        )
        time = (datetime.datetime.now() + datetime.timedelta(seconds=interval)).strftime("%Y-%m-%d-%H-%M")
        logger.info("Next run of {func} at {time}".format(func=worker_func.__name__, time=time))
    except Exception as e:
        logger.error(e, exc_info=True)


    try:
        if args and kwargs:
            worker_func(*args, **kwargs)
        elif args:
            worker_func(*args)
        elif kwargs:
            worker_func(**kwargs)
        else:
            worker_func()
    except Exception as e:
        logger.error("Encountered error in scheduled function {func} at interval {interval}\n\
            args: {args} \n\
            kwargs: {kwargs}".format(
            func=worker_func.__name__,
            interval=interval,
            args=args,
            kwargs=kwargs)
        )
        logger.error(e, exc_info=True)


