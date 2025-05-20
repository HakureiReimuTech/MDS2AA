# Modulate Digital Signal to Analog Audio Project
顾名思义，本程序用于将数字信号调制成模拟信号<br>
你可以把你的文件记录在音频磁带上，也可以通过电话或无线电与你的好友共享文件！<br>
#### 这是一个实验项目，不要让他成为数据的唯一副本！我们不会承担使用本程序产生的任何损失！<br>
## 使用方法
``pip install numpy``<br>
``python Encoder.py N.bin``<br>
``python Decoder.py N.wav``<br>
## 原理
使用正弦波正半周表示1，负半周表示0，该方式更能够忍耐抖动（例如磁带）<br>
![原理图1](https://i.miji.bid/2025/05/06/701a338f3d73369bbfb68622ee85afb6.png)<br>
该程序可将数据记录在磁带上，也可用于在电话线或无线电中传输数据，相比于KCS等协议，这个程序的频率高，抗干扰性能更强，速度更快，而且更能够忍受抖动<br>
## 修改
出于测试目的，程序默认的频率仅为20Hz，可以自行调整<br>
![ ](https://i.miji.bid/2025/05/06/f1b57cbc9c201e4421e9b686b82535fc.png)<br>
![ ](https://i.miji.bid/2025/05/06/76d813736b06e2b3fe208c3cd14353bf.png)<br>
## 纠错
Encoder/Decoder默认不使用任何纠错<br>
HEncoder/Hdecoder使用汉明码作为纠错方式<br>
LDPC-Encoder/LDPC-Decoder使用LDPC作为纠错方式（实验性）<br>
**LDPC纠错待完善，有严重Bug，不要使用**
