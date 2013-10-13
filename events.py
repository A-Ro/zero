channels = {}

def user_join(message):
    print(message)
    channel = message[2][:-1]
    print(channel)
    user = message[1].split('!')[0]
    if user == 'cero':
        channels[channel] = {}
        print(channels)
        just_joined = channel
        print("Joined channel " + channel)
        time.sleep(5)
        return "WHO %s\r\n" % channel
    else:
        return "WHO %s\r\n" % user

def invite(message):
    channel = message[2]
    return "JOIN %s\r\n" % channel #WHO %s" % (channel, channel)

def who_reply(message):
#    print(message)
    msg = message[1].split()
    channel = msg[3]; 
    usernick = msg[7];
    username = msg[4];
    userhost = msg[5]
    userflags = msg[8]
    userrole = ''
    if userflags[-1] in ['~', '%', '&', '+', '@']:
        userrole = userflags[-1]
#        userflags = userflags[-1:]
#    print(username, userhost, userrole, userflags)
    channels[channel][usernick] = {'uname': username, 'uhost': userhost, 'urole': userrole, 'uflags': userflags}
#    print(channels)
    return

def user_part(message):
    pass

def user_gone(message): # this is assuming KICK an PART follow same format
    """User parted/kicked"""
    channel = message[2][:-1]
    user = message[1].split('!')[0]
    if user != 'cero':
        del channels[channel][user]
    else: del channels[channel]    
    pass

def user_quat(message):
    # checked; server kills/klines are also QUITs 
    channel = message[2][:-1]
    user = message[1].split('!')[0]
    if user != 'cero':
        del channels[channel][user]
    pass

def user_nick(message):
    """When a user changes their nick remap their entry in chan dict
    to their new nick"""
    nickorig = message[1].split('!')[0].strip()
    nicknew = message[2].strip()
#    print(channels)
    for item in list(channels.keys()):
        if nickorig in list(channels[item].keys()):
            channels[item][nicknew] = channels[item][nickorig]
            del channels[item][nickorig]

def privmsg(message):
    pass

def notice(message):
    """For integrating services functionality"""
    pass

handledTypes = {'JOIN': user_join, 'PART': user_part, 'INVITE': invite,
    '352': who_reply, 'QUIT': user_quat, 'PART': user_gone, 'KICK': user_gone,
    'NICK': user_nick}

def handler(raw_message):
    message = raw_message.split(':')
    try:
        messageType = message[1].split()[1].strip()
        if messageType in list(handledTypes.keys()):
            return handledTypes[messageType](message)
        else: return
    except:
        messageType = message[0].strip()
        if messageType == 'PING':
            return "PONG %s\r\n" % message[1]