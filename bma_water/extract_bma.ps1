param([switch]$Refresh)
$ErrorActionPreference='Stop'
$source='https://weather.bangkok.go.th/water/summary'
$htmlPath=Join-Path $PSScriptRoot 'source_summary.html'
$utf8=[Text.UTF8Encoding]::new($false)
if($Refresh -or !(Test-Path -LiteralPath $htmlPath)) {
    $response=Invoke-WebRequest -Uri $source -UseBasicParsing -TimeoutSec 45
    [IO.File]::WriteAllText($htmlPath,$response.Content,$utf8)
}
$html=[IO.File]::ReadAllText($htmlPath)
function Read-Array($name) {
    $match=[regex]::Match($html,('(?m)^\s*const '+[regex]::Escape($name)+' = (\[.*\]);\s*$'))
    if(!$match.Success){throw "Source format changed: $name not found"}
    return ,@($match.Groups[1].Value|ConvertFrom-Json)
}
$data=Read-Array 'waterSummaryList'
$districts=Read-Array 'districtList'
if($data.Count -eq 0){throw 'Empty source'}
if(@($data.water_id|Select-Object -Unique).Count -ne $data.Count){throw 'Duplicate station IDs'}
$districtMap=@{}
foreach($d in $districts){$districtMap[[string]$d.district_id]=$d.name}
$retrieved=(Get-Item -LiteralPath $htmlPath).LastWriteTimeUtc.ToString('o')
$receivedThai=(Get-Item -LiteralPath $htmlPath).LastWriteTimeUtc.AddHours(7)
function Clean-Level($v){if($null -eq $v -or $v -eq -99){return $null};return $v}
$rows=@(foreach($d in $data){
    $flood=switch($d.water_status_flood){1{'ปกติ'} 2{'เตือนภัย'} 3{'วิกฤติ'} default{'ไม่ทราบ'}}
    $sensor=switch($d.water_status){1{'ปกติ'} 2{'ขัดข้อง'} default{'ไม่ทราบ'}}
    $age=$null
    $stamp=[datetimeoffset]::MinValue
    $sourceTime=if($d.site_timestamp -is [datetime]){$d.site_timestamp.ToString("yyyy-MM-ddTHH:mm:ss")}else{[string]$d.site_timestamp}
    if($sourceTime){
        $sourceTime=$sourceTime.Trim().Replace(' ','T')
        if($sourceTime -notmatch '(Z|[+-]\d{2}:?\d{2})$'){$sourceTime+='+07:00'}
        if([datetimeoffset]::TryParse($sourceTime,[ref]$stamp)){$age=([datetimeoffset]::Parse($retrieved)-$stamp).TotalMinutes}
    }
    [pscustomobject][ordered]@{
        station_id=$d.water_id;station_code=$d.water_code;station_name=$d.water_name
        district=$districtMap[[string]$d.district_id];canal=$d.river_name
        latitude=$d.latitude;longitude=$d.longitude;observed_at_source=$d.site_timestamp
        water_in_m_msl=(Clean-Level $d.wl_in);water_out01_m_msl=(Clean-Level $d.wl_out01);water_out02_m_msl=(Clean-Level $d.wl_out02)
        has_minus99_source=($d.wl_in -eq -99 -or $d.wl_out01 -eq -99 -or $d.wl_out02 -eq -99)
        age_minutes_at_fetch=$age
        freshness_at_fetch=$(if($null -eq $age){'ไม่ทราบเวลาข้อมูล'}elseif($age -lt 0){'เวลาต้นทางอยู่ในอนาคต'}elseif($age -gt 1440){'ข้อมูลเก่าเกิน 24 ชั่วโมง'}else{'ภายใน 24 ชั่วโมง'})
        older_than_24_hours=($null -ne $age -and $age -gt 1440)
        warning_in_source=$d.warning;critical_in_source=$d.critical
        flood_status_source=$flood;sensor_status_source=$sensor
        flood_status_code=$d.water_status_flood;sensor_status_code=$d.water_status
        source_url=$source;retrieved_at_utc=$retrieved
    }
})
$meta=[ordered]@{
    source_url=$source;retrieved_at_utc=$retrieved;observation_timezone='Asia/Bangkok'
    station_count=$data.Count;unique_station_count=@($data.water_id|Select-Object -Unique).Count
    area_groups_with_stations=@($rows.district|Where-Object{$_}|Select-Object -Unique).Count
    older_than_24_hours=@($rows|Where-Object{$_.older_than_24_hours}).Count
    minus99_source_stations=@($rows|Where-Object{$_.has_minus99_source}).Count
    oldest_observation=($data.site_timestamp|Where-Object{$_}|Sort-Object|Select-Object -First 1)
    newest_observation=($data.site_timestamp|Where-Object{$_}|Sort-Object|Select-Object -Last 1)
    missing_timestamp=@($data|Where-Object{!$_.site_timestamp}).Count
    missing_coordinates=@($data|Where-Object{$null -eq $_.latitude -or $null -eq $_.longitude}).Count
    missing_all_water_values=@($data|Where-Object{$null -eq $_.wl_in -and $null -eq $_.wl_out01 -and $null -eq $_.wl_out02}).Count
    flood_status_counts=@($rows|Group-Object flood_status_source|Select-Object Name,Count)
    sensor_status_counts=@($rows|Group-Object sensor_status_source|Select-Object Name,Count)
    notes=@('Snapshot only, not a historical time series.','Raw source values and status codes are preserved; no alert thresholds recalculated.','Water levels are relative to mean sea level, not street flood depth.','Blank or null is not zero. Source thresholds require validation before reuse, especially across water_system_id.','Source timestamps are shown unchanged and interpreted as Thai local time.','Flood status is distinct from sensor status and observation freshness.')
}
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'stations_raw.json'),(ConvertTo-Json -InputObject $data -Depth 20),$utf8)
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'stations.json'),(ConvertTo-Json -InputObject $rows -Depth 10),$utf8)
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'metadata.json'),(ConvertTo-Json -InputObject $meta -Depth 10),$utf8)
function Esc($v){[Net.WebUtility]::HtmlEncode([string]$v)}
$body=($rows|Sort-Object district,station_name|ForEach-Object {
    $row=$_
    $cells=@($row.station_code,$row.station_name,$row.district,$row.canal,$row.water_in_m_msl,$row.water_out01_m_msl,$row.water_out02_m_msl,$row.flood_status_source,$row.sensor_status_source,$row.observed_at_source,$row.latitude,$row.longitude)
    '<tr>'+ (($cells|ForEach-Object{'<td>'+(Esc $_)+'</td>'}) -join '')+'</tr>'
}) -join "`n"
$headers=@('รหัส','สถานี','เขต','คลอง','ระดับน้ำใน','ระดับน้ำนอก 1','ระดับน้ำนอก 2','สถานะน้ำต้นทาง','เครื่องวัด','เวลาวัด (ไทย)','ละติจูด','ลองจิจูด')
$head=($headers|ForEach-Object{'<th>'+(Esc $_)+'</th>'}) -join ''
$page=@"
<!doctype html><html lang="th"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ข้อมูลระดับน้ำ กทม.</title>
<style>body{font:16px Tahoma,sans-serif;margin:28px;color:#183042;background:#f5f8fa}h1{font-size:26px}p{line-height:1.7}input{padding:12px;width:360px;max-width:90%;margin:10px 0}table{border-collapse:collapse;background:white;font-size:14px;width:100%}th,td{padding:10px;border:1px solid #dae2e7;text-align:left}th{background:#174b64;color:white;position:sticky;top:0}tr:nth-child(even){background:#eef4f7}.scroll{overflow:auto;max-height:75vh}td:nth-child(n+5){white-space:nowrap}</style>
<h1>ข้อมูลระดับน้ำ สำนักการระบายน้ำ กทม.</h1><p>ข้อมูลที่ดึงมา $($data.Count) สถานี • $($meta.area_groups_with_stations) กลุ่มเขต/อำเภอตามต้นทาง รวมพื้นที่นอก กทม.<br>เวลาวัดล่าสุดในชุดข้อมูล: $(Esc $meta.newest_observation) (เวลาไทย)<br>เวลารับข้อมูล UTC: $(Esc $retrieved) • <a href="$source">เว็บไซต์ต้นทาง</a></p>
<p>เป็นข้อมูล ณ รอบที่ดาวน์โหลด ไม่อัปเดตอัตโนมัติ ระดับน้ำมีหน่วย ม.รทก. ไม่ใช่ความลึกน้ำท่วมถนน<br>ช่องว่างหมายถึงไม่มีค่าหรือพบค่า -99 ที่พักไว้ ไม่ใช่ศูนย์ (เก็บค่าเดิมครบใน stations_raw.json)<br>ข้อมูลเกิน 24 ชั่วโมง $($meta.older_than_24_hours) สถานี พบค่า -99 จำนวน $($meta.minus99_source_stations) สถานี<br>สถานะน้ำยึดตามต้นทาง ต้องพิจารณาเวลาและสถานะเครื่องวัดร่วมกัน รหัสเครื่องวัด 0 และ 3 ยังไม่ยืนยันความหมาย จึงแสดงว่าไม่ทราบ</p>
<input id="search" placeholder="ค้นหาสถานี เขต คลอง หรือสถานะ" aria-label="ค้นหา"><span id="count">$($rows.Count) สถานี</span>
<div class="scroll"><table><thead><tr>$head</tr></thead><tbody>$body</tbody></table></div>
<script>document.getElementById('search').addEventListener('input',function(){let n=0;document.querySelectorAll('tbody tr').forEach(r=>{let show=r.textContent.toLowerCase().includes(this.value.toLowerCase());r.hidden=!show;if(show)n++});document.getElementById('count').textContent=n+' สถานี'});</script></html>
"@
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'stations.html'),$page,$utf8)
$meta|ConvertTo-Json -Depth 10
