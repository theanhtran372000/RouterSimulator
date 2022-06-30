from re import L
from struct import pack
import numpy as np
import time
import threading
import logging

from ip_generator import IPGenerator

logging.basicConfig(filename="output.log", format="%(message)s", level=logging.DEBUG)

class Router():
    def __init__(self, inputs, routing_table, life_time=5):
        self.inputs = inputs
        self.routing_table = routing_table
        self.life_time = life_time
    
    def input_thread(self, index):
        for _ in range(self.life_time):
            # Get packet
            input = self.inputs[index]
            packet = input.get_packet()
            print('Input {}: Get a new packet {}!'.format(input.name, packet.id))
            packet.print()
            
            # Routing table
            output = self.routing_table.get_next_hop(packet.destination)
            
            # Transfer packet to output
            output.add(packet)
            output.process()
            logging.error('Output {}: Finish processing IP packet {}!'.format(output.name, packet.id))
            logging.error(packet.to_string())
    
    def run(self):
        threads = []
        
        for i in range(len(self.inputs)):
            thread = threading.Thread(target=self.input_thread, args=(i,))
            thread.start()
            threads.append(thread)
            
        for i in range(len(self.inputs)):
            threads[i].join()
            
        print('Done!')
        

class Input():
    def __init__(self, name, ip_generator):
        self.name = name
        self.ip_generator = ip_generator
        
    def get_packet(self):
        return self.ip_generator()


class Output():
    def __init__(self, name, buff):
        self.name = name
        self.buffer = buff
        
    def add(self, ip_packet):
        self.buffer.append(ip_packet)
    
    def random_process_wait(self):
        t = np.random.exponential()
        time.sleep(t)
    
    def process(self):
        self.random_process_wait()
        packet = self.buffer.pop()
        print('Process: ')
        packet.print()
    

class RoutingTable():
    def __init__(self, route_list):
        self.route_list = route_list # dict: prefix -> Output
        
    def get_next_hop(self, destination):
        for prefix in self.route_list.keys():
            if self.check_prefix(destination, prefix):
                return self.route_list[prefix]
        
    def check_prefix(self, ip, prefix):
        comps = prefix.split('.')
        
        output = []
        for a in comps:
            if a != '0':
                output.append(a)
                
        output = '.'.join(output)
        
        return output in ip


class Buffer():
    def __init__(self, size=1024):
        self.buffer = []
        self.size = size
        
    def append(self, ip_packet):
        if len(self.buffer) > self.size:
            pass
        else:
            self.buffer.append(ip_packet)
            
    def pop(self):
        if len(self.buffer) > 0:
            return self.buffer.pop(0)
        else:
            return None
        
if __name__ == '__main__':
    ip_generator = IPGenerator(
        [
            '192.168.1.0',
            '10.0.0.0',
            '172.16.0.0'
        ],
        payload_size=1024
    )
    
    inputs = [Input("Input {}".format(i), ip_generator) for i in range(3)]
    outputs = [Output("Output {}".format(i), Buffer()) for i in range(3)]
    
    routing_table = RoutingTable({
        "192.168.1.0": outputs[0],
        "172.16.0.0": outputs[1],
        "10.0.0.0": outputs[2]
    })
    
    router = Router(inputs, routing_table)
    router.run()
    
    
    
    