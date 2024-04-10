import datetime
import os


class Logger:

    def log_error(self, message: str):
        with open(os.path.join('logs', 'errors.log'), 'a') as f:
            f.write(str(datetime.datetime.now()) + ' - ' + str(message) + '\n')
