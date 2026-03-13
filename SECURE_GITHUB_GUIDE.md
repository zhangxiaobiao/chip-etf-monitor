# 🔐 安全的GitHub发布指南

## ⚠️ 安全警告

**不要使用GitHub账号密码进行Git操作！**
- GitHub已于2021年8月禁用密码认证
- 使用密码会导致认证失败
- 明文密码存在严重安全风险

## ✅ 推荐的安全方法

### 方法一：Personal Access Token (推荐)

#### 步骤1：创建Personal Access Token

1. **登录GitHub** - 访问 https://github.com
2. **进入设置** - 点击右上角头像 → Settings
3. **找到Token设置** - 左侧菜单 → Developer settings → Personal access tokens → Tokens (classic)
4. **生成新Token** - 点击 "Generate new token (classic)"
5. **配置Token**：
   - **Note**: 输入描述，如 "Claw-ETF-Monitor"
   - **Expiration**: 选择有效期（建议90天）
   - **Scopes**: 勾选以下权限：
     - ✅ `repo` (完整仓库访问权限)
     - ✅ `workflow` (GitHub Actions权限，可选)
6. **生成并复制** - 点击 "Generate token"，**立即复制并妥善保存**

#### 步骤2：使用Token进行Git操作

**Windows命令提示符：**
```cmd
cd C:\Users\INTEL3\WorkBuddy\Claw
git init
git add .
git commit -m "Initial commit: 创科芯片ETF监控系统"
git branch -M main
git remote add origin https://YOUR_TOKEN@github.com/645702352/chip-etf-monitor.git
git push -u origin main
```

**PowerShell：**
```powershell
Set-Location "C:\Users\INTEL3\WorkBuddy\Claw"
git init
git add .
git commit -m "Initial commit: 创科芯片ETF监控系统"
git branch -M main
$token = "YOUR_TOKEN_HERE"  # 替换为你的token
git remote add origin "https://${token}@github.com/645702352/chip-etf-monitor.git"
git push -u origin main
```

**重要提示**：
- 将 `YOUR_TOKEN` 替换为你的实际token
- Token只会在首次推送时需要输入（Windows会凭据管理器保存）
- 不要将token提交到代码仓库！

### 方法二：SSH密钥认证（更安全）

#### 步骤1：生成SSH密钥

```cmd
ssh-keygen -t ed25519 -C "645702352@qq.com"
```

#### 步骤2：添加SSH密钥到GitHub

1. **复制公钥**：
```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub
```

2. **在GitHub添加密钥**：
   - Settings → SSH and GPG keys → New SSH key
   - 粘贴公钥内容
   - 保存

#### 步骤3：使用SSH推送

```cmd
cd C:\Users\INTEL3\WorkBuddy\Claw
git init
git add .
git commit -m "Initial commit: 创科芯片ETF监控系统"
git branch -M main
git remote add origin git@github.com:645702352/chip-etf-monitor.git
git push -u origin main
```

## 📋 完整发布流程

### 前置准备

1. **创建GitHub仓库**
   - 访问 https://github.com/new
   - Repository name: `chip-etf-monitor`
   - Description: `专业的科创芯片ETF(588200)实时监控与分析系统`
   - 选择：Public 或 Private
   - 不要初始化 README、.gitignore 或 license（我们已经有了）

2. **配置本地Git**
```cmd
cd C:\Users\INTEL3\WorkBuddy\Claw
git config user.name "Your Name"
git config user.email "645702352@qq.com"
```

### 推送代码

**选择上面任一方法（Token或SSH）执行推送命令**

## 🔍 验证发布成功

1. **访问GitHub仓库** - https://github.com/645702352/chip-etf-monitor
2. **检查文件** - 确认所有文件都已上传
3. **查看README** - 确认Markdown渲染正常
4. **验证Skill包** - 检查 `.codebuddy/skills/` 目录是否存在

## 🛡️ 安全最佳实践

1. **使用Token或SSH** - 永远不要使用密码
2. **定期轮换Token** - 建议每90天更新一次
3. **不要提交敏感信息** - 确认 `.gitignore` 正确配置
4. **启用2FA** - 在GitHub账号设置中启用双重认证
5. **审查权限** - 定期检查授权的第三方应用

## 🆘 常见问题

### Q: Token创建后在哪里找回？
A: Token只在创建时显示一次，丢失后需要重新创建

### Q: Windows会记住密码吗？
A: 使用Token方式，Windows凭据管理器会保存，下次不需要输入

### Q: SSH密钥如何管理？
A: 私钥保存在 `%USERPROFILE%\.ssh\` 目录，不要分享给任何人

### Q: 如何撤销泄露的Token？
A: GitHub设置 → Developer settings → Personal access tokens → 删除对应token

## 📞 需要帮助？

如果遇到问题，请提供：
1. 具体的错误信息
2. 执行的命令
3. 系统环境信息

---

**安全第一，正确使用认证方式，保护你的代码和账号安全！**
