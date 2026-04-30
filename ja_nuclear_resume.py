import os
import re
import glob
from pathlib import Path
from tqdm import tqdm

LOG_FILE = r"E:\Developer-Toolbox-by-WangDadi\ja_cleaned_files.log"
BASE_DIR = r"E:\Developer-Toolbox-by-WangDadi"

CHINESE_HIGH_FREQ_WORDS = [
    "概述", "核心", "步骤", "建议", "功能点", "決策", "自定义", "自定义的",
    "异常", "例外", "故障", "问题", "解决方案", "配置", "设置", "安装步骤",
    "简介", "主要功能", "使用方法", "技术架构", "应用场景", "优势特点",
    "快速开始", "环境要求", "安装教程", "常见问题", "更新日志", "版本说明",
    "自定义", "配置", "初始化", "执行", "处理", "分析", "监控", "管理",
    "平台", "系统", "模块", "服务", "数据", "信息", "用户", "管理员",
    "网络", "服务器", "客户端", "接口", "协议", "格式", "文件", "目录",
    "路径", "名称", "标识", "编号", "状态", "类型", "属性", "参数",
    "错误", "警告", "提示", "信息", "成功", "失败", "完成", "取消",
    "开始", "结束", "继续", "停止", "暂停", "恢复", "重启", "关闭",
    "创建", "删除", "修改", "查询", "添加", "移除", "复制", "移动",
    "上传", "下载", "发送", "接收", "连接", "断开", "登录", "退出",
    "注册", "激活", "验证", "授权", "认证", "加密", "解密", "编码",
    "优化", "调整", "测试", "调试", "排查", "修复", "解决", "处理",
]

def get_processed_files():
    processed = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "SUCCESS:" in line:
                    path = line.split("SUCCESS:")[-1].strip()
                    processed.add(path)
    return processed

def has_chinese_high_freq_words(content):
    for word in CHINESE_HIGH_FREQ_WORDS:
        if word in content:
            return True
    return False

def count_chinese_chars(text):
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(text))

def should_skip_file(filepath, processed_files):
    if filepath in processed_files:
        return True, "in_log"

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        chinese_count = count_chinese_chars(content)

        if chinese_count < 400:
            return False, "too_short"

        if not has_chinese_high_freq_words(content):
            return True, "clean"

        return False, "needs_rewrite"
    except Exception as e:
        return True, f"error: {e}"

def call_ollama_llama3(project_name, content):
    import urllib.request
    import json

    prompt = f"""あなたは一流のITアーキテクトです。
任務：このプロジェクト（{project_name}）のマニュアルを、完全にプロフェッショナルな日本語で書き直してください。

禁止事項：
1. 中国語の漢字（概述、核心、步骤、建议等）を絶対に使用しないでください。
2. 日本のエンジニアが自然に感じる技術用語（概要、主な機能、クイックスタート、推奨事項）を使用してください。
3. 3つの主要機能、3つの導入ステップ、2つのエキスパートアドバイスを含めること。
4. 既存の Markdown 形式と底部の `https://www.wangdadi.xyz` リンクを維持してください。

元の内容：
{content}"""

    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("response", "")
    except Exception as e:
        print(f"\nOllama Error: {e}")
        return None

def extract_project_name(filepath):
    parts = Path(filepath).parts
    for i, part in enumerate(parts):
        if part == "ja":
            if i > 0:
                return parts[i - 1]
    return "unknown"

def main():
    print("=" * 60)
    print("JA Nuclear Resume - 日语页面彻底重写")
    print("=" * 60)

    processed_files = get_processed_files()
    print(f"已处理文件数: {len(processed_files)}")

    all_ja_files = []
    for pattern in [
        os.path.join(BASE_DIR, "*/manual/ja/*.md"),
        os.path.join(BASE_DIR, "*/manual/*/ja/*.md"),
    ]:
        all_ja_files.extend(glob.glob(pattern))

    all_ja_files = list(set(all_ja_files))
    all_ja_files.sort()

    print(f"扫描到日语文件总数: {len(all_ja_files)}")

    to_process = []
    to_skip_log = []
    to_skip_clean = []
    to_skip_short = []

    for filepath in all_ja_files:
        skip, reason = should_skip_file(filepath, processed_files)
        if skip:
            if reason == "in_log":
                to_skip_log.append(filepath)
            elif reason == "clean":
                to_skip_clean.append(filepath)
            elif reason == "too_short":
                to_skip_short.append(filepath)
            else:
                to_skip_log.append(filepath)
        else:
            to_process.append(filepath)

    print(f"\n断点续传分析:")
    print(f"  - 日志中已存在: {len(to_skip_log)}")
    print(f"  - 已清洁（跳过）: {len(to_skip_clean)}")
    print(f"  - 字数不足400: {len(to_skip_short)}")
    print(f"  - 需要重写: {len(to_process)}")

    if not to_process:
        print("\n所有文件已处理完成，无需重写。")
        return

    print(f"\n开始重写 {len(to_process)} 个文件...")
    print("-" * 60)

    success_count = 0
    fail_count = 0

    with tqdm(total=len(to_process), desc="重写进度", unit="file") as pbar:
        pbar.set_postfix({
            "跳过": len(to_skip_log) + len(to_skip_clean),
            "正在重写": 0
        })

        for i, filepath in enumerate(to_process):
            project_name = extract_project_name(filepath)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    original_content = f.read()

                pbar.set_postfix({
                    "跳过": len(to_skip_log) + len(to_skip_clean) + success_count + fail_count,
                    "正在重写": project_name
                })

                rewritten = call_ollama_llama3(project_name, original_content)

                if rewritten:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(rewritten)

                    with open(LOG_FILE, "a", encoding="utf-8") as log:
                        log.write(f"SUCCESS: {filepath}\n")

                    success_count += 1
                else:
                    fail_count += 1
                    with open(LOG_FILE, "a", encoding="utf-8") as log:
                        log.write(f"FAILED: {filepath}\n")

            except Exception as e:
                fail_count += 1
                print(f"\nError processing {filepath}: {e}")
                with open(LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"ERROR: {filepath} - {e}\n")

            pbar.update(1)
            pbar.set_postfix({
                "跳过": len(to_skip_log) + len(to_skip_clean) + success_count + fail_count,
                "成功": success_count,
                "失败": fail_count
            })

    print("\n" + "=" * 60)
    print("执行完成!")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  总计: {len(to_process)}")
    print("=" * 60)

if __name__ == "__main__":
    main()