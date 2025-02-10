// Fungsi untuk login ke server
async function masukServer() {
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ /* data login Anda di sini */ })
        });
        const data = await response.json();
        catatStatus(`Kode Status Masuk: ${data.status}`);
        catatStatus(`Tanggapan Masuk: ${data.data}`);
        return response.ok ? response : null;
    } catch (error) {
        catatStatus(`Error Login: ${error.message}`);
        return null;
    }
}

// Fungsi untuk cek pembeli
async function cekPembeli(sesi, idPembeli) {
    try {
        const response = await fetch('/api/check-buyer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ buyerId: idPembeli })
        });
        const data = await response.json();
        const responseData = JSON.parse(data.data);
        if (responseData.ret === "S") {
            const msgDict = JSON.parse(responseData.msg);
            catatStatus(`Kode Status Kueri: ${data.status}`);
            catatStatus(`Respons Permintaan: nickName"${msgDict.nickName}"userId"${msgDict.userId}`);
        }
    } catch (error) {
        catatStatus(`Error Cek Pembeli: ${error.message}`);
    }
}

// Fungsi untuk jual kartu
async function jualKartu(sesi, idPembeli) {
    try {
        const response = await fetch('/api/sell-card', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ buyerId: idPembeli })
        });
        const data = await response.json();
        const responseData = JSON.parse(data.data);
        catatStatus(`Kode Status Kartu Jual: ${data.status}`);
        if (responseData.ret === "S") {
            catatStatus(`Respon Sukses:${responseData.msg}`);
            return true;
        }
        return false;
    } catch (error) {
        catatStatus(`Error Jual Kartu: ${error.message}`);
        return false;
    }
}

// Fungsi utama untuk memproses ID
async function mulaiProses() {
    const status = document.getElementById('status');
    const input = document.getElementById('input');
    const success = document.getElementById('success');
    const process = document.getElementById('process');

    status.textContent = "STATUS: Memulai proses...";
    
    const idPengguna = input.value.trim().split('\n').filter(id => id.trim());
    if (idPengguna.length === 0) {
        status.textContent = "STATUS: Error - Tidak ada ID";
        return;
    }
    
    const sesi = await masukServer();
    if (sesi) {
        for (let i = 0; i < idPengguna.length; i++) {
            const idPembeli = idPengguna[i];
            status.textContent = `STATUS: Memproses ID ${idPembeli}`;
            process.value = idPembeli;
            
            await cekPembeli(sesi, idPembeli);
            if (await jualKartu(sesi, idPembeli)) {
                // Pindahkan ID ke area sukses
                const currentSuccess = success.value.trim();
                success.value = currentSuccess ? `${currentSuccess}\n${idPembeli}` : idPembeli;
                
                // Hapus dari area proses
                process.value = '';
                
                // Hapus dari area input
                const remaining = idPengguna.filter(id => id !== idPembeli);
                input.value = remaining.join('\n');
            }
            
            status.textContent = `STATUS: SELESAI DI PROSES: ${i + 1} DARI TOTAL ID YANG DI PROSES: ${idPengguna.length}`;
        }
    }
}

// Fungsi untuk menampilkan tab
function tampilkanTab(namaTab) {
    const tabs = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-button');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    buttons.forEach(button => button.classList.remove('active'));
    
    document.getElementById(`${namaTab}-tab`).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Fungsi untuk menyalin teks
function salinTeks(idElemen) {
    const textarea = document.getElementById(idElemen);
    textarea.select();
    document.execCommand('copy');
}

// Fungsi untuk reset semua
function resetAll() {
    document.getElementById('input').value = '';
    document.getElementById('success').value = '';
    document.getElementById('process').value = '';
    document.getElementById('status').textContent = 'STATUS: READY';
    document.getElementById('log').value = '';
}

// Fungsi untuk membersihkan log
function bersihkanLog() {
    document.getElementById('log').value = '';
}

// Fungsi untuk mencatat status
function catatStatus(pesan) {
    const log = document.getElementById('log');
    log.value += pesan + '\n';
    log.scrollTop = log.scrollHeight;
} 