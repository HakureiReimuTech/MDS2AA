![2b1ba0d3c0c6219edc2c2df2281691df455443751](https://github.com/user-attachments/assets/b35e18d1-8cdb-4eeb-9fd8-008525ae767a)# Modulate Digital Signal to Analog Audio Project
顾名思义，本程序用于将数字信号调制成模拟信号<br>
你可以把你的文件记录在音频磁带上，也可以通过电话或无线电与你的好友共享文件！
#### 这是一个实验项目，不要让他成为数据的唯一副本！我们不会承担使用本程序产生的任何损失！
## 原理
使用正弦波正半周表示1，负半周表示0，该方式更能够忍耐抖动（例如磁带）
![原理图1](https://i.miji.bid/2025/05/06/701a338f3d73369bbfb68622ee85afb6.png)
该程序可将数据记录在磁带上，也可用于在电话线或无线电中传输数据，相比于KCS等协议，这个程序的频率高，抗干扰性能更强，速度更快，而且更能够忍受抖动
## 修改
出于测试目的，程序默认的频率仅为20Hz，可以自行调整
![ ](https://i.miji.bid/2025/05/06/f1b57cbc9c201e4421e9b686b82535fc.png)
![ ](https://i.miji.bid/2025/05/06/76d813736b06e2b3fe208c3cd14353bf.png)
## 纠错
Encoder/Decoder默认不使用任何纠错<br>
HEncoder/Hdecoder使用汉明码作为纠错方式<br>
LDPC-Encoder/LDPC-Decoder使用LDPC作为纠错方式（实验性）<br>
