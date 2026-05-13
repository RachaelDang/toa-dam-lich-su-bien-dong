"""
=============================================================
   SETUP GOOGLE SHEET CHO HỆ THỐNG BÌNH CHỌN
=============================================================
Yêu cầu: Python 3.8+
Cài đặt:  pip install gspread google-auth
=============================================================
"""

import json
import os

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    print("❌ Chưa cài thư viện. Đang cài đặt tự động...")
    os.system("pip install gspread google-auth")
    print("✅ Đã cài đặt. Vui lòng chạy lại script này.\n")
    print("   python setup_google_sheet.py")
    exit()

# ============================================================
# BƯỚC 1: Tạo Google Service Account
# ============================================================
print("=" * 60)
print("  BƯỚC 1: Tạo Service Account")
print("=" * 60)
print("""
1. Truy cập: https://console.cloud.google.com/
2. Tạo project mới (hoặc dùng project hiện có)
3. Vào APIs & Services → Library → Bật "Google Sheets API"
4. Vào APIs & Services → Credentials → Create Credentials → Service Account
5. Đặt tên, chọn role "Editor"
6. Tạo xong → Tải file JSON key về
7. Đặt file JSON này vào cùng folder với script này
""")

credentials_file = input("\n📁 Nhập tên file JSON credentials (VD: my-project-12345.json): ").strip()

if not os.path.exists(credentials_file):
    print(f"\n❌ Không tìm thấy file '{credentials_file}'. Đảm bảo file nằm trong cùng folder.")
    print("   Tải credentials JSON từ Google Cloud Console rồi đặt vào đây.")
    exit()

# ============================================================
# BƯỚC 2: Authorize & Tạo Sheet
# ============================================================
print("\n" + "=" * 60)
print("  BƯỚC 2: Tạo Google Sheet")
print("=" * 60)

scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

try:
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    gc = gspread.authorize(creds)
    print("✅ Đã kết nối Google API thành công!")
except Exception as e:
    print(f"❌ Lỗi xác thực: {e}")
    exit()

# Tạo spreadsheet mới
sheet_name = "Bình chọn Diễn Đàn Biển Đông"
try:
    sh = gc.create(sheet_name)
    print(f"✅ Đã tạo Google Sheet: '{sheet_name}'")
except Exception as e:
    print(f"❌ Lỗi tạo sheet: {e}")
    exit()

# ============================================================
# BƯỚC 3: Setup bảng votes
# ============================================================
print("\n" + "=" * 60)
print("  BƯỚC 3: Tạo bảng bình chọn")
print("=" * 60)

worksheet = sh.sheet1
countries = ['vietnam', 'china', 'cambodia', 'taiwan', 'indonesia',
             'philippines', 'thailand', 'malaysia', 'singapore', 'brunei']

# Header
worksheet.update_cell(1, 1, "Country")
worksheet.update_cell(1, 2, "Votes")
worksheet.update_cell(1, 3, "VotedClients")
worksheet.update_cell(1, 4, "LastUpdated")

# Tạo hàng cho mỗi quốc gia với emoji flag
flags = {
    'vietnam': '🇻🇳', 'china': '🇨🇳', 'cambodia': '🇰🇭',
    'taiwan': '🇹🇼', 'indonesia': '🇮🇩', 'philippines': '🇵🇭',
    'thailand': '🇹🇭', 'malaysia': '🇲🇾', 'singapore': '🇸🇬', 'brunei': '🇧🇳'
}

for i, country in enumerate(countries, start=2):
    worksheet.update_cell(i, 1, f"{flags[country]} {country}")
    worksheet.update_cell(i, 2, 0)
    worksheet.update_cell(i, 3, "")
    worksheet.update_cell(i, 4, "")

print(f"✅ Đã tạo bảng với {len(countries)} quốc gia")

# ============================================================
# BƯỚC 4: Tạo Apps Script
# ============================================================
print("\n" + "=" * 60)
print("  BƯỚC 4: Tạo Apps Script backend")
print("=" * 60)

apps_script_code = '''
function doGet(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  var votes = {};
  for (var i = 1; i < data.length; i++) {
    var country = String(data[i][0]).replace(/^.*?\\\\s+/, '').trim();
    // Fallback: lấy từ cột A nguyên
    if (!country) country = data[i][0];
    votes[country] = parseInt(data[i][1]) || 0;
  }
  return ContentService.createTextOutput(JSON.stringify(votes))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    var parameter = JSON.parse(e.postData.contents);
    if (parameter.action === 'reset') {
      setupSheet();
      return ContentService.createTextOutput(JSON.stringify({success: true}))
        .setMimeType(ContentService.MimeType.JSON);
    }
    var country = parameter.country;
    var clientId = parameter.clientId || 'unknown';
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var data = sheet.getDataRange().getValues();
    for (var i = 1; i < data.length; i++) {
      var rowCountry = data[i][0];
      if (String(rowCountry).indexOf(country) !== -1) {
        var votedClients = data[i][2] ? String(data[i][2]).split(',') : [];
        if (votedClients.indexOf(clientId) !== -1) {
          return ContentService.createTextOutput(JSON.stringify({
            success: false, message: 'Bạn đã bình chọn rồi'
          })).setMimeType(ContentService.MimeType.JSON);
        }
        votedClients.push(clientId);
        sheet.getRange(i + 1, 2).setValue(parseInt(data[i][1]) + 1);
        sheet.getRange(i + 1, 3).setValue(votedClients.join(','));
        break;
      }
    }
    return ContentService.createTextOutput(JSON.stringify({success: true}))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false, message: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function setupSheet() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.clear();
  sheet.appendRow(['Country', 'Votes', 'VotedClients', 'LastUpdated']);
  var countries = ['vietnam','china','cambodia','taiwan','indonesia',
    'philippines','thailand','malaysia','singapore','brunei'];
  var flags = {vietnam:'🇻🇳',china:'🇨🇳',cambodia:'🇰🇭',taiwan:'🇹🇼',
    indonesia:'🇮🇩',philippines:'🇵🇭',thailand:'🇹🇭',malaysia:'🇲🇾',
    singapore:'🇸🇬',brunei:'🇧🇳'};
  countries.forEach(function(c) {
    sheet.appendRow([flags[c] + ' ' + c, 0, '', '']);
  });
}
'''

# Tạo Apps Script project trong Sheet
try:
    project = sh.create_spreadsheet_apps_script("VoteBackend", apps_script_code)
    print(f"✅ Đã tạo Apps Script 'VoteBackend' trong Sheet")
except Exception as e:
    print(f"⚠️ Lỗi tạo Apps Script: {e}")
    print("   Bạn cần tự tạo Apps Script thủ công (xem hướng dẫn)")

# ============================================================
# BƯỚC 5: Làm cho Sheet public
# ============================================================
print("\n" + "=" * 60)
print("  BƯỚC 5: Chia sẻ Sheet (Public)")
print("=" * 60)

try:
    sh.share("", role="reader", notify=False)  # public read
    print("✅ Đã đặt Sheet ở chế độ công khai (ai cũng xem được)")
except Exception as e:
    print(f"⚠️ Không thể chia sẻ tự động: {e}")
    print("   → Vào Google Sheet → Share → 'Anyone with the link' → Viewer")

# ============================================================
# BƯỚC 6: Deploy Apps Script
# ============================================================
print("\n" + "=" * 60)
print("  BƯỚC 6: Deploy Apps Script")
print("=" * 60)
print("""
⚠️  Bước này PHẢI làm thủ công:

1. Mở Google Sheet vừa tạo
2. Extensions → Apps Script
3. Tìm file 'VoteBackend' (đã được tạo)
4. Nhấn ▶ Deploy → New deployment
5. Chọn:
   - Type: Web app
   - Execute as: Me
   - Who has access: Anyone
6. Nhấn Deploy
7. **Copy URL** (dạng https://script.google.com/macros/s/.../exec)
""")

# ============================================================
# BƯỚC 7: Cập nhật debate.html tự động
# ============================================================
print("=" * 60)
print("  BƯỚC 7: Tạo debate.html đã cấu hình URL")
print("=" * 60)

script_url = input("\n📋 Dán URL Apps Script Web App vừa deploy: ").strip()

if script_url.startswith("https://script.google.com/macros/s/"):
    # Tạo debate.html với URL đã cấu hình
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tranh luận & Bình chọn - Diễn Đàn Biển Đông</title>
    <link rel="stylesheet" href="style.css">
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="main.js" defer></script>
</head>
<body>
    <header class="header">
        <div class="header-left">
            <a href="index.html" class="logo"><i class='bx bx-globe'></i> Diễn Đàn Biển Đông</a>
            <p class="tagline">Đối thoại - Hợp tác - Hòa bình</p>
        </div>
        <div class="header-right">
            <nav class="navbar">
                <a href="index.html" style="--i:1">Trang chủ</a>
                <a href="context.html" style="--i:2">Bối cảnh</a>
                <a href="delegates.html" style="--i:3">Đại biểu</a>
                <a href="debate.html" style="--i:4" class="active">Tranh luận & Bình chọn</a>
                <a href="statement.html" style="--i:5">Tuyên bố chung</a>
            </nav>
            <div class="dkn-box"><span class="dkn">DKN KND</span></div>
        </div>
    </header>
    <section class="debate-page">
        <div class="debate-content">
            <h1>Tranh luận & Bình chọn</h1>
            <div class="debate-grid">
                <div class="debate-item">
                    <h3>Chủ đề tranh luận</h3>
                    <p style="color:#fff;margin-bottom:20px;font-size:18px;font-weight:600;">Chủ quyền Biển Đông</p>
                </div>
                <div class="debate-item">
                    <h3>Bình chọn đại biểu ưu tú</h3>
                    <p style="color:#ccc;margin-bottom:20px;font-size:14px;">Bình chọn cho đại biểu thể hiện tốt nhất quan điểm</p>
                    <button class="vote-btn" onclick="scrollToVote()">Bắt đầu bình chọn</button>
                </div>
            </div>
            <div class="vote-grid" id="voteGrid">
                <div class="vote-card" data-country="vietnam">
                    <span class="vote-flag">🇻🇳</span><h3>Vietnam</h3>
                    <span class="vote-count" id="count-vietnam">0</span>
                    <button class="vote-btn-sm" onclick="vote('vietnam')">Bình chọn</button>
                </div>
                <div class="vote-card" data-country="china">
                    <span class="vote-flag">🇨🇳</span><h3>China</h3>
                    <span class="vote-count" id="count-china">0</span>
                    <button class="vote-btn-sm" onclick="vote('china')">Bình chọn</button>
                </div>
                <div class="vote-card" data-country="cambodia">
                    <span class="vote-flag">🇰🇭</span><h3>Cambodia</h3>
                    <span class="vote-count" id="count-cambodia">0</span>
                    <button class="vote-btn-sm" onclick="vote('cambodia')">Bình chọn</button>
                </div>
                <div class="vote-card" data-country="taiwan">
                    <span class="vote-flag">🇹🇼</span><h3>Taiwan</h3>
                    <span class="vote-count" id="count-taiwan">0</span>
                    <button class="vote-btn-sm" onclick="vote('taiwan')">Bình chọn</button>
                </div>
                <div class="vote-card" data-country="indonesia">
                    <span class="vote-flag">🇮🇩</span><h3>Indonesia</h3>
                    <span class="vote-count" id="count-indonesia">0</span>
                    <button class="vote-btn-sm" onclick="vote('indonesia')">Bình chọn</button>
                </div>
                <div class="vote-card" data-country="philippines">
                    <span class="vote-flag">🇵🇭</span><h3>Philippines</h3>
                    <span class="vote-count" id="count-philippines">0</span>
                    <button class="vote-btn-sm" onclick="vote('philippines')">Bình chọn</button>
                </div>
                <div class="vote-card" data-country="thailand">
                    <span class="vote-flag">🇹🇭</span><h3>Thailand</h3>
                    <span class="vote-count" id="count-thailand">0</span>
                    <button class="vote-btn-sm" onclick="vote('thailand')">Bình chọn</button>
                </div>
                <div class="vote-card" data-country="malaysia">
                    <span class="vote-flag">🇲🇾</span><h3>Malaysia</h3>
                    <span class="vote-count" id="count-malaysia">0</span>
                    <button class="vote-btn-sm" onclick="vote('malaysia')">Bình chọn</button>
                </div>
                <div class="vote-card" data-country="singapore">
                    <span class="vote-flag">🇸🇬</span><h3>Singapore</h3>
                    <span class="vote-count" id="count-singapore">0</span>
                    <button class="vote-btn-sm" onclick="vote('singapore')">Bình chọn</button>
                </div>
                <div class="vote-card" data-country="brunei">
                    <span class="vote-flag">🇧🇳</span><h3>Brunei</h3>
                    <span class="vote-count" id="count-brunei">0</span>
                    <button class="vote-btn-sm" onclick="vote('brunei')">Bình chọn</button>
                </div>
            </div>
            <div class="results-section">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px;">
                    <h2>Kết quả bình chọn</h2>
                    <div style="display:flex;gap:10px;align-items:center;">
                        <span id="loadingStatus" style="font-size:13px;color:aaa;">🔴 Chưa kết nối</span>
                        <button class="vote-btn-sm reset-btn" onclick="resetVotes()">🔄 Reset</button>
                    </div>
                </div>
                <div class="results-list" id="resultsList">
                    <p style="text-align:center;color:#ccc;">Đang tải kết quả...</p>
                </div>
            </div>
        </div>
    </section>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script>
        const SHEETS_URL = '%%SCRIPT_URL%%';
        const CLIENT_ID = (function(){var c=localStorage.getItem('dcid');if(!c){c='c_'+Date.now()+'_'+Math.random().toString(36).substr(2,9);localStorage.setItem('dcid',c)}return c})();
        const COUNTRIES=['vietnam','china','cambodia','taiwan','indonesia','philippines','thailand','malaysia','singapore','brunei'];
        const COUNTRY_NAMES={vietnam:'Vietnam',china:'China',cambodia:'Cambodia',taiwan:'Taiwan',indonesia:'Indonesia',philippines:'Philippines',thailand:'Thailand',malaysia:'Malaysia',singapore:'Singapore',brunei:'Brunei'};
        var votesCache={};COUNTRIES.forEach(function(c){votesCache[c]=0;});

        function getVotesLocal(){var s=localStorage.getItem('dv');return s?JSON.parse(s):{}}
        function saveVotesLocal(v){localStorage.setItem('dv',JSON.stringify(v))}

        async function fetchVotes(){
            var loadingEl=document.getElementById('loadingStatus');
            if(!SHEETS_URL||SHEETS_URL==='%%SCRIPT_URL%%'||!SHEETS_URL.startsWith('https://')){
                var stored=getVotesLocal();
                if(stored)votesCache=stored;
                updateUI();
                if(loadingEl)loadingEl.textContent='⚠️ Local mode (chưa cấu hình URL)';
                return;
            }
            try{
                var res=await fetch(SHEETS_URL);
                if(!res.ok)throw new Error(res.status);
                var remote=await res.json();
                COUNTRIES.forEach(function(c){var v=0;for(var k in remote){if(String(k).toLowerCase().indexOf(c)!==-1)v=Math.max(v,parseInt(remote[k])||0);}votesCache[c]=v;});
                saveVotesLocal(votesCache);updateUI();
                if(loadingEl)loadingEl.textContent='🟢 Đã kết nối';
            }catch(err){
                console.warn('Fetch error:',err);
                var fb=getVotesLocal();if(fb)votesCache=fb;updateUI();
                if(loadingEl)loadingEl.textContent='🔴 Lỗi kết nối - dùng local';
            }
        }

        async function sendVote(country){
            if(!SHEETS_URL||SHEETS_URL==='%%SCRIPT_URL%%'||!SHEETS_URL.startsWith('https://')){
                var key='dv_'+CLIENT_ID,arr=JSON.parse(localStorage.getItem(key)||'[]');
                if(arr.indexOf(country)!==-1)return false;
                arr.push(country);localStorage.setItem(key,JSON.stringify(arr));
                votesCache[country]=(votesCache[country]||0)+1;
                saveVotesLocal(votesCache);return true;
            }
            try{
                var key='dv_'+CLIENT_ID,arr=JSON.parse(localStorage.getItem(key)||'[]');
                if(arr.indexOf(country)!==-1){alert('Bạn đã bình chọn rồi!');return false;}
                var res=await fetch(SHEETS_URL,{method:'POST',headers:{'Content-Type':'application/json'},
                    body:JSON.stringify({country:country,clientId:CLIENT_ID})});
                var result=await res.json();
                if(result.success){arr.push(key,country);localStorage.setItem(key,JSON.stringify(arr));
                    votesCache[country]=(votesCache[country]||0)+1;return true;}
                if(result.message)alert(result.message);return false;
            }catch(err){alert('Lỗi:'+err.message);return false;}
        }

        async function vote(country){
            var ok=await sendVote(country);
            if(ok){
                updateUI();
                var btn=document.querySelector('.vote-card[data-country="'+country+'"] .vote-btn-sm');
                if(btn){btn.disabled=true;btn.textContent='✓ Đã bình chọn';}
                var card=document.querySelector('.vote-card[data-country="'+country+'"]');
                if(card)card.classList.add('voted');
            }
        }

        async function resetVotes(){
            if(!confirm('Reset TẤT CẢ bình chọn?'))return;
            if(SHEETS_URL&&SHEETS_URL!=='%%SCRIPT_URL%%'&&confirm('Cũng reset trên Google Sheets?')){
                try{
                    var res=await fetch(SHEETS_URL,{method:'POST',headers:{'Content-Type':'application/json'},
                        body:JSON.stringify({action:'reset'})});
                    var r=await res.json();
                    if(r.success)alert('Đã reset trên Google Sheets!');
                }catch(e){alert('Lỗi reset server');}
            }
            votesCache={};COUNTRIES.forEach(function(c){votesCache[c]=0;});
            localStorage.setItem('dv',JSON.stringify(votesCache));
            localStorage.removeItem('dv_'+CLIENT_ID);
            updateUI();
            document.querySelectorAll('.vote-card .vote-btn-sm').forEach(function(b){b.disabled=false;b.textContent='Bình chọn';});
            document.querySelectorAll('.vote-card.voted').forEach(function(c){c.classList.remove('voted');});
        }

        function updateUI(){
            var total=0;COUNTRIES.forEach(function(c){total+=votesCache[c]||0;});
            COUNTRIES.forEach(function(country){
                var el=document.getElementById('count-'+country);
                if(el)el.textContent=votesCache[country]||0;
            });
            var rl=document.getElementById('resultsList');
            if(!rl)return;
            if(total===0){rl.innerHTML='<p style="text-align:center;color:#ccc;">Chưa có phiếu bầu nào</p>';return;}
            rl.innerHTML='';
            COUNTRIES.slice().sort(function(a,b){return(votesCache[b]||0)-(votesCache[a]||0);}).forEach(function(country){
                var c=votesCache[country]||0,p=total>0?((c/total)*100).toFixed(1):0;
                var item=document.createElement('div');item.className='result-item';
                item.innerHTML='<span class="result-flag">'+getFlagEmoji(country)+'</span>'+
                    '<div class="result-info"><div class="result-country">'+COUNTRY_NAMES[country]+'</div>'+
                    '<div class="result-bar-bg"><div class="result-bar" style="width:'+p+'%"></div></div></div>'+
                    '<div class="result-stats">'+c+' ('+p+'%)</div>';
                rl.appendChild(item);
            });
        }

        function getFlagEmoji(c){var f={vietnam:'🇻🇳',china:'🇨🇳',cambodia:'🇰🇭',taiwan:'🇹🇼',
            indonesia:'🇮🇩',philippines:'🇵🇭',thailand:'🇹🇭',malaysia:'🇲🇾',singapore:'🇸🇬',brunei:'🇧🇳'};return f[c]||'🏳️';}
        function scrollToVote(){document.getElementById('voteGrid').scrollIntoView({behavior:'smooth'});}

        fetchVotes();
        setInterval(function(){fetchVotes();},5000);
    </script>
</body>
</html>'''

    # Thay placeholder bằng URL thật
    html_content = html_content.replace('%%SCRIPT_URL%%', script_url)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debate.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"\n✅ Đã ghi file: {output_path}")

else:
    print("\n❌ URL không hợp lệ. URL phải bắt đầu bằng https://script.google.com/macros/s/")

print("\n" + "=" * 60)
print("  TẤT CẢ ĐÃ HOÀN TẤT!")
print("=" * 60)
print("""
📁 File đã tạo/bị cập nhật:
   • debate.html — Website bình chọn (đã cấu hình URL)
   • code.gs     — Google Apps Script

📌 Cách deploy Google Sheets:
   https://docs.google.com/spreadsheets/d/SHEET_ID
   
📌 Cách deploy Apps Script:
   Extensions → Apps Script → Deploy → New deployment → Web app

🌐 Deploy website:
   Dùng Netlify: kéo thả folder chứa file HTML
""")