class WierdQueue ():
    def __init__(self,len=0,top=''):
        self.len=len
        self.top=top
    
    def enqueue(self,newItem):
        if(self.top==newItem):
            self.len+=1
        else:
            self.dequeue()
        if(self.top==''):
            self.top=newItem
            self.len+=1
            
    def dequeue(self):
        if(self.len>0):
            self.len-=1;
        else:
            self.top=''
            
    @staticmethod
    def main ():
        q=WierdQueue()
        t=['F','F','F','F','F','F','B','B','B','B','B','B','B','B','B','B','B','F']
        for el in t:
            q.enqueue(el)
            print q.len
    
if __name__ == '__main__':
    WierdQueue.main()
    