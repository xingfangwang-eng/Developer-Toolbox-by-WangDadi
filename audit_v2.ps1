# 黑名单词汇
$blacklist = @{}
$blacklist['en'] = @('Describe feature', 'Step 1', 'Practice 1')
$blacklist['de'] = @('Beschreiben', 'Schritt')
$blacklist['es'] = @('Describir', 'Paso', 'Práctica')
$blacklist['ja'] = @('説明する', 'ステップ', 'プラクティス')

# 结果统计
$totalFiles = 0
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
            
            # 检查是否包含黑名单词汇
            $isCritical = $false
            foreach ($lang in $blacklist.Keys) {
                foreach ($word in $blacklist[$lang]) {
                    if ($content -match $word) {
                        $isCritical = $true
                        break
                    }
                }
                if ($isCritical) {
                    break
                }
            }
            
            if ($isCritical) {
                Write-Host "[CRITICAL] $($file.FullName)"
                $global:criticalFiles++
                $global:criticalFilePaths += $file.FullName
            } else {
                Write-Host "[READY] $($file.FullName)"
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

Write-Host "\n待办清单已生成到 todo_list.json"
Write-Host "真实的僵尸文件数量: $criticalFiles"