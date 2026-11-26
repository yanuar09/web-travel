from flask import Flask, render_template, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# Data master jadwal
SCHEDULES = [
    {
        "id": "JAD-01",
        "route": "Bandung (Pasteur) → Jakarta (Sudirman)",
        "origin": "Bandung (Pasteur)",
        "destination": "Jakarta (Sudirman)",
        "departure_time": "08:30 WIB",
        "arrival_time": "11:45 WIB",
        "duration": "3j 15m",
        "fleet_class": "HiAce Premio Eksekutif",
        "facilities": "AC, Reclining Seat, USB Port",
        "total_seats": 14,
        "available_seats": 6,
        "base_fare": 150000,
        "occupied_seats": ["1A", "2A", "2B", "3A", "3C", "4B", "5A", "5D"]
    },
    {
        "id": "JAD-02",
        "route": "Bandung (Pasteur) → Jakarta (Sudirman)",
        "origin": "Bandung (Pasteur)",
        "destination": "Jakarta (Sudirman)",
        "departure_time": "11:00 WIB",
        "arrival_time": "14:15 WIB",
        "duration": "3j 15m",
        "fleet_class": "HiAce Commuter",
        "facilities": "AC, Bagasi Kabin",
        "total_seats": 14,
        "available_seats": 2,
        "base_fare": 135000,
        "occupied_seats": ["1A", "2A", "2B", "2C", "3A", "3B", "3C", "4A", "4B", "5A", "5B", "5D"]
    },
    {
        "id": "JAD-03",
        "route": "Bandung (Pasteur) → Jakarta (Sudirman)",
        "origin": "Bandung (Pasteur)",
        "destination": "Jakarta (Sudirman)",
        "departure_time": "15:30 WIB",
        "arrival_time": "18:50 WIB",
        "duration": "3j 20m",
        "fleet_class": "HiAce Premio Eksekutif",
        "facilities": "AC, Reclining Seat, USB Port",
        "total_seats": 14,
        "available_seats": 11,
        "base_fare": 150000,
        "occupied_seats": ["1A", "2A", "3A"]
    }
]

# Kategori tiket dan persentase tarif
TICKET_CATEGORIES = {
    "dewasa": {"label": "Dewasa (Reguler)", "discount": 0.0, "factor": 1.0},
    "pelajar": {"label": "Pelajar (Diskon 15%)", "discount": 0.15, "factor": 0.85},
    "lansia": {"label": "Lansia (Diskon 20%)", "discount": 0.20, "factor": 0.80},
    "anak": {"label": "Anak-anak (Diskon 25%)", "discount": 0.25, "factor": 0.75}
}

SERVICE_FEE = 5000

@app.route('/')
def index():
    return render_template('index.html', 
                           schedules=SCHEDULES, 
                           categories=TICKET_CATEGORIES,
                           service_fee=SERVICE_FEE)

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    return jsonify({"status": "success", "data": SCHEDULES})

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json or {}
    schedule_id = data.get("schedule_id", "JAD-01")
    passengers = data.get("passengers", [])
    
    selected_sched = next((s for s in SCHEDULES if s["id"] == schedule_id), SCHEDULES[0])
    base_fare = selected_sched["base_fare"]
    
    breakdown = []
    subtotal = 0
    
    for p in passengers:
        cat_key = p.get("category", "dewasa").lower()
        cat_info = TICKET_CATEGORIES.get(cat_key, TICKET_CATEGORIES["dewasa"])
        fare = int(base_fare * cat_info["factor"])
        subtotal += fare
        breakdown.append({
            "seat": p.get("seat", "-"),
            "name": p.get("name", ""),
            "phone": p.get("phone", ""),
            "category": cat_key,
            "category_label": cat_info["label"],
            "fare": fare
        })
        
    total = subtotal + SERVICE_FEE if passengers else 0
    
    return jsonify({
        "status": "success",
        "base_fare": base_fare,
        "service_fee": SERVICE_FEE if passengers else 0,
        "subtotal": subtotal,
        "total": total,
        "passengers": breakdown
    })

@app.route('/api/book', methods=['POST'])
def book_ticket():
    data = request.json or {}
    booking_code = f"NS-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
    return jsonify({
        "status": "success",
        "booking_code": booking_code,
        "message": "Tiket berhasil diterbitkan!",
        "issued_at": datetime.now().strftime("%d %b %Y %H:%M:%S"),
        "cashier": "Loket Pasteur • Sifa A."
    })

if __name__ == '__main__':
    print("Menjalankan NusaShuttle Travel Web App di http://localhost:5000 ...")
    app.run(debug=True, port=5000)

