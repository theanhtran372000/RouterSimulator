import uuid

class IPPacket():
    def __init__(self, source, destination, payload):
        self.id = uuid.uuid4()
        self.source = source
        self.destination = destination
        self.payload = payload
        
    def to_string(self):
        str = ""
        str += '- ' * 34 + '\n' + \
            '| ' + "SOURCE" + ' ' * 26 + 'DESTINATION' + ' ' * 21 + '|' + '\n' + \
                '- ' * 34 + '\n' + \
                    '| ' + self.source + ' ' * (32 - len(self.source)) + self.destination + ' ' * (32 - len(self.destination)) + '|' + '\n' + \
                        '- ' * 34 + '\n' + \
                            '| ' + ' ' * (32 - 7) + "PAYLOAD" + ' ' * (32 - 0) + '|' + '\n' + \
                                '- ' * 34 + '\n'
        
        l = len (self.payload)
        for i in range(0, l, 32):
            str += '| ' + ' '.join(list(self.payload[i : i + 32])) + ' ' * (64 - 2 * len(self.payload[i : i + 32])) + ' |' + '\n'
            
        str += '- ' * 34 + '\n'
        return str
        
    def print(self):
        
        # print('- ' * 34)
        # print('| ' + "SOURCE" + ' ' * 26 + 'DESTINATION' + ' ' * 21 + '|')
        
        # print('- ' * 34)
        # print('| ' + self.source + ' ' * (32 - len(self.source)) + self.destination + ' ' * (32 - len(self.destination)) + '|')
        
        # print('- ' * 34)
        # print('| ' + ' ' * (32 - 7) + "PAYLOAD" + ' ' * (32 - 0) + '|')
        
        # print('- ' * 34)
        # l = len (self.payload)
        
        # for i in range(0, l, 32):
        #     print('|', ' '.join(list(self.payload[i : i + 32])) + ' ' * (64 - 2 * len(self.payload[i : i + 32])), '|')
            
        # print('- ' * 34)
        
        print(self.to_string())
        
if __name__ == '__main__':
    packet = IPPacket('192.168.1.232', '123.123.123.321', '1' * 100 + '0' * 100)
    packet.print()
        
        