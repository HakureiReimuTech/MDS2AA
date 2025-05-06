import wave
import numpy as np
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python demodulator.py <input_wav>")
        sys.exit(1)
    
    input_wav = sys.argv[1]
    
    # 调制参数（需与调制程序一致）
    carrier_freq = 20           # 载波频率（Hz）
    sample_rate = 192000        # 采样率（Hz）
    samples_per_half_cycle = sample_rate // (2 * carrier_freq)  # 每半周期样本数
    
    # 读取WAV文件
    with wave.open(input_wav, 'rb') as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != sample_rate:
            print("不支持的WAV格式")
            sys.exit(1)
        frames = wf.readframes(wf.getnframes())
    
    # 转换为numpy数组
    audio = np.frombuffer(frames, dtype=np.int16)
    
    # 分割为半周期块
    num_chunks = len(audio) // samples_per_half_cycle
    audio = audio[:num_chunks * samples_per_half_cycle]
    chunks = audio.reshape((num_chunks, samples_per_half_cycle))
    
    # 解调比特流
    bits = []
    for chunk in chunks:
        avg = np.mean(chunk)
        bits.append(1 if avg > 0 else 0)
    
    # 组合为字节（高位在前）
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) != 8:
            break  # 丢弃不足8位的部分
        byte = 0
        for bit in byte_bits:
            byte = (byte << 1) | bit
        bytes_list.append(byte)
    
    # 写入文件
    with open('output.bin', 'wb') as f:
        f.write(bytes(bytes_list))
    
    print("解调完成，结果保存为 output.bin")

if __name__ == "__main__":
    main()
