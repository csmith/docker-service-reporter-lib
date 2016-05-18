#!/usr/bin/env python3

import time
import etcd


class Connection:


    def __init__(self, host, port, prefix):
        self._client = etcd.Client(host=host, port=port)
        self._prefix = prefix


    def _read(self, key, **kwargs):
        try:
            node = self._client.read(self._prefix + key, **kwargs)
            return node.value if node else None
        except etcd.EtcdKeyNotFound:
            return None


    def _read_recursive(self, key):
        try:
            return self._client.read(self._prefix + key, recursive=True)
        except etcd.EtcdKeyNotFound:
            return None


    def _write(self, key, value):
        self._client.write(self._prefix + key, value)


    def _write_obj(self, prefix, obj):
        for key, value in obj.items():
            new_prefix = "%s/%s" % (prefix, key)

            if isinstance(value, dict):
                self._write_obj(new_prefix, value)
            else:
                self._write(new_prefix, str(value))


    def _delete(self, key):
        try:
            self._client.delete(self._prefix + key, recursive=True)
        except etcd.EtcdKeyNotFound:
            pass


    def wipe(self):
        self._delete('')


    def add_containers(self, new_containers):
        for container in new_containers:
            name = container['name']
            print('Adding container %s' % name)
            self._write_obj('/containers/%s' % name, container)
            for k, v in container['labels'].items():
                self._write('/labels/%s/%s' % (k, name), v)
            for k, v in container['net']['addr'].items():
                self._write('/networks/%s/%s' % (k, name), v)
            self._write('/hosts/%s/%s' % (container['host'], name), name)
        self._notify_update()


    def remove_containers(self, old_containers):
        for container in old_containers:
            name = container['name']
            print('Removing container %s' % name)
            self._delete('/containers/%s' % name)
            for k, _ in container['labels'].items():
                self._delete('/labels/%s/%s' % (k, name))
            for k, _ in container['net']['addr'].items():
                self._delete('/networks/%s/%s' % (k, name))
            self._delete('/hosts/%s/%s' % (container['host'], name))
        self._notify_update()


    def get_label(self, label):
        node = self._read_recursive('/labels/%s' % label)
        if node:
            return {child.key.split('/')[-1]: child.value for child in node.children}
        else:
            return {}


    def _notify_update(self):
        print('Update completed', flush=True)
        self._write('/_updated', time.time())


    def wait_for_update(self):
        original_time = self._read('/_updated')
        new_time = original_time

        while new_time == original_time:
            try:
                new_time = self._read('/_updated', wait=True)
            except etcd.EtcdWatchTimedOut:
                new_time = self._read('/_updated')
            time.sleep(10)

