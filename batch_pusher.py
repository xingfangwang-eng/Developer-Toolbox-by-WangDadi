import os
import subprocess
import time
from tqdm import tqdm

# 全局变量
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BATCH_SIZE = 3
RETRY_DELAY = 10  # 重试等待时间（秒）

# 获取根目录下的项目文件夹
def get_project_folders():
    project_folders = []
    for item in os.listdir(ROOT_DIR):
        item_path = os.path.join(ROOT_DIR, item)
        # 只考虑目录，排除指定的文件夹
        if os.path.isdir(item_path):
            # 排除隐藏文件夹和特定文件夹
            if not item.startswith('.') and item not in ['venv', '__pycache__']:
                project_folders.append(item)
    return project_folders

# 执行 git 命令
def run_git_command(cmd, cwd):
    try:
        result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

# 推送单个项目
def push_project(project_name):
    # 执行 git add [文件夹名]
    success, stdout, stderr = run_git_command(f'git add {project_name}', ROOT_DIR)
    if not success:
        print(f"❌ {project_name}: git add 失败 - {stderr}")
        return False
    
    return True

# 主函数
def main():
    # 获取项目文件夹
    project_folders = get_project_folders()
    total_projects = len(project_folders)
    total_batches = (total_projects + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"发现 {total_projects} 个项目，将分为 {total_batches} 批处理")
    print("\n扫描到的项目列表：")
    for i, project in enumerate(project_folders, 1):
        print(f"{i}. {project}")
    
    # 分批处理
    for batch_idx in range(total_batches):
        start_idx = batch_idx * BATCH_SIZE
        end_idx = min((batch_idx + 1) * BATCH_SIZE, total_projects)
        batch_projects = project_folders[start_idx:end_idx]
        
        print(f"\n[Batch {batch_idx + 1}/{total_batches}] 处理项目: {', '.join(batch_projects)}")
        
        # 处理当前批次
        batch_success = False
        retry_count = 0
        
        while not batch_success and retry_count < 5:  # 最多重试 5 次
            batch_success = True
            
            # 添加批次中的所有项目
            for project in tqdm(batch_projects, desc="添加项目"):
                if not push_project(project):
                    batch_success = False
                    break
            
            if batch_success:
                # 执行 git commit
                success, stdout, stderr = run_git_command('git commit -m "Deploy: Souls injected into 3 projects"', ROOT_DIR)
                if not success:
                    # 可能没有需要提交的更改
                    if "nothing to commit" in stderr or "nothing to commit" in stdout:
                        print(f"[Batch {batch_idx + 1}] No changes, skipping to next.")
                        batch_success = True  # 无变动视为成功
                    else:
                        print(f"❌ git commit 失败 - {stderr}")
                        batch_success = False
                
                if batch_success and not ("nothing to commit" in stderr or "nothing to commit" in stdout):
                    # 执行 git push -f 强制推送
                    success, stdout, stderr = run_git_command('git push -f origin main', ROOT_DIR)
                    if not success:
                        print(f"❌ git push 失败 - {stderr}")
                        batch_success = False
            
            if not batch_success:
                retry_count += 1
                print(f"❌ 批次推送失败，{RETRY_DELAY} 秒后重试... (尝试 {retry_count}/5)")
                time.sleep(RETRY_DELAY)
        
        if batch_success:
            print(f"✅ [Batch {batch_idx + 1}/{total_batches}] 推送成功")
        else:
            print(f"❌ [Batch {batch_idx + 1}/{total_batches}] 推送失败，已达到最大重试次数")
    
    print("\n所有批次处理完成！")

if __name__ == "__main__":
    main()