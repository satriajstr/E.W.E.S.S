# Ultrasonic Sensor Dashboard

Dashboard web untuk monitoring sensor ultrasonik HC-SR04 dengan Flask dan MySQL.

## Setup

1. Clone repository:
```bash
git clone https://github.com/dindinmhs/ultrasonik-dasborad.git
cd ultrasonik-dasborad
```

2. Install dependencies:
```bash
pip install flask mysql-connector-python
```

3. Setup database MySQL:
```sql
CREATE DATABASE sensor;

USE sensor;

CREATE TABLE ultrasonik (
    id INT AUTO_INCREMENT PRIMARY KEY,
    distance FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

4. Konfigurasi database di `app.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'sensor',
    'user': 'root',
    'password': ''
}
```

5. Jalankan aplikasi:
```bash
python app.py
```

6. Akses dashboard di browser:
```
http://localhost:5000
```

## API Endpoints

### GET `/`
Halaman dashboard utama

### POST `/api/realtime`
Menerima data real-time dari sensor
```json
{
  "distance": 15.5,
  "timestamp": "2025-11-26T08:19:15"
}
```

### GET `/api/realtime`
Mengambil data real-time terakhir

### POST `/api/store`
Menyimpan data ke database
```json
{
  "distance": 15.5
}
```

### GET `/api/statistics?period=24h`
Mengambil statistik dan grafik historis
- Parameter: `period` (1h, 24h, 7d)

## Teknologi

- Flask
- MySQL
- Tailwind CSS
- Chart.js

## Struktur Folder

```
ultrasonik/
├── app.py
├── templates/
│   └── dashboard.html
└── README.md
```