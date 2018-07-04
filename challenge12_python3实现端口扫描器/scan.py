#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
import sys
import socket

def get_args():
    args = sys.argv[1:]
    try:
        #��ò���
        host_index = args.index('--host')
        port_index = args.index('--port')

        host_temp = args[host_index + 1]
        port_temp = args[port_index + 1]
        #�ж�IP��ַ�ĸ�ʽ
        if len(host_temp.split('.')) != 4:
            print('Parameter Error')
            exit()
        else:
            host = host_temp
        #�ж��Ƿ�Ϊ���˿�
        if '-' in port_temp:
            port = port_temp.split('-')
        else:
            port = [port_temp, port_temp]

        return host, port
    except (ValueError, IndexError):
        #������ȡ���󣬴�ӡ������Ϣ���˳�
        print('Parameter Error')
        exit()

def scan():
    host = get_args()[0]
    port = get_args()[1]
    open_list = []
    #ɨ��˿�
    for i in range(int(port[0]), int(port[1]) + 1):
        s = socket.socket()
        #���ó�ʱ����ֹ�ű���ס
        s.settimeout(0.1)
        if s.connect_ex((host,i)) ==0:
            open_list.append(i)
            print(i, 'open')
        else:
            print(i , 'closed')
        s.close()
    #������ڿ���״̬�Ķ˿�
    print('Complted scan. Opening ports at {open_list}'.format(open_list=open_list))

#ִ��
if __name__ == '__main__':
    scan()








