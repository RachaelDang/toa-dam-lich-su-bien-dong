// Google Apps Script - Code.gs
// Deploy as Web App (Execute as: Me, Who has access: Anyone)

function doGet(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  var votes = {};
  for (var i = 1; i < data.length; i++) {
    votes[data[i][0]] = parseInt(data[i][1]) || 0;
  }
  return ContentService.createTextOutput(JSON.stringify(votes))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
   try {
     var parameter = JSON.parse(e.postData.contents);

     // Handle reset action
     if (parameter.action === 'reset') {
       setupSheet();
       return ContentService.createTextOutput(JSON.stringify({success: true}))
         .setMimeType(ContentService.MimeType.JSON);
     }

     var country = parameter.country;
     var clientId = parameter.clientId || 'unknown';

     var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
     var data = sheet.getDataRange().getValues();

     // Kiểm tra trùng lặp theo clientId trong cột C
     for (var i = 1; i < data.length; i++) {
       if (data[i][0] === country) {
         var votedClients = data[i][2] ? String(data[i][2]).split(',') : [];
         if (votedClients.indexOf(clientId) !== -1) {
           return ContentService.createTextOutput(JSON.stringify({
             success: false,
             message: 'Bạn đã bình chọn cho quốc gia này rồi'
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
       success: false,
       message: error.toString()
     })).setMimeType(ContentService.MimeType.JSON);
   }
 }

// Khởi tạo sheet nếu chưa có dữ liệu
function setupSheet() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.clear();
  sheet.appendRow(['Country', 'Votes', 'VotedClients']);
  
  var countries = ['vietnam', 'china', 'cambodia', 'taiwan', 'indonesia', 
                   'philippines', 'thailand', 'malaysia', 'singapore', 'brunei'];
  countries.forEach(function(c) {
    sheet.appendRow([c, 0, '']);
  });
}