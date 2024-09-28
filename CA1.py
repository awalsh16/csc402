from sys import stdin

class inputStream:
    def __init__(self, char_stream=None):
        if not char_stream:
            char_stream = stdin.read()
        clean_stream = char_stream.replace(' ','') \
                                  .replace('\t','') \
                                  .replace('\n','')
        self.stream = [c for c in clean_stream]
        self.stream.append('\eof')
        self.stream_ix = 0
    
    def pointer(self):
        return self.stream[self.stream_ix]
    
    def next(self):
        if not self.end_of_file():
            self.stream_ix += 1
        return self.pointer()
    
    def match(self, sym):
        if sym == self.pointer():
            s = self.pointer()
            self.next()
            return s
        else:
            raise SyntaxError('unexpected symbol {} while parsing, expected {}'.format(self.stream[self.stream_ix], sym))
        
    def end_of_file(self):
        if self.pointer() == '\eof':
            return True
        else:
            return False
        
    def A(stream):
        sym = stream.pointer()
        if sym in ['a']:
            stream.match('a')
            B(stream)
            return
        else:
            return
        
    def B(stream):
        sym = stream.pointer()
        if sym in ['b']:
            stream.match('b')
            A(stream)
            return

    def parse():
        from inputstream import InputStream