import datetime
import os
LOG_PATH = 'logs/errors.log'

class Logger:

    def log_error(self, message: str):
        if not os.path.exists(os.path.dirname(LOG_PATH)):
            os.mkdir(os.path.dirname(LOG_PATH))
        if not os.path.isfile(LOG_PATH):
            with open(LOG_PATH, 'w') as f:
                f.close()

        with open(os.path.join('logs', 'errors.log'), 'a') as f:
            f.write(str(datetime.datetime.now()) + ' - ' + str(message) + '\n')
