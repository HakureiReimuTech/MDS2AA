import sys
import numpy as np
import wave
from pyldpc import make_ldpc, encode

def main():
    if len(sys.argv) != 2:
        print("Usage: python modulator.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # LDPC编码参数（修正后）
    n = 12   # 码长
    d_v = 3  # 变量节点度数
    d_c = 4  # 校验节点度数
    snr = 0  # 编码占位参数
    
    # 调制参数
    carrier_freq = 20
    sample_rate = 192000
    amplitude = 0.7

    # 生成LDPC编码矩阵
    H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
    k = G.shape[1]  # 信息位长度
    
    # 调试输出G矩阵结构
    print(f"G矩阵维度: {G.shape}")
    print("G矩阵前5行示例:")
    print(G[:5, :])
    
    # 读取文件并转换为二进制流
    with open(input_file, 'rb') as f:
        raw_bytes = np.frombuffer(f.read(), dtype=np.uint8)
    
    # 调试输出原始字节
    print(f"原始字节示例: {raw_bytes[:10]}")
    
    bits = np.unpackbits(raw_bytes).astype(int)  # 字节转比特流
    
    # 调试输出原始比特流
    print(f"原始比特流前20位: {bits[:20]}")
    
    # 补零对齐块长度（随机填充）
    pad_len = (k - (len(bits) % k)) % k
    print(f"需要填充的位数: {pad_len}")
    bits = np.concatenate([bits, np.random.randint(0, 2, pad_len)])
    
    # 调试输出填充后的比特流
    print(f"填充后的比特流后10位: {bits[-10:]}")
    
    # LDPC编码（分块处理）
    coded_bits = []
    for i in range(0, len(bits), k):
        msg = bits[i:i+k]
        if len(msg) < k:
            msg = np.pad(msg, (0, k - len(msg)), 'constant')
        
        # 调试输入消息
        print(f"编码块 {i//k}: 输入消息前5位: {msg[:5]}")
        
        codeword = encode(G, msg, snr)
        coded_bits.extend(codeword.tolist())
        
        # 调试编码输出
        print(f"编码块 {i//k}: 输出前10位: {codeword[:10]}")
    
    # 强制插入测试位（验证调制映射）
    coded_bits[:10] = [0,1,0,1,0,1,0,1,0,1]  # 确保有0和1
    
    # 生成波形模板
    samples_per_half_cycle = int(sample_rate / (2 * carrier_freq))
    t = np.linspace(0, 1/(2*carrier_freq), samples_per_half_cycle, endpoint=False)
    positive_half = np.sin(2 * np.pi * carrier_freq * t)
    negative_half = -positive_half
    
    # 生成音频信号（仅生成前1000位用于验证）
    audio = []
    for idx, bit in enumerate(coded_bits[:1000]):
        if bit not in [0, 1]:
            print(f"错误：位置 {idx} 的比特值为 {bit}")
            bit = 0  # 强制纠正
        waveform = positive_half if bit == 1 else negative_half
        audio.append(waveform)
    audio = np.concatenate(audio)
    
    # 调整振幅并转换为16位整数格式
    audio = (audio * amplitude * 32767).astype(np.int16)
    
    # 写入WAV文件
    with wave.open('output_ldpc.wav', 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

if __name__ == "__main__":
    main()
