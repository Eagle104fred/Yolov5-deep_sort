from KalmanCV import KalmanFilter
import queue


class KalmanBox:
    def __init__(self, maxAge):
        self.predList = []
        self.maxAge = maxAge

    def Predict(self, ids, boxes):
        resultBoxes=[]
        resultId=[]
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = [int(i) for i in box]
            id = int(ids[i]) if ids is not None else 0
            flag = True
            for boxPred in self.predList:
                if (id == boxPred.id):
                    boxPred.Predict(x1, y1, x2, y2)
                    pred_x1=boxPred.predPoint_x1
                    pred_y1=boxPred.predPoint_y1
                    pred_x2=boxPred.predPoint_x2
                    pred_y2=boxPred.predPoint_y2

                    #KS: 过滤初始预测不准的情况
                    if(abs(pred_x1-x1)<50):
                        x1=pred_x1
                    if (abs(pred_y1 - y1) < 50):
                        y1 = pred_y1
                    if(abs(pred_x2-x2)<50):
                        x2 = pred_x2
                    if (abs(pred_y2 - y2) < 50):
                        y2 = pred_y2
                        
                    resultBoxes.append([x1, y1, x2, y2])
                    resultId.append(id)
                    flag = False
            if (flag):
                """
                KS:!!!!!!!!!!!!!bug!!!!!!!!!!!!!!!!!!!
                    这个地方新建了之后应该马上投入计算, 晚点修复 
                """
                self.predList.append(KfBox(id,x1, y1, x2, y2,self.maxAge))
        return resultId, resultBoxes



    def UpdateAllAge(self):
        for box in self.predList:
            if(box.age<=0):
                self.predList.remove(box)
            box.UpdateAge()


"""
KS:单个卡尔曼追踪器定义 
"""


class KfBox:
    def __init__(self, id, x1,y1,x2,y2, age):
        self.age = age
        self.id = id
        self.kf_p1 = KalmanFilter()
        self.kf_p2 = KalmanFilter()
        self.predPoint_x1 = x1
        self.predPoint_y1 = y1
        self.predPoint_x2 = x2
        self.predPoint_y2 = y2

    def UpdateAge(self):
        self.age -= 1

    def Predict(self, x1,y1,x2,y2):
        self.predPoint_x1, self.predPoint_y1 = self.kf_p1.Update(x1, y1)
        self.predPoint_x2, self.predPoint_y2 = self.kf_p2.Update(x2, y2)
        self.age += 10
