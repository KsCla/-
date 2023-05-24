import matplotlib.pyplot as plt
root_path = "D:\\document\\gradu\\自测数据分析"
import sys
sys.path.append( root_path )
from read_file import Read

if __name__ == "__main__":
    total = 300
    path = "D:\\document\\gradu\\自测数据分析\\低频频谱图"
    for i in range(total):
        cnt = i+1
        freq = Read(cnt)
        plt.figure()
        plt.plot(freq , linewidth =0.5)
        img_path = path + "\\" + str(cnt) + ".jpg"
        plt.savefig(img_path , dpi = 300)
        plt.close()
