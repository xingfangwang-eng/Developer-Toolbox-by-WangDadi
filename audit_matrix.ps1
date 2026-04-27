# 占位符列表
$placeholderPatterns = @('Describe feature', 'Step 1', 'Practice 1')

# 结果统计
$totalFiles = 0
$readyFiles = 0
$criticalFiles = 0
$criticalFilePaths = @()

# 遍历目录
function Audit-Directory {
    param(
        [string]$directory
    )
    
    $files = Get-ChildItem -Path $directory -Recurse -Include "*.md" -ErrorAction SilentlyContinue
    
    foreach ($file in $files) {
        $global:totalFiles++
        
        # 读取文件内容
        try {
            $content = Get-Content -Path $file.FullName -Encoding UTF8 -Raw
            
            # 检查是否包含占位符
            $hasPlaceholder = $false
            foreach ($pattern in $placeholderPatterns) {
                if ($content -match $pattern) {
                    $hasPlaceholder = $true
                    break
                }
            }
            
            if ($hasPlaceholder) {
                Write-Host "[CRITICAL] $($file.FullName)"
                $global:criticalFiles++
                $global:criticalFilePaths += $file.FullName
            } else {
                Write-Host "[READY] $($file.FullName)"
                $global:readyFiles++
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
Write-Host "\n=== 体检报告 ==="
Write-Host "总文件数: $totalFiles"
Write-Host "已就绪数: $readyFiles"
Write-Host "待修复数: $criticalFiles"

# 生成待办清单
$todoList = @{
    "total_files" = $totalFiles
    "ready_files" = $readyFiles
    "critical_files" = $criticalFiles
    "critical_file_paths" = $criticalFilePaths
}

$todoList | ConvertTo-Json -Depth 100 | Out-File -FilePath "todo_list.json" -Encoding UTF8

Write-Host "\nTodo list generated to todo_list.json"
Write-Host "There are $criticalFiles files to fix"