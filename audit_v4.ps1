# 占位符列表（不区分大小写）
$placeholders = @('Describe feature', 'Describe Step', 'Beschreiben', 'Describir', '説明')

# 结果统计
$totalFiles = 0
$criticalFiles = 0
$criticalFilePaths = @()

# 遍历目录
function Audit-Directory {
    param(
        [string]$directory
    )
    
    Write-Host "正在扫描目录: $directory"
    
    $files = Get-ChildItem -Path $directory -Recurse -Include "*.md" -ErrorAction SilentlyContinue
    Write-Host "找到 $($files.Count) 个 .md 文件"
    
    foreach ($file in $files) {
        $global:totalFiles++
        
        # 读取文件内容
        try {
            Write-Host "正在检查文件: $($file.FullName)"
            $content = Get-Content -Path $file.FullName -Encoding UTF8 -Raw -ErrorAction SilentlyContinue
            if ($content) {
                $content = $content.ToLower()
                
                # 检查是否包含占位符
                $isCritical = $false
                foreach ($placeholder in $placeholders) {
                    if ($content -match $placeholder.ToLower()) {
                        $isCritical = $true
                        break
                    }
                }
                
                if ($isCritical) {
                    Write-Host "找到僵尸文件: $($file.FullName)"
                    $global:criticalFiles++
                    $global:criticalFilePaths += $file.FullName
                }
            }
        } catch {
            Write-Host "[ERROR] 无法读取文件 $($file.FullName): $($_.Exception.Message)"
            $global:criticalFiles++
            $global:criticalFilePaths += $file.FullName
        }
    }
}

# 主函数
Write-Host "开始执行体检脚本..."

# 遍历当前目录
$baseDirectory = Get-Location
Audit-Directory -directory $baseDirectory

# 生成报告
Write-Host "`n=== 体检报告 ==="
Write-Host "总文件数: $totalFiles"
Write-Host "僵尸文件数: $criticalFiles"
Write-Host "就绪文件数: $($totalFiles - $criticalFiles)"

# 生成待办清单
$todoList = @{
    "total_files" = $totalFiles
    "critical_files" = $criticalFiles
    "ready_files" = $totalFiles - $criticalFiles
    "critical_file_paths" = $criticalFilePaths
}

$todoList | ConvertTo-Json -Depth 100 | Out-File -FilePath "todo_list.json" -Encoding UTF8

Write-Host "`n待办清单已生成到 todo_list.json"
Write-Host "真实的僵尸文件数量: $criticalFiles"