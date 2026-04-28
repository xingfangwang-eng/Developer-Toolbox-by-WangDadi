#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Pusher - GitHub 实时同步脚本
每隔1小时自动扫描文件夹变动，超过50个文件变更则自动提交推送
"""

import os
import time
import subprocess
from datetime import datetime

GIT_REPO_PATH = r"E:\Developer-Toolbox-by-WangDadi"
COMMIT_THRESHOLD = 50
CHECK_INTERVAL_HOURS = 1

def get_changed_files(repo_path):
    """获取所有已跟踪文件的变更状态"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode != 0:
            print(f"⚠️ Git 命令执行失败: {result.stderr}")
            return []
        
        changed_files = []
        for line in result.stdout.strip().split('\n'):
            if line:
                file_path = line[3:].strip()
                changed_files.append(file_path)
        return changed_files
    except Exception as e:
        print(f"❌ 获取变更文件失败: {e}")
        return []

def git_add_commit_push(repo_path, changed_files):
    """执行 git add, commit, push"""
    try:
        print(f"\n📦 开始提交 {len(changed_files)} 个文件...")
        
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"🤖 Auto-sync: {timestamp} - {len(changed_files)} files updated"
        
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=repo_path,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            if "nothing to commit" in result.stdout:
                print("📝 没有需要提交的内容")
                return False
            print(f"⚠️ Commit 失败: {result.stderr}")
            return False
        
        print(f"✅ Commit 成功: {commit_message}")
        
        print("🚀 正在推送到 GitHub...")
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print(f"⚠️ Push 失败: {result.stderr}")
            return False
        
        print("✅ 推送成功！GitHub 页面已更新")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def main():
    print("=" * 60)
    print("Batch Pusher - GitHub 实时同步启动")
    print("=" * 60)
    print(f"📁 仓库路径: {GIT_REPO_PATH}")
    print(f"📊 提交阈值: {COMMIT_THRESHOLD} 个文件")
    print(f"⏰ 检查间隔: {CHECK_INTERVAL_HOURS} 小时")
    print("=" * 60)
    
    while True:
        check_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"🕐 [{check_time}] 开始检查文件变动...")
        
        changed_files = get_changed_files(GIT_REPO_PATH)
        changed_count = len(changed_files)
        
        print(f"📝 发现 {changed_count} 个已跟踪文件发生变动")
        
        if changed_count >= COMMIT_THRESHOLD:
            print(f"🚀 超过阈值 ({COMMIT_THRESHOLD})，触发自动提交！")
            
            if git_add_commit_push(GIT_REPO_PATH, changed_files):
                print(f"✅ [{check_time}] 同步完成！")
            else:
                print(f"❌ [{check_time}] 同步失败！")
        else:
            print(f"📝 变动文件不足，等待下次检查...")
        
        print(f"\n⏰ 下次检查时间: {CHECK_INTERVAL_HOURS} 小时后")
        time.sleep(CHECK_INTERVAL_HOURS * 3600)

if __name__ == "__main__":
    main()