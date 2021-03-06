import atexit
import json
import os
from datetime import datetime
from urllib.request import Request, urlopen


class TrainingLogger:
    '''
        Keeps a log for training runs
        * output_path: The path to the folder to which 
        the log will be written
        * slack_url: An optional webhook string for sending
        logs to slack in real time
     '''
    def __init__(self, output_path, slack_url=None):
        self._slack_url = slack_url
        self._date_format = '%d-%-m-%Y %H:%M:%S'
        #self._file = open(os.path.join(output_path, datetime.now().strftime(self._date_format)+'.log'), 'a')
        self._fpath = os.path.join(output_path, datetime.now().strftime(self._date_format)+'.log')
        self.line()
        self.log('Starting a training run')
        self.line()

    def log(self, msg, title=True, slack=False):
        '''
            Prints a string to standard out, saves it to the
            given output file and reports it optionally to a 
            slack channel.

            Input:
            msg: A string
            slack: A boolean
        '''
        print(msg)
        date = datetime.now().strftime(self._date_format)
        if title:
            logged_msg = '[%s]: %s\n' % (date, msg) 
        else:
            logged_msg = '%s\n' % msg
        with open(self._fpath, 'a') as logfile:
            logfile.write(logged_msg)      
        if slack and self._slack_url is not None:
            self._slack_msg(date, msg)

    def _slack_msg(self, title, body):
        '''
            Sends a message with a title and and a body
            to the set slack webhook
        '''
        req = Request(self._slack_url)
        req.add_header('Content-Type', 'application/json')
        urlopen(req, json.dumps({
            'username': 'Tacotron',
            'icon_emoji': ':taco:',
            'text': '*%s*: %s' % (title, body)
        }).encode())
    
    def line(self):
        '''
            Log a line for readability
        '''
        self.log('------------------------------------', 
            title=False, slack=False)