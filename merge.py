import matplotlib.pyplot as plt
root_path = "D:\\document\\gradu\\自测数据分析"
import sys
sys.path.append( root_path )
from read_file import Read
from k_points_average import *
import os

def Get_lr( freq , place ): #对于某谷值, 求两侧峰的位置
    length = len(freq)
    l = place
    r = place
    while ( l>0 and freq[l-1]>freq[l] ): l -= 1
    while ( r<length-1 and freq[r+1]>freq[r] ): r += 1
    return (l,r)

def Fix( freq , place ): #用最小的变化填平某处谷值
    fixed = freq
    l,r = Get_lr(freq , place)
    if ( freq[l]>freq[r] ):
        while ( freq[l+1]>freq[r] ): l += 1
    else:
        while ( freq[l]<freq[r-1] ): r -= 1
    for i in range(l+1,r):
        fixed[i] = freq[l] + (freq[r]-freq[l])/(r-l)*(i-l)
    return fixed

def Get_peak(freq): #求频谱的峰值位置(包括两端)
    length = len(freq)
    peak = []
    if (freq[0]>freq[1]): peak.append(0)
    for i in range(1, length-1 ):
        if ( freq[i-1]<freq[i] and freq[i]>freq[i+1] ): peak.append(i)
    if (freq[ length-2 ]<freq[ length-1 ]): peak.append(length-1)
    return peak

def Merge(freq , num , res): #在高于噪声的地方保留num个峰，频谱分辨率为res
    level = 27.0
    area_limit = 1000.0

    noise_db = max(freq) - level
    fixed = freq

    temp = Get_peak(fixed)
    peak = []
    for p in temp:
        if (fixed[p]>noise_db): peak.append(p) #高于噪声的峰才是有意义的峰

    while ( len(peak)>num ):
        temp = Get_valley(fixed)
        vall = []
        for v in temp:
            l,r = Get_lr(fixed , v)
            if ( min(freq[l],freq[r])>noise_db ): vall.append(v) #能使两个特征峰合并的谷值

        bot = []
        for place in vall:
            l,r = Get_lr(fixed , place)

            fixed_height = fixed[l] + (fixed[r]-fixed[l])/(r-l)*(place-l)
            weight = (fixed_height-fixed[place])*(r-l)/2.0
            bot.append( [place , weight] )
            #用三角形面积作为权重
        
        if ( len(bot)==0 ): return fixed
        bot.sort(key = lambda x: x[1])
        if ( bot[0][1]*res>area_limit ): return fixed #三角形面积过大则不合并

        place = bot[0][0]
        fixed = Fix(fixed , place)
        
        temp = Get_peak(fixed)
        peak = []
        for p in temp:
            if (fixed[p]>noise_db): peak.append(p)

    return fixed

if __name__ == "__main__":
    total = 300
    peak_num = 2 #保留的峰数
    resolution = 5000/600
    path = "D:\\document\\gradu\\自测数据分析\\合并后\\"

    for i in range(total):
        cnt = i + 1

        freq = Read(cnt)
        k = Calc_average_len(freq)
        freq = KPointsSmooth(freq , k)
        freq = Merge(freq , peak_num , resolution)

        img_path = path + str(cnt) + ".jpg"
        Plot(img_path , freq)
