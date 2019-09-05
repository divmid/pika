#! /usr/bin/env python2.7
# coding=utf-8
import subprocess

from retrying import retry
from .websocket_server import WebsocketServer
@retry(stop_max_attempt_number=3)
def service_stop():
    # 关闭监控
    # 关机
    subprocess.call(
        "systemctl stop mysqld;"
        "systemctl stop rabbitmq-server;"
        "systemctl stop redis;"
        "init 0",
        shell=True,
        stdout=subprocess.PIPE
    )


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    print("Client(%d) said: %s, client:%s" % (client['id'], message, client))
    server.send_message(client, "关机")
    service_stop()


if __name__ == "__main__":
    PORT = 9001
    server = WebsocketServer(PORT)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
