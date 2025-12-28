# Update all HTML file paths to use new frontend structure
$htmlFiles = Get-ChildItem -Path "frontend/pages/*.html"

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Update CSS paths
    $content = $content -replace 'href="css/', 'href="../css/'
    $content = $content -replace 'href="css/style\.css"', 'href="../css/main.css"'
    $content = $content -replace 'href="css/layout\.css"', 'href="../css/main.css"'
    $content = $content -replace 'href="css/components\.css"', 'href="../css/main.css"'
    $content = $content -replace 'href="css/animations\.css"', 'href="../css/main.css"'
    
    # Remove duplicate CSS imports - keep only main.css
    $content = $content -replace '  <link rel="stylesheet" href="\.\./css/main\.css">\r?\n  <link rel="stylesheet" href="\.\./css/main\.css">\r?\n  <link rel="stylesheet" href="\.\./css/main\.css">\r?\n  <link rel="stylesheet" href="\.\./css/main\.css">', '  <link rel="stylesheet" href="../css/main.css">'
    
    # Update JS paths
    $content = $content -replace 'src="js/validation\.js"', 'src="../js/core/validation.js"'
    $content = $content -replace 'src="js/storage\.js"', 'src="../js/core/storage.js"'
    $content = $content -replace 'src="js/navigation\.js"', 'src="../js/core/navigation.js"'
    $content = $content -replace 'src="js/ui\.js"', 'src="../js/core/ui.js"'
    $content = $content -replace 'src="js/config\.js"', 'src="../js/config/config.js"'
    $content = $content -replace 'src="js/analysis\.js"', 'src="../js/analysis/analysis.js"'
    $content = $content -replace 'src="js/resume\.js"', 'src="../js/analysis/resume.js"'
    $content = $content -replace 'src="js/result\.js"', 'src="../js/analysis/result.js"'
    $content = $content -replace 'src="js/button-state\.js"', 'src="../js/utils/button-state.js"'
    
    # Update asset paths
    $content = $content -replace 'src="assets/', 'src="../assets/'
    
    # Update navigation links
    $content = $content -replace 'href="index\.html"', 'href="index.html"'
    $content = $content -replace 'href="check\.html"', 'href="check.html"'
    $content = $content -replace 'href="analysis\.html"', 'href="analysis.html"'
    $content = $content -replace 'href="result\.html"', 'href="result.html"'
    $content = $content -replace 'href="workflow\.html"', 'href="workflow.html"'
    $content = $content -replace 'href="about\.html"', 'href="about.html"'
    $content = $content -replace 'href="contact\.html"', 'href="contact.html"'
    $content = $content -replace 'href="resume-templates\.html"', 'href="resume-templates.html"'
    
    Set-Content -Path $file.FullName -Value $content -NoNewline
}

Write-Host "All HTML files updated with new paths" -ForegroundColor Green
