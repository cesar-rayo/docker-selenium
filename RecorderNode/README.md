## Selenium Grid - Video Recorder Service

This is a service that can be used to record a test execution within a browser node of the Selenium Grid cluster.

* In order to be able to consume the service we first need to build the docker image:
```shell
$ docker build -t video-recorder .
```

* Verify the image has been created and registered
```shell
$ docker images
REPOSITORY         TAG        IMAGE ID       CREATED         SIZE
video-recorder     latest     c47e68fe9d18   2 days ago      585MB
```

* Deploy the Selenium Grid either using Helm or docker-compose
* Having the Grid deployed, the new service will be accessible from the port `5001`

### Start a recording:
```shell
$ curl -X POST http://localhost:5001/start -H "Content-Type: application/json" -d '{"videoName":"helm_01202023_160248","targetDisplay":"chrome-display"}'
{"file": "helm_01202023_160248.mp4", "status": "recording"}
```
Here we need to specify the name of the container we want to record from:

For Docker compose we use the container node name like:
* chrome

For Kubernetes we use headless services names like:
* chrome-display

### Check service status:
```shell
$ curl -X GET http://localhost:5001/status
{"status": "waiting"}
```
In case a recording is already running you will get something like this:
```shell
$ curl -X GET http://localhost:5001/status
{"file": "helm_01202023_160248.mp4", "status": "recording"}
```

### Stop a recording:
```shell
$ curl -v -X POST http://localhost:5001/stop
{"file": "test_01202023_160248.mp4", "status": "stopped"}
```

Once the stop request is processed, a new file will be created in the folder we have specified in the shared volumes:
* Docker compose: `video_recorder.volumes`
* Kubernetes: `videoRecorder.videosPath`