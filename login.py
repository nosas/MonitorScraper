import gmail


def gmail_login():
    gm = gmail.GMail('GMAIL', 'PASSWORD')
    gm.connect()
    return gm