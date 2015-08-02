from flask import Flask, render_template
app = Flask(__name__)

@app.route('/person/', methods=['POST'])
def index():
	return 'HTTP 201'

if __name__ == '__main__':
    app.run(debug=True)
