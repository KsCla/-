from scipy.fftpack import fft
from math import log10

def Read(cnt):
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

if __name__ == "__main__":
    pass