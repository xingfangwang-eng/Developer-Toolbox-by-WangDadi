# 全局变量
$API_KEY = "sk-acea097d87da45508303b0662a398434"
$API_ENDPOINT = "https://api.deepseek.com/chat/completions"
$MODEL = "deepseek-chat"

# 目标文件路径
$targetFile = "e:\Developer-Toolbox-by-WangDadi\champions-sp-calc\manual\ja\CHA_013.md"

# 创建提示词
$prompt = @"
You are the chief architect of champions-sp-calc, a tool for calculating hero skill points in games. Please create a comprehensive Japanese technical document for this project with the following sections:

1. Project Overview
2. Core Features (3 technical features with specific parameters and metrics)
3. Operation Steps (3 detailed steps)
4. Best Practices (2 industry recommendations)
5. Related Resources (with link to https://www.wangdadi.xyz/?utm_source=github)

Write in authentic Japanese and include technical details like millisecond-level calculations, PostgreSQL integration, etc.
"@

# 准备 API 请求
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
    Write-Host "发送 API 请求..."
    $response = Invoke-RestMethod -Uri $API_ENDPOINT -Method Post -Body $payload -Headers $headers -TimeoutSec 30
    
    $content = $response.choices[0].message.content
    
    Write-Host "\n生成的内容:"
    Write-Host $content
    
    # 使用 .NET 方法写入文件，确保使用 utf-8-sig 编码
    [System.IO.File]::WriteAllText($targetFile, $content, [System.Text.Encoding]::UTF8)
    
    Write-Host "\n文件已成功重写并使用 UTF-8 编码保存！"
} catch {
    Write-Host "API 请求失败: $($_.Exception.Message)"
    Write-Host "错误详情: $($_.ErrorDetails.Message)"
}
