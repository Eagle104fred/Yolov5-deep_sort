class IdPool:
    def __init__(self):
        self.id_dict = {}
    def init(self):#检测这个id是否存活
        for i in range(1,9999):
            if(i in self.id_dict.keys()):
                continue
            else:
                self.id_dict[i]=500
                return i
        return 0
    def updat_times(self):
        for k,v in self.id_dict.items():
            v-=1
            print("v:"+v)
            if(v<=0):
                print("release id :" + k)
                del self.id_dict[k]


    def update(self,id):
        self.id_dict[id] = 500