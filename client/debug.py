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
    def error(cls, msg):
        stack = inspect.stack()
        callerframe = stack[1]
        caller = callerframe.function
        cls.printlogger("ERROR", caller, *msg)