import wave
import numpy as np
from pyldpc import make_ldpc
from pyldpc.decoder import decode  # 明确导入解码函数

def main():
    # 参数设置（必须与编码器完全一致）
    n = 20          # 码长
    d_v = 3         # 变量节点度数
    d_c = 4         # 校验节点度数
    snr = 10        # 信噪比
    carrier_freq = 20      # 载波频率
    sample_rate = 192000   # 采样率

    # 生成LDPC校验矩阵（与编码器相同）
    H, _ = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
    k = H.shape[1] - H.shape[0]  # 计算信息位长度

    # 读取WAV文件
    with wave.open('output_ldpc.wav', 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
        audio /= 32767.0  # 归一化到[-1,1]

    # 计算每个符号的样本数
    samples_per_symbol = int(sample_rate / (2 * carrier_freq))
    num_symbols = len(audio) // samples_per_symbol
    audio = audio[:num_symbols * samples_per_symbol]

    # 分割音频到符号块并解调（硬判决）
    t = np.linspace(0, 1/(2*carrier_freq), samples_per_symbol, endpoint=False)
    ref_wave = np.sin(2 * np.pi * carrier_freq * t)  # 参考波形
    
    bits = []
    for i in range(num_symbols):
        symbol = audio[i*samples_per_symbol : (i+1)*samples_per_symbol]
        corr = np.dot(symbol, ref_wave)
        bit = 1 if corr > 0 else 0  # 直接硬判决
        bits.append(bit)

    # 重组为LDPC码字
    codeword_bits = len(bits) // n * n
    codewords = np.array(bits[:codeword_bits]).reshape(-1, n)

    # LDPC解码（调用旧版decode函数）
    decoded_data = []
    for cw in codewords:
        info_bits = decode(H, cw, snr=snr, maxiter=100)[:k]  # 直接解码硬比特
        decoded_data.extend(info_bits)

    # 转换为字节流（高位在前）
    byte_stream = bytearray()
    for i in range(0, len(decoded_data), 8):
        chunk = decoded_data[i:i+8]
        chunk += [0]*(8 - len(chunk))  # 补足8位
        byte = sum(bit << (7 - j) for j, bit in enumerate(chunk))
        byte_stream.append(byte)

    # 写入文件
    with open('decoded.bin', 'wb') as f:
        f.write(byte_stream)

if __name__ == "__main__":
    main()
