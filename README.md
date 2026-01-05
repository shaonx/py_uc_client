# UCenter Python Client (PHP 迁移版) 🍮✨

这是一个将 UCenter PHP 客户端核心逻辑迁移到 Python 的小项目。它可以让你在 Python 环境中丝滑地调用 UCenter 接口（比如登录验证），而不需要依赖 PHP 环境。

本项目完全复刻了 UCenter 的 `uc_authcode` 加密算法和通信协议，安全又防弹！🛡️

## 🌟 项目亮点

- **零依赖**：只使用 Python 标准库（`hashlib`, `base64`, `urllib`, `xml` 等），轻量又快速。
- **协议兼容**：完美对齐 PHP 版 `uc_client` 1.7.0+ 协议，支持 `UC_KEY` 加密通信。
- **安全优先**：严格实现 RC4 变体加密，确保通信过程中的数据安全。
- **简单易用**：几行代码就能完成 UCenter 登录验证。

## 📂 目录结构

```text
.
├── py_uc_client/          # Python 核心库
│   ├── auth.py           # uc_authcode 算法实现 (核心加密)
│   ├── client.py         # UCClient 客户端封装 (API 调用)
│   └── xmlcodec.py       # UCenter XML 协议解析器
├── test.py               # Python 调用示例 (测试脚本)
├── uc_client/            # 原 PHP 版客户端 (参考用)
└── test.php              # 原 PHP 版测试脚本 (对比用)
```

## 🚀 快速开始

### 1. 配置参数

在你的 Python 代码中，你需要准备好 UCenter 的配置信息（这些通常可以在你的 Discuz! 或 UCenter 后台找到）：

```python
UC_KEY = '你的UC_KEY'
UC_API = 'http://your-uc-server/uc_server'
UC_APPID = '2'
UC_CLIENT_RELEASE = '20250901'
```

### 2. 调用示例

```python
from py_uc_client.client import UCClient

# 初始化客户端
client = UCClient(UC_API, UC_KEY, UC_APPID, UC_CLIENT_RELEASE)

# 尝试登录
# 参数: username, password, isuid, checkques, questionid, answer, ip, nolog
result = client.uc_user_login('test_user', 'test_password')

print(f"登录结果: {result}")
```

### 3. 运行测试

你可以直接运行项目根目录下的 `test.py` 来验证配置是否正确：

```bash
python test.py
```

如果配置正确且 UCenter 服务正常，你将看到类似如下的输出：
`登录测试结果: ["2", "test", "test", "test@123.com", "0"]`

## 🛠️ 技术细节 

- **加密逻辑**：auth.py实现了 PHP 著名的 `uc_authcode` 函数。注意它使用了 `latin-1` 编码来处理字节流，以确保与 PHP 的原始字符串处理逻辑一致。
- **通信协议**：client.py模拟了 `uc_api_post` 的行为，包括构造 `input` 参数和处理 `User-Agent` 的 MD5 校验。
- **数据解析**：xmlcodec.py负责将 UCenter 返回的特殊 XML 格式解析为 Python 的列表或字典，处理了递归的 `<item>` 标签。

## ⚠️ 安全提醒

- 请务必保护好你的 `UC_KEY`，它是通信安全的基石！
- 建议在生产环境中使用 HTTPS 协议连接 `UC_API`。
