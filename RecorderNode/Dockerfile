FROM jrottenberg/ffmpeg:4.3.1-ubuntu2004

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN apt-get -qqy update \
    && apt-get -qqy install python3-pip

WORKDIR /video_recorder
COPY entry_point.sh server.py requirements.txt ./

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "./entry_point.sh"]
