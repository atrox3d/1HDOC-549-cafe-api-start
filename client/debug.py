import inspect


class Debug:
    from dataclasses import dataclass

    @dataclass()
    class FakeResponse:
        status_code = 200
        text = "debug fake response"
        url = "debug"

    enabled = False
    response = FakeResponse()

    @classmethod
    def enable(cls):
        cls.enabled = True

    @classmethod
    def disable(cls):
        cls.enabled = False

    @classmethod
    def printlogger(cls, level, callername, *msg):
        print(f"{level:<8}|", f"{callername:>20}()|", *msg)

    @classmethod
    def info(cls, *msg):
        stack = inspect.stack()
        callerframe = stack[1]
        caller = callerframe.function
        cls.printlogger("INFO", caller, *msg)

    @classmethod
    def debug(cls, msg):
        if not cls.enabled:
            return
        stack = inspect.stack()
        callerframe = stack[1]
        caller = callerframe.function
        cls.printlogger("INFO", caller, *msg)

    @classmethod
    def success(cls, *msg):
        stack = inspect.stack()
        callerframe = stack[1]
        caller = callerframe.function
        cls.printlogger("SUCCESS", caller, *msg)

    @classmethod
    def error(cls, *msg):
        stack = inspect.stack()
        callerframe = stack[1]
        caller = callerframe.function
        cls.printlogger("ERROR", caller, *msg)

    @classmethod
    def decorator(cls, function):

        def params2str(*args, **kwargs):
            argslist = list(map(str, args))
            kwargslist = [f"{key}={value}" for key, value in kwargs.items()]
            params = argslist + kwargslist
            return ", ".join(params)

        import functools
        cls.info(f"decorating {function.__name__}")

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            cls.info(f"executing {function.__name__}({params2str(*args, **kwargs)})")
            retval = function(*args, **kwargs)
            cls.info("retval: ", retval)
            return retval

        cls.info("returning decorated")
        return wrapper
