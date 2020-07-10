import importlib
import logging

from ..utils import is_dev
from ..aws import send_msg


class Worker:
    """ Base class in which all workers must inherit """
    def __init__(self, **kwargs):
        self.args = kwargs

    @staticmethod
    def from_sqs(req_data):
        module = importlib.import_module(req_data.get('module_name'))
        cls = getattr(module, req_data.get('class_name'))
        logging.debug(f'Worker created from sqs: {cls}')
        return cls(req_data.get('args'))

    def enqueue(self):
        if is_dev():
            self.process()
        else:
            send_msg(self.to_msg())

    def process(self):
        raise UnimplementedWorkerException("No Worker")

    def to_msg(self):
        msg = {
            'module_name': self.__class__.__module__,
            'class_name': self.__class__.__name__,
            'args': self.args,
        }
        logging.info(f'Preparing message: {msg}')
        return msg


class UnimplementedWorkerException(Exception):
    pass
