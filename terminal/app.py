import subprocess
import os
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def execute_command(command):
    if command.startswith('cd'):
        # Change directory
        try:
            path = command.split(' ')[1]
            os.chdir(path)
            session['cwd'] = os.getcwd()
            output = ''
        except Exception as e:
            output = str(e)
    else:
        # Execute other commands
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, cwd=session.get('cwd', None))
            output = result
        except subprocess.CalledProcessError as e:
            output = e.output
    return output

@app.route('/')
def index():
    session['cwd'] = os.getcwd()
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    output = execute_command(command)
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
