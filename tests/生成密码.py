from passlib.context import CryptContext

# 你的原始密码上下文配置，完全不变
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 明文密码 admin123
plain_password = "admin123"

# 生成加密后的哈希密码（核心加密方法）
hashed_password = pwd_context.hash(plain_password)

# 打印加密结果
print("admin123 的 pbkdf2_sha256 加密密码：", hashed_password)