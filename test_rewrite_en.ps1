# Global variables
$API_KEY = "sk-acea097d87da45508303b0662a398434"
$API_ENDPOINT = "https://api.deepseek.com/chat/completions"
$MODEL = "deepseek-chat"
$PROJECTS_JSON = "projects.json"

# Load projects info
function Load-Projects {
    if (Test-Path $PROJECTS_JSON) {
        $content = Get-Content -Path $PROJECTS_JSON -Encoding UTF8 -Raw
        return $content | ConvertFrom-Json
    }
    return @{}
}

# Extract project name and language from path
function Extract-Info {
    param(
        [string]$filePath
    )
    
    # Extract project name (folder name)
    $parts = $filePath -split '\\'
    $projectName = $null
    $lang = "en"
    
    for ($i = 0; $i -lt $parts.Length; $i++) {
        $part = $parts[$i]
        if ($part -like "*manual*") {
            if ($i -gt 0) {
                $projectName = $parts[$i-1]
            }
            # Check language
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

# Call DeepSeek API to rewrite content
function Rewrite-Content {
    param(
        [string]$content,
        [string]$projectName,
        [string]$keywords,
        [string]$lang
    )
    
    $prompt = "You are no longer a translator, you are the chief architect of this project.
Project name: $projectName, Keywords: $keywords, Target language: $lang.
Please completely rewrite this Markdown with the following requirements:
1. Strictly do not translate original words like 'Describe feature' or '説明する'.
2. Based on the project name and keywords, use your imagination to write 3 real, hardcore technical features. For example, if it's champions-sp-calc, you should write about how it accurately calculates hero skill point allocation, supports multi-version data comparison, etc.
3. Must include specific parameter names and technical indicators (e.g., millisecond-level calculation, PostgreSQL integration).
4. The language must be 100% authentic $lang.
5. Completely delete all fake links containing example.com in Related Resources.
6. Replace with: 👉 `https://www.wangdadi.xyz/?utm_source=github`.
7. Must generate 3 detailed operation steps, content should appear extremely professional.
8. Generate 2 industry best practice recommendations for this tool.
9. Directly output the main text, do not include any nonsense like "Okay, this is the rewritten content".

Original text:
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
        Write-Host "API request failed: $($_.Exception.Message)"
        return $null
    }
}

# Main function
function Main {
    # Target file path
    $targetFile = "e:\Developer-Toolbox-by-WangDadi\champions-sp-calc\manual\ja\CHA_013.md"
    
    # Load projects info
    $projects = Load-Projects
    
    try {
        # Read file content, use UTF-8 encoding
        $content = Get-Content -Path $targetFile -Encoding UTF8 -Raw
        
        Write-Host "=== Original Content ==="
        Write-Host $content
        Write-Host "\n=== Rewritten Content ==="
        
        # Extract project info
        $projectName, $lang = Extract-Info -filePath $targetFile
        
        # Get project keywords
        $keywords = ""
        if ($projectName -and $projects.PSObject.Properties.Name -contains $projectName) {
            $keywords = $projects.$projectName.keywords
        }
        
        # Call API to rewrite
        $rewrittenContent = Rewrite-Content -content $content -projectName $projectName -keywords $keywords -lang $lang
        
        if ($rewrittenContent) {
            Write-Host $rewrittenContent
            
            # First clear file content
            "" | Out-File -FilePath $targetFile -Encoding UTF8
            # Write new content, use UTF-8 encoding
            $rewrittenContent | Out-File -FilePath $targetFile -Encoding UTF8
            Write-Host "\nFile rewritten successfully!"
        } else {
            Write-Host "Rewrite failed!"
        }
    } catch {
        Write-Host "Failed to process file: $($_.Exception.Message)"
    }
}

# Execute main function
Main