'''
Webapp for Raspberry Pi ZeroW Timelapse camera
'''

from time import time
from flask import Flask, render_template, request
import datetime
import subprocess
import os

app_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

# Initial params for html
state = "START"
awb = 'auto'

# Timelepse params
timelapse = False
end = 0
tl = 0

@app.route("/", methods=['GET', 'POST'])
def index():

    global state
    global awb
    global timelapse
    global end
    global tl

    # Update by each GET
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M:%S")

    # white balance
    awb_list = ['off','auto','sun','cloud','shade','tungsten','fluorescent','incandescent','flash','horizon','greyworld']

    if request.method == 'POST':
        if request.form['submit_button'] == 'SNAPSHOT':
            awb = request.form['awb']
            subprocess.call([app_dir+'/snapshot.sh', awb])
            state = "Snapshot done"

        elif request.form['submit_button'] == 'RUN TIMELAPSE':
            days = request.form['days']
            hours = request.form['hours']
            minutes = request.form['minutes']
            period = request.form['period']
            awb = request.form['awb']
            
            days_ms = int(days) * 24 * 60 * 60 * 1000
            hours_ms = int(hours) * 60 * 60 * 1000
            minutes_ms = int(minutes) * 60 * 1000

            interval_ms = days_ms + hours_ms + minutes_ms
            period_ms = int(period) *1000

            if period_ms < interval_ms:
                print("Timelapse: interval", interval_ms, "period", period_ms)
                tl = subprocess.Popen([app_dir+'/timelapse.sh', awb, str(interval_ms), str(period_ms)])
                timelapse = True
                end = now + datetime.timedelta(milliseconds=interval_ms)
            else:
                state = "Wrong timelapse params"
 
    if timelapse:
        if tl.poll() is None:  
            waiting = end - now
            state = "Processing timelapse until: " + end.strftime("%Y-%m-%d %H:%M:%S") + ", wait: " + str(waiting).split('.', 2)[0]
        else:
            timelapse = False
            state = "Waiting"

    templateData = {
      'title' : 'Timelapse camera',
      'time': timeString,
      'state':state,
      'user_image': '/static/img/snapshot.jpg',
      'awb_list': awb_list,
      'awb_sel': awb
    }

    return render_template('index.html', **templateData)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)

