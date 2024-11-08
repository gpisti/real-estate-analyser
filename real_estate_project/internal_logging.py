def basicConfig(level="INFO", format="{level}: {msg}"):
    root.level = level
    root.format = format
    root.handlers.append("StreamHandler")


def info(msg):
    if len(root.handlers) == 0:
        basicConfig()
    root.info(msg)


def warning(msg):
    if len(root.handlers) == 0:
        basicConfig()
    root.warning(msg)


def error(msg):
    if len(root.handlers) == 0:
        basicConfig()
    root.error(msg)


class RootLogger:
    def __init__(self):
        self.handlers = []
        self.level = "INFO"
        self.format = "{level}: {msg}"

    def log(self, level, msg):
        levels = ["INFO", "WARNING", "ERROR"]
        if levels.index(level) >= levels.index(self.level):
            formatted_msg = self.format.format(level=level, msg=msg)
            for handler in self.handlers:
                if handler == "StreamHandler":
                    print(formatted_msg)

    def info(self, msg):
        self.log("INFO", msg)

    def warning(self, msg):
        self.log("WARNING", msg)

    def error(self, msg):
        self.log("ERROR", msg)


root = RootLogger()
