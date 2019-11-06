from time import sleep

from pythonosc import udp_client

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
#
for x in range(10):
    print('send front {0}'.format(x))
    client.send_message("/vest_front", '{0},{1}'.format(x, 100))
    sleep(1)
    print('Send back {0}'.format(x))
    client.send_message("/vest_back", '{0},{1}'.format(x, 100))
    sleep(1)

