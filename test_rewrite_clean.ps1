# Global variables
$API_KEY = "sk-acea097d87da45508303b0662a398434"
$API_ENDPOINT = "https://api.deepseek.com/chat/completions"
$MODEL = "deepseek-chat"

# Target file path
$targetFile = "e:\Developer-Toolbox-by-WangDadi\champions-sp-calc\manual\ja\CHA_013.md"

# Read file content
$content = Get-Content -Path $targetFile -Encoding UTF8 -Raw

# Clean invalid Unicode characters
function Clean-Unicode {
    param([string]$text)
    $cleaned = $text -replace '[\u0000-\u001F\u007F-\u009F]', ''
    return $cleaned
}

$cleanedContent = Clean-Unicode -text $content

Write-Host "=== Original Content (Cleaned) ==="
Write-Host $cleanedContent.Substring(0, [Math]::Min(500, $cleanedContent.Length)) # Show first 500 chars
Write-Host "..."

# Create simple prompt
$prompt = @"
You are the chief architect of champions-sp-calc. Rewrite this content in Japanese with 3 technical features, 3 operation steps, and 2 best practices. Directly output the main text.

Original text:
$cleanedContent.Substring(0, [Math]::Min(500, $cleanedContent.Length))
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
    "max_tokens" = 1500
    "temperature" = 0.7
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $API_KEY"
}

try {
    Write-Host "\n=== Sending API request... ==="
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
