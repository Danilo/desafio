import urllib2
from flaskext.mysql import MySQL
from flask import Flask, request, json, jsonify

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'Desafio'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/person/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        facebookId = request.form['facebookId']
        token = 'CAACEdEose0cBAKXM7fDsQZAoeZBTZBbRXaQPDNdyXllii6FSFkcj6fpEeMHAGKymyslGA9ZAaZAN3dK4Mz6UD8mdHNDNoQlaLBmYTXGZC7eZAKrNR98JkioLtN0mu9qwIpoSsG5jmESab5L0ZC2KdROZBcptJ7sSscAQfxPFJhRbmfaOrGYEYROL82kxuddqaFyyEOk0nwkAFVZA9rzyyyWGrIPfw8W9KsZCmgZD'
        try:
            content = urllib2.urlopen("https://graph.facebook.com/v2.0/%s?access_token=%s" % (facebookId, token))
        except urllib2.HTTPError, err:
            return '{}\n'.format(err)
        data = json.load(content)
        connector = mysql.connect()
        cursor = connector.cursor()
        add_user = ("INSERT INTO Users "
                   "(facebookId, first_name, last_name, name) "
                   "VALUES (\'%s\', \'%s\', \'%s\', \'%s\')") % (data['id'], data['first_name'], data['last_name'], data['name'])
        try:
            cursor.execute(add_user)
            connector.commit()
            cursor.close()
            connector.close()
            return 'HTTP 201\n'
        except connector.Error, err:
            if err.args[0] == 1146:
                try:
                    create_table = ("CREATE TABLE Users "
                    "(facebookId BIGINT NOT NULL, first_name VARCHAR(50), last_name VARCHAR(50), name VARCHAR(100), PRIMARY KEY(facebookId))")
                    cursor.execute(create_table)
                    cursor.execute(add_user)
                    connector.commit()
                    cursor.close()
                    connector.close()
                    return 'HTTP 201\n'
                except connector.Error, err:
                    return ("MySQL Error: {}\n".format(err))
            else:
                return ("MySQL Error: {}\n".format(err))
    elif request.method == 'GET':
        connector = mysql.connect()
        cursor = connector.cursor()
        query = ("SELECT * FROM Users LIMIT %s") % request.args.get('limit', '')

        try:
            cursor.execute(query)
            return "HTTP 200\n%s\n" % (json.dumps(cursor.fetchall(), indent=2))
        except connector.Error, err:
            return ("MySQL Error: {}\n".format(err))

@app.route('/person/<facebookId>/', methods=['DELETE'])
def deletion(facebookId):

    if request.method == 'DELETE':
        connector = mysql.connect()
        cursor = connector.cursor()
        delete = ("DELETE FROM Users WHERE facebookId=%s") % (facebookId)

        try:
            cursor.execute(delete)
            connector.commit()
            cursor.close()
            connector.close()
            return 'HTTP 204\n'
        except connector.Error, err:
            return ("MySQL Error: {}\n".format(err))

if __name__ == '__main__':
    app.run(debug=True)
