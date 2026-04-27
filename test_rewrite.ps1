# 全局变量
$API_KEY = "sk-acea097d87da45508303b0662a398434"
$API_ENDPOINT = "https://api.deepseek.com/chat/completions"
$MODEL = "deepseek-chat"
$PROJECTS_JSON = "projects.json"

# 加载项目信息
function Load-Projects {
    if (Test-Path $PROJECTS_JSON) {
        $content = Get-Content -Path $PROJECTS_JSON -Encoding UTF8 -Raw
        return $content | ConvertFrom-Json
    }
    return @{}
}

# 从路径中提取项目名和语言
function Extract-Info {
    param(
        [string]$filePath
    )
    
    # 提取项目名（文件夹名）
    $parts = $filePath -split '\\'
    $projectName = $null
    $lang = "en"
    
    for ($i = 0; $i -lt $parts.Length; $i++) {
        $part = $parts[$i]
        if ($part -like "*manual*") {
            if ($i -gt 0) {
                $projectName = $parts[$i-1]
            }
            # 检查语言
            if ($i + 1 -lt $parts.Length) {
                $nextPart = $parts[$i+1]
                if ($nextPart -in @("de", "es", "ja")) {
                    $lang = $nextPart
                }
            }
            break
        }
    }
    
    return @($projectName, $lang)
}

# 调用 DeepSeek API 重写内容
function Rewrite-Content {
    param(
        [string]$content,
        [string]$projectName,
        [string]$keywords,
        [string]$lang
    )
    
    $prompt = "你不再是翻译官，你是这个项目的首席架构师。
项目名：$projectName，关键词：$keywords，目标语言：$lang。
请彻底重写这段 Markdown，要求如下：
1. 严禁翻译原本的 'Describe feature' 或 '説明する' 等词汇。
2. 根据项目名和关键词，发挥想象力编写 3 个真实的、硬核的技术功能。例如：如果是 champions-sp-calc，你应该写它如何精准计算英雄技能点分配、支持多版本数据对比等。
3. 必须包含具体的参数名、技术指标（如：ミリ秒単位の計算、PostgreSQLとの連携）。
4. 语言必须是 100% 地道的 $lang。
5. 彻底删除 Related Resources 里所有包含 example.com 的假链接。
6. 替换为：👉 `https://www.wangdadi.xyz/?utm_source=github`。
7. 必须生成 3 个详细的操作步骤，内容要显得极度专业。
8. 生成 2 个针对该工具的行业最佳实践建议。
9. 直接输出正文，不要包含任何"好的，这是重写后的内容"之类的废话。

原文：
$content"
    
    $payload = @{
        "model" = $MODEL
        "messages" = @(
            @{
                "role" = "user"
                "content" = $prompt
            }
        )
        "max_tokens" = 2000
        "temperature" = 0.7
    } | ConvertTo-Json -Depth 10
    
    $headers = @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $API_KEY"
    }
    
    try {
        $response = Invoke-RestMethod -Uri $API_ENDPOINT -Method Post -Body $payload -Headers $headers -TimeoutSec 30
        return $response.choices[0].message.content
    } catch {
        Write-Host "API 请求失败: $($_.Exception.Message)"
        return $null
    }
}

# 主函数
function Main {
    # 目标文件路径
    $targetFile = "e:\Developer-Toolbox-by-WangDadi\champions-sp-calc\manual\ja\CHA_013.md"
    
    # 加载项目信息
    $projects = Load-Projects
    
    try {
        # 读取文件内容，使用 utf-8-sig 编码
        $content = Get-Content -Path $targetFile -Encoding UTF8 -Raw
        
        Write-Host "=== 原始内容 ==="
        Write-Host $content
        Write-Host "\n=== 重写内容 ==="
        
        # 提取项目信息
        $projectName, $lang = Extract-Info -filePath $targetFile
        
        # 获取项目关键词
        $keywords = ""
        if ($projectName -and $projects.PSObject.Properties.Name -contains $projectName) {
            $keywords = $projects.$projectName.keywords
        }
        
        # 调用 API 重写
        $rewrittenContent = Rewrite-Content -content $content -projectName $projectName -keywords $keywords -lang $lang
        
        if ($rewrittenContent) {
            Write-Host $rewrittenContent
            
            # 先清空文件内容
            "" | Out-File -FilePath $targetFile -Encoding UTF8
            # 写入新内容，使用 utf-8-sig 编码
            $rewrittenContent | Out-File -FilePath $targetFile -Encoding UTF8
            Write-Host "\n文件已成功重写！"
        } else {
            Write-Host "重写失败！"
        }
    } catch {
        Write-Host "处理文件失败: $($_.Exception.Message)"
    }
}

# 执行主函数
Main