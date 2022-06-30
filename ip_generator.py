from ip_packet import IPPacket
import numpy as np
import random
import time

class IPGenerator():
    def __init__(self, destinations, payload_size=65535):
        self.destinations = destinations
        self.payload_size = payload_size

    def get_random_payload(self):
        l = random.randint(0, self.payload_size)
        result = ''.join([str(random.randint(0, 1)) for i in range(l)])
        return result
    
    def get_random_destination(self, prefix):
        addrs = prefix.split('.')
        for i in range(len(addrs)):
            if addrs[i] == '0':
                addrs[i] = str(random.randint(0, 255))
        return '.'.join(addrs)
    
    def get_random_source(self):
        addrs = [str(random.randint(0, 255)) for _ in range(4)]
        return '.'.join(addrs)
    
    def get_ip_packet(self):
        dest = random.choice(self.destinations)
        return IPPacket(self.get_random_source(), self.get_random_destination(dest), self.get_random_payload())
    
    def random_generate_ip_packet(self):
        delay_time = np.random.exponential(10)
        time.sleep(delay_time)
        return self.get_ip_packet()
    
    def __call__(self):
        return self.random_generate_ip_packet()
    
if __name__ == '__main__':
    generator = IPGenerator(
        [
            '182.12.1.0',
            '182.12.2.0',
            '182.12.3.0'
        ],
        payload_size=1024
    )
    
    while True:
        packet = generator()
        packet.print()
        print()