## M1 Arch
```shell
$ docker-compose up
Creating network "m1_arch_default" with the default driver
Creating selenium-hub ... done
Creating m1_arch_chrome2_1 ... done
Creating m1_arch_chrome1_1 ... done
Creating m1_arch_chrome0_1 ... done
```

```shell
$ docker ps
CONTAINER ID   IMAGE                                  
d10740542a7e   seleniarm/node-chromium:4.10.0-20230615
a3159ec6bab2   seleniarm/node-chromium:4.10.0-20230615
c04e50458fda   seleniarm/node-chromium:4.10.0-20230615
84e0aeed02b8   seleniarm/hub:4.10.0-20230615
```