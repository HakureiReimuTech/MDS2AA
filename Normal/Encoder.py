import sys
import numpy as np
import wave

def main():
    if len(sys.argv) != 2:
        print("Usage: python modulator.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 调制参数
    carrier_freq = 22500     # 载波频率（Hz）
    sample_rate = 192000    # 采样率（Hz）
    amplitude = 0.7         # 振幅系数（0到1）
    
    # 计算每个半周期的样本数
    samples_per_half_cycle = int(sample_rate / (2 * carrier_freq))
    
    # 读取输入文件
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # 将字节数据转换为比特流（高位在前）
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    
    # 生成基础波形模板
    t = np.linspace(0, 1/(2*carrier_freq), samples_per_half_cycle, endpoint=False)
    positive_half = np.sin(2 * np.pi * carrier_freq * t)
    negative_half = -positive_half
    
    # 生成完整音频信号
    audio = []
    for bit in bits:
        audio.append(positive_half if bit else negative_half)
    audio = np.concatenate(audio)
    
    # 调整振幅并转换为16位整数格式
    audio = (audio * amplitude * 32767).astype(np.int16)
    
    # 写入WAV文件
    with wave.open('output.wav', 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

if __name__ == "__main__":
    main()
