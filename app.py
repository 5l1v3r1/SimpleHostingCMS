#!/usr/bin/python
'''
A basic bottle app skeleton
'''
import MySQLdb
from mysql_check import db
from datetime import datetime
from bottle import *

app = application = Bottle()
cur = None
debug = True

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_settings():
    settings = {'logo_path': '..'}
    cur = db.query("SELECT path,width,height FROM settings WHERE option_name='logo'")
    settings['logo_path'], settings['logo_width'], settings['logo_height'] = cur.fetchone()
    return settings

@app.route('/static/<filename:path>')
def static(filename):
    '''
    Serve static files
    '''
    #return static_file(filename, root='{}/static'.format(conf.get('bottle', 'root_path')))
    return static_file(filename, root='./static')

##################################
######## Index Page ##############
@app.route('/')
def show_index():
    '''
    The front "index" page
    '''
    return template('hosting', name='index', menu_data=menu(),
        logined=logined(), user=get_username(), settings=get_settings())


##################################
######## login ###################
@app.get('/login') 
def login():
    return template('login_form', settings=get_settings())

@app.post('/login') # or @route('/login', method='POST')
def do_login():
    # !!! NEED VALIDATE INPUT !!!
    username = request.forms.get('username')
    password = request.forms.get('password')
    destination_url = request.headers.get('Referer','/').strip()

    if check_passwd(username, password):
        auth_hash = id_generator()
        cur = db.query("SELECT user_id FROM users WHERE login='%s'" % username)
        user_id = int(cur.fetchone()[0])
        response.set_cookie('id', str(user_id))
        response.set_cookie('hash', str(auth_hash))
        response.set_cookie('logged_at', str(datetime.now()))
        cur = db.query("UPDATE users SET cookies='%s' WHERE login='%s'" % (auth_hash, username))
        redirect(destination_url)
    else:
        return "<p>Login failed.</p>"

def check_passwd(login, password):
    customer = customer_exist(login)[0]
    if debug: print colors.HEADER, 'HASH FROM DB   ', colors.FAIL, customer , colors.ENDC
    if customer: # exist
        salt_end = customer.rindex('$')
        salt = customer[:salt_end]
        import crypt;
        crypted_pass_hash = crypt.crypt(password, salt)
        if debug: print colors.HEADER, 'HASH FROM CRYPT', colors.FAIL, crypted_pass_hash, salt , colors.ENDC
        if crypted_pass_hash == customer:
            return 1
        else:
            print("Login Failed: "+login, password)
            return 0
    else:
        print("No user found: "+login)
        pprint(customer)
        return 0
        
def logined():
    user_id = request.cookies.get('id')
    user_hash = request.cookies.get('hash')
    if user_id:
        if debug: print colors.HEADER, 'USER ID:', colors.FAIL, user_id , colors.ENDC
        cur = db.query("SELECT cookies FROM users WHERE user_id=%d" % int(user_id))
        cookie = cur.fetchone()[0]
        if debug: print colors.HEADER, 'COOKIE:', colors.FAIL, cookie, user_hash , colors.ENDC
        if cookie == user_hash:
            return 1

    return 0

def get_username():
    user_id = request.cookies.get('id')
    if user_id:
        cur = db.query("SELECT login FROM users WHERE user_id=%d" % int(user_id))
        return cur.fetchone()[0]

    return "LOL"

def customer_exist(customer_name):
    cur = db.query("SELECT p_hash FROM users WHERE login='%s'" % str(customer_name))
    return cur.fetchone()
######## login end ###################
######################################

######################################
######## logout ######################
@app.post('/logout')
def do_logout():
    response.set_cookie('id', '', expires=0)
    destination_url = request.headers.get('Referer','/').strip()
    redirect(destination_url)

######## logout end ##################
######################################


#####################################
######## Register ###################
@app.get('/register')
def register_form():
    return template('register', user_exist=0, menu_data=menu(), settings=get_settings())

@app.post('/register')
def do_register():
    email = request.forms.get('email')
    name = request.forms.get('name')
    password = request.forms.get('password')
    destination_url = request.headers.get('Referer','/').strip()

    if not mail_exist(email):
        import crypt;  
        salt = '$6$FIXEDS'
        pass_hash = crypt.crypt(password, salt)
        if debug: print colors.OKBLUE, pass_hash, colors.ENDC
        sql = "INSERT INTO users (login, email, password, p_hash) VALUES ('{}', '{}', '{}', '{}')".format(name, email, password, pass_hash)
        if debug: print colors.OKBLUE, sql, colors.ENDC
        db.query(sql)
        send_email('./mails/grats_to_register.txt', 'register_grats', email)
        send_email('./mails/admin_registered_notify.txt', 'admin_register_notify', email)
        ###
        redirect('/')
    else:
        return template('register', user_exist=1, menu_data=menu(), settings=get_settings())

def mail_exist(email):
    cur = db.query("SELECT user_id FROM users WHERE email = '%s'" % email)
    user_exists = cur.fetchone()
    if user_exists:
        return 1
    else:
        if debug: print colors.HEADER,"No user found:", colors.OKGREEN, email, colors.ENDC
        return 0
######## Register end ###############
#####################################

@app.route('/order/:page_name')
def show_order(page_name):
    '''
    Return a page that has been rendered using a template
    '''
    if logined():
        user_id = request.cookies.get('id')
        # get mail
        cur = db.query("SELECT email FROM users WHERE user_id = %s" % user_id)
        email = cur.fetchone()[0]; 
        send_email(page_name, 'order_grats', email)
        send_email(page_name, 'admin_order_notify', email)
        return template('order', name=page_name, settings=get_settings(),
            menu_data=menu(), logined=logined(), user=get_username())
    else:
        return template('order_deny', name=page_name, settings=get_settings(),
            menu_data=menu(), logined=logined())

@app.route('/:razdel/:page_name')
def show_page(razdel, page_name):
    resp=str(response.status_code)
    return template(razdel, name=page_name, settings=get_settings(),
            menu_data=menu(), logined=logined(), user=get_username(), response=resp)

##################
###### test ######
#@app.route('/menu')
def menu():
    menu_content = []
    sections = []
    counter = 0
    menu_sections = db.query("SELECT section_id,title,targetclass,link FROM menu_sections")
    for section in menu_sections:
        menu_element = []
        sections.append(section)
        if debug: print colors.HEADER, 'MENU SECTION ID:', colors.FAIL, section[0] , colors.ENDC
        mc = db.query("SELECT * FROM menu_content WHERE section_id = %d" % section[0])
        cur = db.query("SELECT count(*) FROM menu_content WHERE section_id = %d" % section[0])
        menu_column_nums = int(cur.fetchone()[0])
        if debug: print colors.HEADER, 'MENU COLUMN NUMBER:', colors.FAIL, menu_column_nums , colors.ENDC
        for n in range(menu_column_nums):
            menu_content_cache = mc.fetchone()
            try:
                menu_content_column = {'title': 'bla'} ## Initializing
                menu_content_column['title'] = menu_content_cache[0]
                menu_content_column['description'] = menu_content_cache[1]
                menu_content_column['price'] = menu_content_cache[2]
                menu_content_column['link'] = menu_content_cache[3]
                menu_content_column['section_id'] = menu_content_cache[5]
                menu_element.append(menu_content_column)

                if debug == 'off':
                  print '============Begin+=========='
                  print colors.OKBLUE,section[0], colors.HEADER,'title      ', colors.OKGREEN, menu_content_column['title'], colors.ENDC
                  print colors.OKBLUE,section[0], colors.HEADER,'description', colors.OKGREEN, menu_content_column['description'], colors.ENDC
                  print colors.OKBLUE,section[0], colors.HEADER,'price      ', colors.OKGREEN, menu_content_column['price'], colors.ENDC
                  print colors.OKBLUE,section[0], colors.HEADER,'link       ', colors.OKGREEN, menu_content_column['link'], colors.ENDC
                  print colors.OKBLUE,section[0], colors.HEADER,'section_id ', colors.OKGREEN, menu_content_column['section_id'], colors.ENDC
                  print '============End============='

            except TypeError:
                if debug: print colors.HEADER, 'SKIPPING ', colors.FAIL, menu_content_cache , colors.ENDC
                continue
                #pass

        if not menu_element == []: #not empty
            menu_content.append(menu_element)
        else:
            if debug: print colors.HEADER, 'SKIPPING append', colors.FAIL, menu_element , colors.ENDC

    menu_data = [sections, menu_content]
    if debug: 
        for data in menu_data[1]:
            print colors.HEADER, 'RESULT ', colors.FAIL, data[0]['title'] , colors.ENDC

    return menu_data

################
### Coockies ###
@app.route('/counter')
def counter():
    count = int( request.cookies.get('counter', '0') )
    count += 1
    response.set_cookie('counter', str(count))
    return 'You visited this page %d times' % count
################

@app.route('/hello/:name')
def hello(name):
    return 'Hello %s' % name

@app.route('/db/:name')
def db_check(name):
    cur = db.query("SELECT login,password FROM users WHERE login = '%s'" % name)
    ret = 'User not Found'
    for row in cur.fetchall():
        if row:
            ret = row[1]

    return ret

###### test end ######
######################

def send_email(message_file, mtype, mailto):
    # Import smtplib for the actual sending function
    import smtplib
    # Import the email modules we'll need
    from email.mime.text import MIMEText

    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
#    fp = open(message_file, 'rb')
    # Create a text/plain message
#    msg = MIMEText(fp.read())
#    fp.close()

    # me == the sender's email address
    # you == the recipient's email address
    if mtype == 'register_grats':
        cur = db.query("SELECT login FROM users WHERE email = '%s'" % mailto)
        text = 'Thanks for register\\n \
        %s' % mailto
        msg = MIMEText(text)
        msg['Subject'] = 'Thanks for register %s' % cur.fetchone()
        msg['From'] = 'registrator@itjunky.ws'
        msg['To'] = mailto
    elif mtype == 'admin_register_notify':
        text = 'New user registered\\n \
        %s' % mailto
        msg = MIMEText(text)
        msg['Subject'] = 'Mew user registered %s' % mailto
        msg['From'] = 'admin@itjunky.ws'
        msg['To'] = 'alphaQu4z4r@gmail.com'
    elif mtype == 'order_grats' :
        cur = db.query("SELECT login FROM users WHERE email = '%s'" % mailto)
        user = cur.fetchone()[0]
        print colors.HEADER, 'DBG:', colors.OKBLUE, message_file, colors.OKGREEN, user, colors.ENDC
        text = "{} thanks for new order in queue {}".format(user, message_file)
        msg = MIMEText(text)
        msg['Subject'] = 'Thanks for order %s' % message_file
        msg['From'] = 'order@itjunky.ws'
        msg['To'] = 'alphaQu4z4r@gmail.com'
    elif mtype == 'admin_order_notify':
        text = "New order queued\\r\\n \
        {} by {}".format(message_file, mailto)
        msg = MIMEText(text)
        msg['Subject'] = 'New order queued %s' % mailto
        msg['From'] = 'admin@itjunky.ws'
        msg['To'] = 'alphaQu4z4r@gmail.com'

    if debug:
        print colors.HEADER, 'Try MAIL sending'
#        print colors.HEADER, 'From:', colors.FAIL, msg['From']
#        print colors.HEADER, 'To:', colors.FAIL, msg['To']
        print colors.OKBLUE, msg.as_string(), colors.ENDC 
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    if debug: print colors.HEADER, 'End MAIL sending', colors.ENDC 
    s.quit()

import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

if __name__ == '__main__':
    run(app=StripPathMiddleware(app),
        host='0.0.0.0',
        port=8080,
        reloader=True)
