import time
open_list=[]
close_list=[]

class Position:
    x=0
    y=0
    def __init__(self,X,Y):
        self.x,self.y = X,Y#必须写成self.x,否则x是一个新的对象，将覆盖self.x
    def __eq__(self,other):#重载== !=函数，self和other可能是None
        if(other and self):
            return self.x == other.x and self.y == other.y
        else: return not(self or other)

#存储地图每点信息Message        
class Msg:
    G = 0
    H = 0
    IsUnk = 1   #此处替代close_list功能，判断某点是否被搜索过。可直接访问，不需在close_list中搜索
    parent = None #Position
    def __init__(self):
        self.G = 0
        self.H = 0
        self.IsUnk = 1
    def GetF(self): #F不适合写成对象，因为G对象时常更新，F依赖于G
        return self.G+self.H

#地图棋盘，内含Position和Msg信息mapx[Position]=Col*Row个Msg
class Board:
    mapx = [] #Msg[ROW][COL]
    def __init__(self,mapp,target_position):
        for i in range(len(mapp)):
            self.mapx.append([])
            for j in range(len(mapp[0])):
                self.mapx[i].append(Msg())  #是Msg()而不是Msg,否则是一个新的对象，mapx中所有信息同步变动
                self.mapx[i][j].IsUnk=1-mapp[i][j]
                # 有很多万法可以估算H值。这里找们使用Manhattan万法，
                # 计算从当前万格横可或纵回移动到达目标所经过的方格数，忽略对角移动，然后把总数乘以10。
                self.mapx[i][j].H = 10*(abs(target_position.x - i) + abs(target_position.y - j))

        # for k in range(len(self.mapx)):
        #     for m in range(len(self.mapx[k])):
        #         print(self.mapx[k][m].H,end=" ")
        #     print('')
        # print('')

    def GetMsg(self,pos):   #根据Position通过mapx获得Msg
        return self.mapx[pos.x][pos.y]
    
def IsInBoard(i,j):
    if(i>=0 and i<len(mapp) and j>=0 and j<len(mapp[i]) and mapp[i][j]==0):
        return 1
    else:
        return 0

def SearchPath(mapp,cp,target_position):
    start_time=time.time()#计时
    board = Board(mapp,target_position)#地图棋盘对象
    board.GetMsg(cp).IsUnk = 0
    open_list.append(cp)
    while(open_list != []):
        # for k in range(len(board.mapx)):
        #     for m in range(len(board.mapx[k])):
        #         if(board.mapx[k][m].parent):
        #             print('p',board.mapx[k][m].parent.__dict__,end=" ")
        #         else: print('p',"                ",end=" ")
        #     print('')
        # print('')
        #取出第一个（F最小，判定最优）位置
        current_position=open_list[0]
        open_list.remove(current_position)
        #close_list.append(current_position)
        #到达
        if(current_position == target_position):
            print("成功找到解")
            tmp=[]#内存储Position   
            while(current_position != None):
                tmp.append(current_position)
                current_position=board.GetMsg(current_position).parent
            tmp.reverse()
            for i in tmp:
                print(str(i.__dict__))
            end_time=time.time()#计时     
            print(end_time-start_time)
            return

        #将下一步可到达的位置加入open_list，并检查记录的最短路径G是否需要更新，记录最短路径经过的上一个点
        #斜（上下左右与此思路相同，只是细节有差）
        for i in [current_position.x-1,current_position.x+1]:
            for j in [current_position.y-1,current_position.y+1]:
                if(IsInBoard(i,j)):
                    new_G=board.GetMsg(current_position).G+14
                    #维护当前已知最短G
                    if(board.mapx[i][j].IsUnk): 
                        board.mapx[i][j].IsUnk=0
                        open_list.append(Position(i,j))
                        board.mapx[i][j].parent=current_position
                        board.mapx[i][j].G=new_G
                        
                    if(board.mapx[i][j].G>new_G):#如果未遍历或需更新
                        board.mapx[i][j].parent=current_position
                        board.mapx[i][j].G=new_G
        #上下
        j=current_position.y
        for i in [current_position.x-1,current_position.x+1]:
            if(IsInBoard(i,j)):
                new_G=board.GetMsg(current_position).G+10
                if(board.mapx[i][j].IsUnk): 
                    board.mapx[i][j].IsUnk=0
                    open_list.append(Position(i,j))
                    board.mapx[i][j].parent=current_position
                    board.mapx[i][j].G=new_G
                    
                if(board.mapx[i][j].G>new_G):#如果未遍历或需更新
                    board.mapx[i][j].parent=current_position
                    board.mapx[i][j].G=new_G
        #左右
        i = current_position.x
        for j in [current_position.y-1,current_position.y+1]:
            if(IsInBoard(i,j)):
                new_G=board.GetMsg(current_position).G+10
                if(board.mapx[i][j].IsUnk): 
                    board.mapx[i][j].IsUnk=0
                    open_list.append(Position(i,j))
                    board.mapx[i][j].parent=current_position
                    board.mapx[i][j].G=new_G
                    
                if(board.mapx[i][j].G>new_G):#如果未遍历或需更新
                    board.mapx[i][j].parent=current_position
                    board.mapx[i][j].G=new_G
        #open_list.sort(key=searchKey(board))
        #对open_list里的内容按F的大小排序
        open_list.sort(key=lambda elem : board.GetMsg(elem).GetF())     

if __name__ == "__main__":
    #定义初始状态
    mapp = [[0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0]]
    #mapp=[[0,0,0],[0,1,0],[0,0,0]]
    start_position = Position(2,1)
    target_position = Position(2,5)
    SearchPath(mapp,start_position,target_position)
