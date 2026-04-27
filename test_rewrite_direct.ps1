# Global variables
$API_KEY = "sk-acea097d87da45508303b0662a398434"
$API_ENDPOINT = "https://api.deepseek.com/chat/completions"
$MODEL = "deepseek-chat"

# Target file path
$targetFile = "e:\Developer-Toolbox-by-WangDadi\champions-sp-calc\manual\ja\CHA_013.md"

# Create a clean prompt without using the original file content
$prompt = @"
You are the chief architect of champions-sp-calc, a tool for calculating hero skill points in games. Please create a comprehensive Japanese technical document for this project with the following sections:

1. Project Overview
2. Core Features (3 technical features with specific parameters and metrics)
3. Operation Steps (3 detailed steps)
4. Best Practices (2 industry recommendations)
5. Related Resources (with link to https://www.wangdadi.xyz/?utm_source=github)

Write in authentic Japanese and include technical details like millisecond-level calculations, PostgreSQL integration, etc.
"@

# Prepare API request
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
    Write-Host "=== Sending API request... ==="
    $response = Invoke-RestMethod -Uri $API_ENDPOINT -Method Post -Body $payload -Headers $headers -TimeoutSec 30
    
    $rewrittenContent = $response.choices[0].message.content
    
    Write-Host "\n=== Rewritten Content ==="
    Write-Host $rewrittenContent
    
    # First clear file content
    "" | Out-File -FilePath $targetFile -Encoding UTF8
    # Write new content
    $rewrittenContent | Out-File -FilePath $targetFile -Encoding UTF8
    Write-Host "\nFile rewritten successfully!"
} catch {
    Write-Host "API request failed: $($_.Exception.Message)"
    Write-Host "Error details: $($_.ErrorDetails.Message)"
}
