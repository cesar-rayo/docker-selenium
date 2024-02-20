## M1 Arch
```shell
$ docker-compose up
...
Creating selenium-hub ... done
Creating test_chrome1_1 ... done
Creating test_chrome0_1 ... done
Creating test_chrome2_1 ... done
```


```shell
$ docker ps
CONTAINER ID   IMAGE                                  
d10740542a7e   seleniarm/node-chromium:4.10.0-20230615
a3159ec6bab2   seleniarm/node-chromium:4.10.0-20230615
c04e50458fda   seleniarm/node-chromium:4.10.0-20230615
84e0aeed02b8   seleniarm/hub:4.10.0-20230615
```