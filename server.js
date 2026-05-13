const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

let votes = {
    vietnam: 0, china: 0, cambodia: 0, taiwan: 0, indonesia: 0,
    philippines: 0, thailand: 0, malaysia: 0, singapore: 0, brunei: 0
};
let votedClients = {}; // { country: [clientId1, clientId2, ...] }
const countries = Object.keys(votes);

// GET - Trả về kết quả
app.get('/votes', (req, res) => {
    res.json(votes);
});

// POST - Bình chọn
app.post('/vote', (req, res) => {
    const { country, clientId } = req.body;
    if (!country || !countries.includes(country)) {
        return res.json({ success: false, message: 'Quốc gia không hợp lệ' });
    }
    if (!votedClients[country]) votedClients[country] = [];
    if (votedClients[country].includes(clientId)) {
        return res.json({ success: false, message: 'Bạn đã bình chọn rồi' });
    }
    votedClients[country].push(clientId);
    votes[country]++;
    res.json({ success: true });
});

// POST - Reset
app.post('/reset', (req, res) => {
    countries.forEach(c => { votes[c] = 0; });
    votedClients = {};
    res.json({ success: true });
});

// ===== CHẠY SERVER =====
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log('Vote server running on port ' + PORT);
});