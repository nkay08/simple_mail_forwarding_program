import threading
import logging

logger = logging.getLogger()


def schedule_function(interval: int, worker_func: callable, args: [] = None, kwargs: {} = None, iterations: int = 0):
    if iterations != 1:
        threading.Timer(
            interval,
            schedule_function, [interval, worker_func, args, kwargs, 0 if iterations == 0 else iterations-1]
        ).start()
    logger.warning("Scheduled to run {func} at interval {interval}\n\
     args: {args} \n\
      kwargs: {kwargs}".format(
        func=worker_func.__name__,
        interval=interval,
        args=args,
        kwargs=kwargs)
    )

    if args and kwargs:
        worker_func(*args, **kwargs)
    elif args:
        worker_func(*args)
    elif kwargs:
        worker_func(**kwargs)
    else:
        worker_func()


