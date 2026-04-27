# API Test Script
$API_KEY = "sk-acea097d87da45508303b0662a398434"
$API_ENDPOINT = "https://api.deepseek.com/chat/completions"

# Test simple request
$payload = @{
    "model" = "deepseek-chat"
    "messages" = @(
        @{
            "role" = "user"
            "content" = "Hello, test message"
        }
    )
    "max_tokens" = 100
    "temperature" = 0.7
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $API_KEY"
}

try {
    Write-Host "Sending API request..."
    $response = Invoke-RestMethod -Uri $API_ENDPOINT -Method Post -Body $payload -Headers $headers -TimeoutSec 30
    Write-Host "API response received successfully!"
    Write-Host "Response content:"
    Write-Host $response.choices[0].message.content
} catch {
    Write-Host "API request failed: $($_.Exception.Message)"
    Write-Host "Error details: $($_.ErrorDetails.Message)"
}
