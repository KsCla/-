import matplotlib.pyplot as plt
root_path = "D:\\document\\gradu\\自测数据分析"
import sys
sys.path.append( root_path )
from read_file import Read

def Get_valley(freq): #求频谱的谷值位置(不包括两端)
    length = len(freq)
    vall = []
    for i in range(1, length-1 ):
        if ( freq[i-1]>freq[i] and freq[i]<freq[i+1] ): vall.append(i)
    return vall

def Get_lr( freq , place ): #对于某谷值, 求两侧峰的位置
    length = len(freq)
    l = place
    r = place
    while ( l>0 and freq[l-1]>freq[l] ): l -= 1
    while ( r<length-1 and freq[r+1]>freq[r] ): r += 1
    return (l,r)

def Calc_average_len(freq): #选取合适的滑动平均长度
    vall = Get_valley(freq)
    dist = len(freq)/len(vall)
    dist *= 2.0
    dist = dist+1.0
    k = 1
    for i in range( len(freq) ):
        if (i%2==1):
            d = abs(dist - i)
            if (d < abs(dist - k)): k=i
    return k

def KPointsSmooth(freq , k): #k点滑动平均
    length = len(freq)
    avg_freq = []
    l = k//2

    for i in range(l):
        val = 0.0
        for j in range(2*i+1): val += freq[j]
        val /= (2.0*i+1.0)
        avg_freq.append(val)
    
    for i in range(l, length-l ):
        val = 0.0
        for j in range(-l,l+1): val += freq[i+j]
        avg_freq.append( val/k )
    
    for i in range(length-l , length):
        val = 0.0
        for j in range(2*i-length+1 , length): val += freq[j]
        val /= (2.0*(length-i)-1.0)
        avg_freq.append( val )

    return avg_freq

def Plot(img_path , freq):
    plt.figure()
    plt.plot(freq , linewidth =0.5)
    plt.savefig(img_path , dpi = 300)
    plt.close()

if __name__ == "__main__":
    total = 300
    for i in range(total):
        cnt = i+1
        freq = Read(cnt)
        k = Calc_average_len(freq)
        avg_freq = KPointsSmooth(freq , k)

        path = "D:\\document\\gradu\\自测数据分析\\k滑动平均"
        img_path = path + "\\" + str(cnt) + ".jpg"
        Plot(img_path , avg_freq)
