import matplotlib.pyplot as plt
root_path = "D:\\document\\gradu\\自测数据分析"
import sys
sys.path.append( root_path )
from read_file import *
from k_points_average import *
import os
from merge import *
from sklearn.cluster import dbscan
from sklearn.cluster import k_means
from dbscan import *

def Read_time_seq(cnt):
    dataset = (cnt-1)//100+1
    id = (cnt-1)%100
    path = "D:\\document\\gradu\\自测数据分析\\数据\\" + str(dataset) + "\\新建文件" + str(id) + ".csv"
    with open(path) as file:
        data = file.readlines()
        length = len(data)
        data = data[2:length]
        freq = [float(x.split(",")[1]) for x in data]
        freq = fft(freq)
        freq = abs(freq)
        freq = freq[1:length//2]
        freq = freq/len(freq)
        data = [20.0*log10(x+0.000001) for x in freq]
    return data

def Plot1():
    data1 = [4,3,2,1,2,3]
    freq = [15]
    for i in range(60):
        freq = freq + data1
    img_path = "D:\\document\\gradu\\自测数据分析\\art_pic.jpg"
    Plot(img_path , freq)

def Work_kmeans(freq_list , res , num):
    idx , peaks = Extract(freq_list , res)

    h_convert = 5.0
    w_convert = 100.0
    points = []
    for p in peaks: points.append([ p[0]*res/w_convert , p[1]/h_convert ])

    model = k_means(points, n_clusters=num)

    col = model[1]
    return peaks , col

def Show_kmeans(batch_id , num):
    batch_size = 50
    res = 5000/600
    freq_list = []
    for cnt in range( (batch_id-1)*batch_size+1 , batch_id*batch_size+1 ):
        freq_list.append( Read(cnt) )
    
    peaks , cluster_ids = Work_kmeans(freq_list , res , num)

    path = "D:\\document\\gradu\\pic\\kmeans_"
    img_path = path + str(batch_id) + ".jpg"
    plt.figure()

    x = [p[0] for p in peaks]
    y = [p[1] for p in peaks]
    plt.scatter(x , y , c = cluster_ids , s = 2)
    plt.savefig(img_path , dpi = 300)
    plt.close()

if __name__ == "__main__":
    num = [3,3,2,2,2,2]
    for batch_id in range(1,7):
        Show_kmeans(batch_id , num[batch_id-1])
    