import wave
import numpy as np
import sys

def hamming_decode(bits):
    """将7位海明码解码为4位数据，并纠正单比特错误"""
    if len(bits) != 7:
        raise ValueError("Hamming code must be 7 bits")
    
    # 变量名与编码器码字排列严格对应
    p1, p2, d1, p3, d2, d3, d4 = bits
    
    # 计算校验子
    s1 = p1 ^ (d1 ^ d2 ^ d4)
    s2 = p2 ^ (d1 ^ d3 ^ d4)
    s3 = p3 ^ (d2 ^ d3 ^ d4)
    
    # 使用位或合并校验子
    error_pos = s1 | (s2 << 1) | (s3 << 2)
    
    # 纠正错误位
    if error_pos != 0:
        error_index = error_pos - 1
        if error_index < 7:
            bits[error_index] ^= 1
            # 重新提取纠正后的位
            p1, p2, d1, p3, d2, d3, d4 = bits
    
    # 返回合并后的半字节
    return (d1 << 3) | (d2 << 2) | (d3 << 1) | d4

def main():
    if len(sys.argv) != 2:
        print("Usage: python HDecoder.py <input_wav>")
        sys.exit(1)
    
    input_wav = sys.argv[1]
    
    # 参数需与编码器严格一致
    carrier_freq = 20
    sample_rate = 192000
    samples_per_half_cycle = int(sample_rate / (2 * carrier_freq))  # 4800
    
    # 读取音频文件
    with wave.open(input_wav, 'rb') as wf:
        n_frames = wf.getnframes()
        frames = wf.readframes(n_frames)
    
    audio = np.frombuffer(frames, dtype=np.int16)
    
    # 分割为半周期段并解调
    bits = []
    num_segments = len(audio) // samples_per_half_cycle
    for i in range(num_segments):
        start = i * samples_per_half_cycle
        end = start + samples_per_half_cycle
        segment = audio[start:end]
        avg = np.mean(segment)
        bits.append(1 if avg > 0 else 0)
    
    # 海明解码
    nibbles = []
    for i in range(0, len(bits), 7):
        chunk = bits[i:i+7]
        if len(chunk) < 7:
            break
        nibble = hamming_decode(chunk)
        nibbles.append(nibble)
    
    # 合并半字节为字节
    bytes_list = bytearray()
    for i in range(0, len(nibbles), 2):
        if i+1 >= len(nibbles):
            break
        high = nibbles[i]
        low = nibbles[i+1]
        bytes_list.append((high << 4) | low)
    
    # 写入输出文件
    with open('decoded.bin', 'wb') as f:
        f.write(bytes_list)
    
    print("Decoding completed. Output saved to decoded.bin")

if __name__ == "__main__":
    main()
