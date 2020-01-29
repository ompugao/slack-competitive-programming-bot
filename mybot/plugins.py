from slackbot.bot import listen_to
import requests
import os
import datetime
import io
import json

datafile = os.environ['DATAFILE']

with open(datafile, 'r') as f:
    d = f.readlines()
    users = [l.rstrip() for l in d]

class DataStore(object):
    # TODO: rewrite with sqlite3
    def __init__(self, datafile):
        self.datafile = datafile
        self.read()

    def read(self, ):
        with open(datafile, 'r') as f:
            self.data = json.load(f)

    def write(self,):
        with open(datafile, 'w') as f:
            json.dump(self.data, f)

    @property
    def users(self):
        return self.data['users']

    def user_exists(self, user):
        if user in self.data['users']:
            return False
        return True

    def add_user(self, user):
        if not user in self.data['users']:
            self.data['users'].append(user)
            self.write()
            return True
        return False

    def remove_user(self, user):
        if user in self.data['users']:
            self.data['users'].remove(user)
            self.write()
            return True
        return False

def get_daily_statistics():
    yesterday_midnight = datetime.datetime.combine((datetime.datetime.now().date() - datetime.timedelta(days=1)), datetime.time(hour=0, minute=0, second=0))

    ss = io.StringIO()

    ss.write('Accepted Submissions from %s:\n'%(yesterday_midnight.strftime('%Y/%m/%d %H:%M:%S'),))
    for user in users:
        r = requests.get('https://kenkoooo.com/atcoder/atcoder-api/results?user=%s'%(user,))
        if r.status_code != 200:
            print('submission of user \'%s\' is not fetched'%(user,))
            continue
        submissions = r.json()
        ss.write('- %s: '%user)

        ss2 = io.StringIO()
        inc = 0
        for submission in submissions:
            if submission[u'result'] == u'AC' and submission[u'epoch_second'] > yesterday_midnight.timestamp():
                inc += 1
                ss2.write('%s, '%(submission[u'problem_id']))
        ss.write('+%d! (%s)\n'%(inc, ss2.getvalue()))
    return ss.getvalue()



def get_user_statistics(user):
    r = requests.get('https://kenkoooo.com/atcoder/atcoder-api/v2/user_info?user=%s'%(user,))
    if r.status_code != 200:
        return None
    return r.json()

def get_statistics():
    s = []
    for user in users:
        ret = get_user_statistics(user)
        if ret is not None:
            s.append('- %s: %s'%(user, ret['accepted_count']))
    return s


@listen_to('^help$')
def help(message):
    s = """
    Usage:
    register atcoder user
    `register username`
    unregister atcoder user
    `unregister username`
    see statistics
    `stat`
    or
    `stat username`
    """
    message.reply(s)


@listen_to('^stat$')
@listen_to('^stat (.*)$')
def statistics(message, user=None):
    if user is None:
        s = []
        s.append('')
        s.extend(get_statistics())
        message.reply('\n'.join(s))
    else:
        ret = get_user_statistics(user)
        if ret is not None:
            message.reply('%s\'s AC: %s'%(user, ret['accepted_count']))
        else:
            message.reply('user \'%s\' not found'%user)


@listen_to('^register (.+)')
def register_user(message, user):
    if user in users:
        message.reply('%s is already registered'%user)
        return
    r = requests.get('https://kenkoooo.com/atcoder/atcoder-api/v2/user_info?user=%s'%(user,))
    if r.status_code == 200:
        users.append(user)
        with open(datafile, 'w') as f:
            f.write('\n'.join(users))
        message.reply('%s is registered'%user)
    else:
        message.reply('%s is not found'%user)

@listen_to('^unregister (.+)')
def unregister_user(message, user):
    if user in users:
        users.remove(user)
        with open(datafile, 'w') as f:
            f.write('\n'.join(users))
        message.reply('unregister %s'%(user,))
        return

    r = requests.get('https://kenkoooo.com/atcoder/atcoder-api/v2/user_info?user=%s'%(user,))
    if r.status_code == 200:
        users.append(user)
        with open(datafile, 'w') as f:
            f.write('\n'.join(users))
        message.reply('%s is registered'%user)
    else:
        message.reply('%s is not found'%user)

