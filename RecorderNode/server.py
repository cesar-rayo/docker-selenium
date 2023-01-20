import json
import os
import subprocess
import signal
from flask import Flask, request

VIDEO_SIZE = "1360x1020"
DISPLAY_NUM = "99"
FRAME_RATE = 15
CODEC = "libx264"
PRESET = "-preset ultrafast"

app = Flask(__name__)


@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    try:
        video_name = data['videoName']
        display_container_name = data['targetDisplay']
        return start_recording(video_name, display_container_name)
    except KeyError as e:
        return app.response_class(
            response=json.dumps(
                {
                    "error": "The request is missing one or more required fields, {}".format(e)
                }
            ),
            status=400,
            mimetype='application/json'
        )


@app.route('/stop', methods=['POST'])
def stop():
    # target = request.form.get('targetFolder')
    return stop_recording()


@app.route('/status', methods=['GET'])
def status():
    return get_server_status()


def start_recording(video_name, display_container_name):
    try:
        if get_ffmpeg_pid():
            file_name = os.environ.get('FILE_NAME')
            raise Exception("ffmpeg is already in use by {}".format(file_name))
        else:
            os.environ['FILE_NAME'] = f'{video_name}.mp4'
            file_name = os.environ.get('FILE_NAME')
            command = f'ffmpeg -nostdin -loglevel panic -y -f x11grab -video_size {VIDEO_SIZE} ' \
                      f'-r {FRAME_RATE} -i {display_container_name}:{DISPLAY_NUM} -codec:v {CODEC} ' \
                      f'{PRESET} -pix_fmt yuv420p "./videos/{file_name}" &'

            subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

            if get_ffmpeg_pid():
                response = app.response_class(
                    response=json.dumps(
                        {
                            "file": file_name,
                            "status": "recording"
                        }
                    ),
                    status=200,
                    mimetype='application/json'
                )
            else:
                raise FFPEGNotRunning("ffmpeg command is not running")
    except Exception as e:
        response = app.response_class(
            response=json.dumps(
                {
                    "file": file_name,
                    "error": "Could not start recording screen for [ {}:{} ], {}".format(
                        display_container_name, DISPLAY_NUM, e)
                }
            ),
            status=500,
            mimetype='application/json'
        )
    return response


def get_ffmpeg_pid():
    command = "ps ax | grep 'ffmpeg -nostdin' | grep -v grep | awk '{print $1}'"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    pid = output.decode()
    return pid


def get_server_status():
    pid = get_ffmpeg_pid()
    file_name = os.environ.get('FILE_NAME')
    data = {}
    try:
        int(pid)
        data['file'] = file_name
        data['status'] = "recording"
    except ValueError:
        data['status'] = "waiting"
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


def stop_recording():
    try:
        file_name = os.environ.get('FILE_NAME')
        pid = get_ffmpeg_pid()
        try:
            os.kill(int(pid), signal.SIGINT)
        except ValueError:
            raise FFPEGNotRunning("Make sure ffmpeg is running")
        response = app.response_class(
            response=json.dumps(
                {
                    "file": file_name,
                    "status": "stopped"
                }
            ),
            status=200,
            mimetype='application/json'
        )
    except FFPEGNotRunning as e:
        response = app.response_class(
            response=json.dumps(
                {
                    "error": "Could not stop the recording, {}".format(e)
                }
            ),
            status=500,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        response = app.response_class(
            response=json.dumps(
                {
                    "file": file_name,
                    "error": "Could not stop the recording, {}".format(e)
                }
            ),
            status=500,
            mimetype='application/json'
        )
    return response


class FFPEGNotRunning(Exception):
    """ ffmpeg command is either not found or not running """
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
