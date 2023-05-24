import matplotlib.pyplot as plt
root_path = "D:\\document\\gradu\\自测数据分析"
import sys
sys.path.append( root_path )
from read_file import Read
from k_points_average import *
import os
from merge import *
from sklearn.cluster import dbscan
from dbscan import *
import numpy as np
import seaborn as sns

def Get_bw(freq , l , r , level): #获取频谱中某一段的level dB带宽
    f_max = max(freq[l:r+1])
    limit = f_max - level
    if ( freq[l]>limit or freq[r]>limit ): return -1.0

    while (freq[l+1]<limit): l+=1
    while (freq[r-1]<limit): r-=1
    dl = float(l) + (limit-freq[l])/(freq[l+1]-freq[l])
    dr = float(r) - (limit-freq[r])/(freq[r-1]-freq[r])

    return (dr-dl)

def Calc_fea(peaks , cluster_ids):
    num_fea = max(cluster_ids)
    f_fea = []
    A_fea = []
    for c in range(num_fea+1):
        f_avg = 0.0
        A_avg = 0.0
        num_p = 0
        for p in range( len(cluster_ids) ):
            if (cluster_ids[p] == c):
                num_p += 1
                A_avg += peaks[p][1]
                f_avg += peaks[p][0]
        f_fea.append(f_avg/num_p)
        A_fea.append(A_avg/num_p)
    return f_fea , A_fea

def Calc_lr(freq , peak): #对于某峰值, 求两侧谷的位置(已是端点则返回自身)
    length = len(freq)
    l = peak
    r = peak
    while ( l>0 and freq[l-1]<freq[l] ): l -= 1
    while ( r<length-1 and freq[r+1]<freq[r] ): r += 1
    return (l,r)

def Work_bw(idx , place , level):
    res = 5000/600
    freq = Preprocess( Read(idx) , res)
    l,r = Calc_lr(freq , place)
    return Get_bw(freq , l , r , level)

def Plot_hist(img_path , data):
    plt.figure()
    sns.displot( data=data, kind='hist' , kde=False , binwidth=2.5 , bins=10 )
    plt.savefig(img_path , dpi = 300)
    plt.close()

def Bw_anal(batch_id):
    batch_size = 50
    res = 5000/600
    freq_list = []
    for cnt in range( (batch_id-1)*batch_size+1 , batch_id*batch_size+1 ):
        freq_list.append( Read(cnt) )
    
    idx , peaks , cluster_ids = Work_dbscan(freq_list , res)
    cur = (batch_id-1)*batch_size
    f_fea , A_fea = Calc_fea(peaks , cluster_ids)
    wave_id = np.argmin(f_fea)
    #频率最低为波浪

    db_list = [3,6,10]
    db_bw = []
    for level in db_list:
        bws = []
        for i in range( len(cluster_ids) ):
            if (cluster_ids[i] == wave_id):
                bw = Work_bw(cur+idx[i] , peaks[i][0] , level)
                if (bw>0.0): bws.append(bw)
        db_bw.append(bws)
    
    return db_bw

if __name__ == "__main__":
    
    for batch_id in range(1,7):
        db_bw = Bw_anal(batch_id)
