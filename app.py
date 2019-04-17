from flask import Flask, render_template, request, url_for, session, redirect, flash,make_response
import requests
import json
from flask_mysqldb import MySQL
import functools
# from flask_oauth import OAuth
from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery
import urllib.request
import os

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
CLIENT_ID = '952741789324-7bjgjv478nonvtrujqf7aurpkpprpt2m.apps.googleusercontent.com'
CLIENT_SECRET = 'YejsARKSxYR-WhDe2nF2p0QS'
REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console
# FN_BASE_URI - 'http://localhost:5000'
ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'
AUTHORIZATION_SCOPE ='openid email profile'
# AUTH_REDIRECT_URI = os.environ.get("REDIRECT_URI", default=False)
AUTH_REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback' # one of the Redirect URIs from Google APIs console
BASE_URI = 'http://127.0.0.1:5000'
AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'
USER_INFO_KEY = 'user_info'

app = Flask(__name__)
#in order to use sessions you need to use session keys
app.secret_key = 'development key'

# config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Init MySQL
mysql = MySQL(app)


# the destination of the text directory
text =  "C:\\Users\\STEALTH\\Documents\\Python\\Newsapp\\text"

@app.route('/')
def home():
    # Use request to get the data from news api for the top headlines
    # r = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    # data = r.json()

    # retreive the data from the file that has the top news from news api
    with open(os.path.join(text, "news.txt"), "r") as file_x:
        if file_x.mode == 'r':
            contents = file_x.read()
            data = json.loads(contents)
            # print(temp[0])

        file_x.close()
    # Acess the title of the first element using the below statement
    # return data['articles'][0]['title']

    # article = data['articles'][:15]         #First 15 elements
    article = data['articles']         #All elements
    print("article in home:", len(article))
    print("article type:", type(article))
    access_token = session.get('access_token')

    if not is_logged_in():
        return render_template('alpha.html', data = article)
    else:
        if 'email' in session:
            return render_template('alpha.html', data = article, email = session['email'])
        else:
            return render_template('alpha.html', data = article)


@app.route('/category/<id>')
def category(id):
    list = ['business','sports','health','sports','science','technology']
    if id in list:
        print(id)
        print("in list")

        # To retreive data from text file
        part2 = '.txt'
        category_file = ''.join([id,part2])
        print (category_file)
        with open(os.path.join(text, category_file), "r") as file_c:
            if file_c.mode == 'r':
                contents = file_c.read()
                data = json.loads(contents)
                # print(temp[0])

            file_c.close()

        # article = data['articles'][:15]         #First 15 elements
        article = data['articles']                #All elements to be send to the template

        access_token = session.get('access_token')

        # if not 'access_token' in session:
        if access_token is None:
            return render_template('alpha.html', data = article)

        # Request user info from google so that we could display welcome %username% after login
        else:
            # email = getAccess(access_token)
            return render_template('alpha.html', data = article, email = session['email'])
    else:
        return '',204


def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache_impl, view)

@app.route('/login')
@no_cache
def login():
    session_outh = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE, redirect_uri=AUTH_REDIRECT_URI)

    uri, state = session_outh.create_authorization_url(AUTHORIZATION_URL)

    session[AUTH_STATE_KEY] = state
    print("state:",session[AUTH_STATE_KEY])
    print("state type:",type(session[AUTH_STATE_KEY]))
    session.permanent = True
    print("uri:",uri)
    return redirect(uri, code=302)

@app.route(REDIRECT_URI)
@no_cache
def authorized():
    print("Inside authorized")

    req_state = request.args.get('state', default=None, type=None)
    print('req_state:',type(req_state))
    print('req_state:',req_state)
    print("session:",session[AUTH_STATE_KEY])
    if req_state != session[AUTH_STATE_KEY]:
        response = make_response('Invalid state parameter', 401)
        return response
    else:
        session_outh = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                                scope=AUTHORIZATION_SCOPE,
                                state=session[AUTH_STATE_KEY],
                                redirect_uri=AUTH_REDIRECT_URI)

        oauth2_tokens = session_outh.fetch_access_token(
                            ACCESS_TOKEN_URI,
                            authorization_response=request.url)

        session[AUTH_TOKEN_KEY] = oauth2_tokens
        session['logged_in'] = True
        user_info = get_user_info()
        session['email'] = user_info['email']
        print(session['email'])
        return redirect(url_for('home'), code=302)

        # email = getAccess(session['access_token'])
        # print('email outside the getAccess function:',email)

        # return redirect(url_for('home'))


@app.route('/logout')
def logout():
    # revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
    #   params={'token': session['access_token']},
    #   headers = {'content-type': 'application/x-www-form-urlencoded'})
    # status_code = getattr(revoke, 'status_code')
    # if status_code == 200:
    #     session.pop('access_token', None)
    #     session.pop('logged_in', None)
    #     return('Credentials successfully revoked.')
    # else:
    #     return('An error occurred.')
    # # session.clear()

    session.pop(AUTH_TOKEN_KEY, None)
    session.pop(AUTH_STATE_KEY, None)
    session.pop(USER_INFO_KEY, None)
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('url', None)

    return redirect(BASE_URI, code=302)

    # return redirect(url_for('home'))

# this function is called when a logged in user clicks on any news link
@app.route('/receiver', methods = ['POST'])
def receive():
    data = request.get_json(force=True)
    print (data)

    if 'access_token' in session:
        print("Inside receiver:",session['email'])
        session['url'] = data['data']
        email = session['email']
        print(email)
        # database call start
        #Intialize cursor
        cur_int = mysql.connection.cursor()
        # sqlId = cur_int.execute("(SELECT id FROM users WHERE email = %s)" % session['email'])
        sql = "(SELECT id FROM `users` usr WHERE usr.email = %s)"
        par = (email,)
        cur_int.execute(sql,par)
        sqlId = cur_int.fetchone()
        print(sqlId['id'])
        session['id'] = sqlId['id']
        mysql.connection.commit()
        cur_int.close()

        cur = mysql.connection.cursor()
        # #Execute
        # cur.execute("INSERT IGNORE INTO links (id,title,source,url,articledate,content,description) SELECT id,%s,%s,%s,%s,%s,%s FROM users WHERE email = %s", (data['title'],data['source'],session['url'],data['articleDate'],data['content'],data['description'],session['email'],))

        cur.execute("INSERT IGNORE INTO links  (id,title,source,url,articledate,content,description) VALUES (%s,%s,%s,%s,%s,%s,%s)",(session['id'],data['title'],data['source'],session['url'],data['articleDate'],data['content'],data['description'],))

        # #Commit to DB
        mysql.connection.commit()
        #
        # #Close the connection
        cur.close()
        # Return a response to the ajax post
        return json.dumps({'status':True}), 200, {'ContentType':'application/json'}

    else:
        # Return a response to the ajax post
        return json.dumps({'status':False}), 200, {'ContentType':'application/json'}

@app.route('/feedback',methods = ['POST'])
def feedback():
    if 'access_token' in session:
        if 'like' not in request.form or 'relevant' not in request.form or 'novelty' not in request.form or 'readability' not in request.form or 'authority' not in request.form :
            flash('please give a valid input!!!', 'error')
            # return redirect(url_for('home'))
        else:
            print(request.form['like'])
            print(request.form['authority'])

            like = request.form['like']
            relevant = request.form['relevant']
            novelty = request.form['novelty']
            readability = request.form['readability']
            authority = request.form['authority']

            # print(type(like))

            # # try:
            # Add the feedback to the database
            #Intialize cursor
            cur = mysql.connection.cursor()
            #Execute
            cur.execute("""UPDATE links SET f_like = %s,f_relevant = %s,f_novelty = %s,f_readability = %s,f_authority = %s WHERE id = %s AND url = %s""",(like,relevant,novelty,readability,authority,session['id'],session['url']))

            #Commit to DB
            mysql.connection.commit()

            #Close the connection
            cur.close()
            # # except (MySQLdb.Error, MySQLdb.Warning) as e:
            # #     print(e)
            # #     return None
        return redirect(url_for('home'))

# this function is called when the tab is active again and time is calculated
@app.route('/timer', methods = ['POST'])
def timer():
    count = request.get_json(force=True)
    print (count)

    if 'access_token' in session:
        email = session['email']
        url = session['url']
        # database call start
        #Intialize cursor
        cur = mysql.connection.cursor()
        #Execute
        cur.execute("""UPDATE links SET time_article = %s WHERE id = %s AND url = %s""",(count['count'],session['id'],session['url']))
        #Commit to DB
        mysql.connection.commit()

        #Close the connection
        cur.close()
        # Return a response to the ajax post
        return json.dumps({'status':True}), 200, {'ContentType':'application/json'}

    else:
        # Return a response to the ajax post
        return json.dumps({'status':False}), 200, {'ContentType':'application/json'}

@app.route('/openurl')
def openurl():
    return render_template('openurl.html')

# Get access to user data from google and store in to the database used by home() and category() if possible
# urllib2 has been deprecated and we user urllib.request to invoke Request , urlopen and URLError
def getAccess(access_token):
    # access_token = session.get('access_token')
    access_token = access_token[0]
    # accessing user info from google
    headers = {'Authorization': 'OAuth '+access_token}
    req = urllib.request.Request('https://www.googleapis.com/oauth2/v1/userinfo',
    None, headers)
    try:
        res = urllib.request.urlopen(req)
    except urllib.request.URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
            return res.read()

    t = res.read()
    temp = json.loads(t)
    print(temp)
    # name = temp['name']
    # create an alert here so that we could inform the user that there was problem with the login
    email = temp['email']
    session['email'] = email

    if email != "" :
        # database call start
        #Intialize cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT IGNORE INTO users (email) VALUES (%s)", (email,))

        #Commit to DB
        mysql.connection.commit()
        print ('email inside getAccess function:', email)
        #Close the connection
        cur.close()
        return email

# Debug method to print the data of the news api result
@app.route('/debug_api_data')
def debug_api_data():
    # r = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    r = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    # print (type(format(data)))
    return format(data['articles'])

def is_logged_in():
    return True if AUTH_TOKEN_KEY in session else False

def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens = session[AUTH_TOKEN_KEY]

    return google.oauth2.credentials.Credentials(
                oauth2_tokens['access_token'],
                refresh_token=oauth2_tokens['refresh_token'],
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                token_uri=ACCESS_TOKEN_URI)

def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
                        'oauth2', 'v2',
                        credentials=credentials)

    return oauth2_client.userinfo().get().execute()




if __name__ == '__main__':
    app.run(debug=True)
