''' Message bus implementation
'''
import copy

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class MsgBus(object):
    ''' Message bus '''
    def __init__(self,):
        self._subscriptions = {}

    def subscribe(self, token, subject, owner, func):
        ''' Subscribe a bus message listener

        :param token: token
        :param subject: message subject to listen
        :param owner: listener
        :param func: callback function func(token, subject, message)
        '''
        log.info('subscribe(%s, %s, %s, %s)', str(token), str(subject), str(owner), str(func))
        if not owner in self._subscriptions:
            self._subscriptions[owner] = {}
        if not token in self._subscriptions[owner]:
            self._subscriptions[owner][token] = {}
        self._subscriptions[owner][token][subject] = func

    def publish(self, subject, message):
        ''' Send messade to all subscribers

        :param subject: message subject
        :param message: message data
        '''
        log.debug('publish(%s, %s)', str(subject), str(message))
        for owner in self._subscriptions.keys():
            for token in self._subscriptions[owner].keys():
                if subject in self._subscriptions[owner][token]:
                    self._subscriptions[owner][token][subject](token, subject, copy.deepcopy(message))

    def unsubscribe(self, token, subject, owner):
        ''' Unsubscribe a bus message listener

        All parameters must be the same that was used for subscribe

        :param token: token
        :param subject: message subject to listen
        :param owner: listener
        '''
        log.info('unsubscribe(%s, %s, %s)', str(token), str(subject), str(owner))
        if not owner in self._subscriptions:
            raise Exception('no subscriptions for this owner')
        if not token in self._subscriptions[owner]:
            raise Exception('unknown token')
        if not subject in self._subscriptions[owner][token]:
            raise Exception('no subscription')
        del self._subscriptions[owner][token][subject]
        if not len(self._subscriptions[owner][token]):
            del self._subscriptions[owner][token]
        if not len(self._subscriptions[owner]):
            del self._subscriptions[owner]

    def unsubscribe_all(self, owner):
        ''' Unsubscribe all listeners of one owner

        :param owner: listener
        '''
        log.info('unsubscribe_all(%s)', str(owner))
        if owner in self._subscriptions:
            del self._subscriptions[owner]

    def __str__(self):
        s = 'Subscriptions:'
        for owner in self._subscriptions.keys():
            s += '  ' + str(owner) + ':\n'
            for token in self._subscriptions[owner].keys():
                s+= '    token=' + str(token) + ', subscriptions=' + ','.join(self._subscriptions[owner][token].keys()) + '\n'
        return s
