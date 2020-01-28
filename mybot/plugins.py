from slackbot.bot import listen_to
import requests
import os

datafile = os.environ['DATAFILE']

with open(datafile, 'r') as f:
    d = f.readlines()
    users = [l.rstrip() for l in d]


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
            s.append('%s: %s'%(user, ret['accepted_count']))
    return s

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

