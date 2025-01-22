import secrets

def generate_token(length=32):
    # 使用secrets.token_hex生成一个安全的随机十六进制字符串
    return secrets.token_hex(length // 2)

# 生成32位密钥token
token = generate_token()
print(token)
