# ============================================
# Monitoring PBL - RKS203
# Polibatam - Windows Server 2025
# ============================================

# === KONFIGURASI DISCORD WEBHOOK ===
$WebhookURL = "https://discord.com/api/webhooks/1522156235753783368/9CRWhmYofNrxGcX5L8pw4D4iFbXG3QxP_L5TNM8-r6T9PzPyASg8BNs4S2bar7_LXKJJ"

# === FUNGSI KIRIM KE DISCORD ===
function Send-DiscordAlert {
    param([string]$Message, [string]$Color = "3066993")
    
    $Body = @{
        embeds = @(@{
            title       = "🖥️ Monitoring PBL - Windows Server"
            description = $Message
            color       = [int]$Color
            footer      = @{ text = "polibatam.local | $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')" }
        })
    } | ConvertTo-Json -Depth 10

    Invoke-RestMethod -Uri $WebhookURL -Method Post -Body $Body -ContentType "application/json"
}

# === 1. MONITORING CPU ===
$CPU = (Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
$CPUStatus = if ($CPU -gt 80) { "🔴 TINGGI" } elseif ($CPU -gt 50) { "🟡 SEDANG" } else { "🟢 NORMAL" }

# === 2. MONITORING RAM ===
$OS = Get-CimInstance Win32_OperatingSystem
$RAMTotal = [math]::Round($OS.TotalVisibleMemorySize / 1MB, 2)
$RAMFree = [math]::Round($OS.FreePhysicalMemory / 1MB, 2)
$RAMUsed = [math]::Round($RAMTotal - $RAMFree, 2)
$RAMPercent = [math]::Round(($RAMUsed / $RAMTotal) * 100, 1)
$RAMStatus = if ($RAMPercent -gt 80) { "🔴 TINGGI" } elseif ($RAMPercent -gt 50) { "🟡 SEDANG" } else { "🟢 NORMAL" }

# === 3. MONITORING DISK ===
$Disk = Get-PSDrive C | Select-Object Used, Free
$DiskTotal = [math]::Round(($Disk.Used + $Disk.Free) / 1GB, 2)
$DiskUsed = [math]::Round($Disk.Used / 1GB, 2)
$DiskPercent = [math]::Round(($DiskUsed / $DiskTotal) * 100, 1)
$DiskStatus = if ($DiskPercent -gt 80) { "🔴 TINGGI" } elseif ($DiskPercent -gt 50) { "🟡 SEDANG" } else { "🟢 NORMAL" }

# === 4. MONITORING SERVICE ===
$Services = @("W3SVC", "ADWS", "DNS")
$ServiceNames = @{"W3SVC"="IIS Web Server"; "ADWS"="Active Directory"; "DNS"="DNS Server"}
$ServiceReport = ""
$AlertColor = "3066993" # Hijau default

foreach ($svc in $Services) {
    $status = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($status.Status -eq "Running") {
        $ServiceReport += "✅ $($ServiceNames[$svc]): **Running**`n"
    } else {
        $ServiceReport += "❌ $($ServiceNames[$svc]): **STOPPED**`n"
        $AlertColor = "15158332" # Merah kalau ada service mati
    }
}

# === 5. SUSUN PESAN ===
$Message = @"
**📊 Laporan Monitoring Sistem**

**💻 CPU Usage**
> $CPU% — $CPUStatus

**🧠 RAM Usage**
> $RAMUsed GB / $RAMTotal GB ($RAMPercent%) — $RAMStatus

**💾 Disk C: Usage**
> $DiskUsed GB / $DiskTotal GB ($DiskPercent%) — $DiskStatus

**⚙️ Status Services**
$ServiceReport
"@

# === 6. KIRIM KE DISCORD ===
Send-DiscordAlert -Message $Message -Color $AlertColor
Write-Host "✅ Notifikasi berhasil dikirim ke Discord!" -ForegroundColor Green
Write-Host "Waktu: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')" -ForegroundColor Cyan