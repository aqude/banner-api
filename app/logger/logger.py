import datetime
import os


class Logger:

    def log_error(self, message):
        with open(os.path.join('logs', 'errors.log'), 'a') as f:
            f.write(str(datetime.datetime.now()) + ' - ' + message + '\n')
