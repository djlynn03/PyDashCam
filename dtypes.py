class Frame:
    def __init__(self, frame):
        self.frame = frame
        self.next = None


class FrameQueue:
    def __init__(self, maxsize):
        self.front = None
        self.back = None
        self.maxsize = maxsize
        self.currentsize = 0
        
    def enqueue(self, frame):
        temp = Frame(frame)
        if self.back is not None:
            self.back.next = temp
            self.back = temp
        else:
            self.back = temp
            self.front = temp
        self.currentsize += 1
        
        if self.currentsize > self.maxsize:
            self.dequeue()
            
    def dequeue(self):
        if not self.is_empty():
            rm = self.front
            if self.back is self.front:
                self.front = None
                self.back = None
            else:
                self.front = self.front.next
            self.currentsize -= 1
            return rm.frame
        raise RuntimeError('Queue is empty')

    def peek_front(self):
        if not self.is_empty():
            return self.front.frame
        raise RuntimeError('Queue is empty')
    
    def is_empty(self):
        return self.front is None
    
    def foreach(self, func: callable):
        returnv = None
        jumper = self.front
        while jumper is not None:
            returnv = func(jumper.frame)
            jumper = jumper.next