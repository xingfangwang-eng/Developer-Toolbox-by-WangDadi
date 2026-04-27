#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Brute Push - 暴力推送脚本
用于强制推送所有更改到 GitHub
"""

import os
import subprocess

# 配置
GITHUB_REPO = "your-github-username/your-repo-name"  # 替换为你的仓库
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# 检查环境变量
if not GITHUB_TOKEN:
    print("错误：请设置 GITHUB_TOKEN 环境变量")
    exit(1)

# 执行 Git 操作
def execute_git_commands():
    """执行 Git 提交和强制推送"""
    try:
        # 获取仓库目录
        repo_name = GITHUB_REPO.split('/')[-1]
        repo_path = os.path.join(os.getcwd(), repo_name)
        
        if not os.path.exists(repo_path):
            print(f"错误：仓库目录 {repo_path} 不存在！")
            return False
        
        print("开始暴力推送操作...")
        
        # 1. 强制添加所有更改
        print("执行 git add . 强制添加所有更改...")
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        
        # 2. 检查是否有更改
        result = subprocess.run(
            ["git", "status", "--porcelain"], 
            cwd=repo_path, 
            capture_output=True, 
            text=True
        )
        
        if not result.stdout.strip():
            print("没有更改需要提交")
            return True
        
        # 3. 提交
        commit_message = "Brute Push: Force update all changes"
        print(f"执行 git commit -m '{commit_message}'...")
        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
        
        # 4. 强制推送
        print("执行 git push -f...")
        subprocess.run(["git", "push", "-f"], cwd=repo_path, check=True)
        
        print("暴力推送操作完成！")
        return True
        
    except Exception as e:
        print(f"Git 操作失败: {e}")
        return False

# 主函数
def main():
    print("Brute Push 脚本启动")
    print("==================================")
    
    success = execute_git_commands()
    
    if success:
        print("\n✓ 推送成功！")
    else:
        print("\n✗ 推送失败！")

if __name__ == "__main__":
    main()
