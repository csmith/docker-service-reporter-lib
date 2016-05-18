FROM csmith/service-reporter-lib:dev 
MAINTAINER Chris Smith <chris87@gmail.com> 

RUN \
  pip install \
    nose \
    pylint

WORKDIR /
ENTRYPOINT ["pylint", "--ignored-classes=etcd.EtcdResult", "/etcdlib.py"]
