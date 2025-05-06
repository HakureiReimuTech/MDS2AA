import sys
import numpy as np
import wave

def hamming_encode(half_byte):
    """将4位半字节编码为7位海明码"""
    d1 = (half_byte >> 3) & 1
    d2 = (half_byte >> 2) & 1
    d3 = (half_byte >> 1) & 1
    d4 = half_byte & 1
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4
    # 码字排列：p1, p2, d1, p3, d2, d3, d4
    code = (p1 << 6) | (p2 << 5) | (d1 << 4) | (p3 << 3) | (d2 << 2) | (d3 << 1) | d4
    return [(code >> i) & 1 for i in range(6, -1, -1)]

def main():
    if len(sys.argv) != 2:
        print("Usage: python modulator.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 调制参数
    carrier_freq = 20     # 载波频率（Hz）
    sample_rate = 192000  # 采样率（Hz）
    amplitude = 0.7       # 振幅系数（0到1）
    
    samples_per_half_cycle = int(sample_rate / (2 * carrier_freq))
    
    # 读取并编码数据
    with open(input_file, 'rb') as f:
        data = f.read()
    
    bits = []
    for byte in data:
        # 拆分字节为两个4位半字节
        high_nibble = (byte >> 4) & 0x0F
        low_nibble = byte & 0x0F
        # 海明编码并添加到比特流
        bits.extend(hamming_encode(high_nibble))
        bits.extend(hamming_encode(low_nibble))
    
    # 生成波形
    t = np.linspace(0, 1/(2*carrier_freq), samples_per_half_cycle, endpoint=False)
    positive_half = np.sin(2 * np.pi * carrier_freq * t)
    negative_half = -positive_half
    
    audio = np.concatenate([positive_half if bit else negative_half for bit in bits])
    audio = (audio * amplitude * 32767).astype(np.int16)
    
    # 保存音频
    with wave.open('output.wav', 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

if __name__ == "__main__":
    main()
