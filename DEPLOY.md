# GitHub 上传指南

本项目已完成本地git初始化，按照以下步骤上传到GitHub：

## 步骤一：创建GitHub仓库

1. 访问 https://github.com/new
2. 填写仓库名称（例如：`taobao-user-behavior-analysis`）
3. 选择 **Public** 或 **Private**
4. **不要**初始化README（我们已经有了）
5. 点击 "Create repository"

## 步骤二：添加远程仓库

在PowerShell中运行：

```powershell
# 替换为你的GitHub用户名和仓库名
git remote add origin https://github.com/你的用户名/仓库名.git

# 例如：
# git remote add origin https://github.com/zhangsan/taobao-analysis.git
```

## 步骤三：推送到GitHub

```powershell
# 首次推送（设置上游分支）
git branch -M main
git push -u origin main
```

或者如果你想用master分支：

```powershell
git push -u origin master
```

## 常见问题

### 认证失败

如果你启用了2FA，需要使用Personal Access Token：

1. 访问 https://github.com/settings/tokens
2. 生成新Token，勾选 `repo` 权限
3. 推送时，用户名填你的GitHub用户名，密码填Token

### 使用SSH（推荐）

```bash
# 添加SSH远程仓库
git remote set-url origin git@github.com:你的用户名/仓库名.git
```

## 查看远程仓库

```powershell
git remote -v
```

## 更新README中的图片

在GitHub上，图片会自动显示，你可以在README中这样引用：

```markdown
![PV/UV趋势图](pv_uv_trend.png)
![PV/UV对比图](pv_uv_comparison.png)
```

---
**提示**：项目已包含15个文件，约619行代码 + 2张可视化图表
