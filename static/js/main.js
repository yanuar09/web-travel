// Data Jadwal Master
const schedulesData = [
  {
    id: "JAD-01",
    route: "Bandung (Pasteur) → Jakarta (Sudirman)",
    departure_time: "08:30 WIB",
    arrival_time: "11:45 WIB",
    duration: "3j 15m",
    fleet_class: "HiAce Premio Eksekutif",
    facilities: "AC, Reclining Seat, USB Port",
    total_seats: 14,
    available_seats: 6,
    base_fare: 150000,
    occupied_seats: ["1A", "2A", "2B", "3A", "3C", "4B", "5A", "5D"]
  },
  {
    id: "JAD-02",
    route: "Bandung (Pasteur) → Jakarta (Sudirman)",
    departure_time: "11:00 WIB",
    arrival_time: "14:15 WIB",
    duration: "3j 15m",
    fleet_class: "HiAce Commuter",
    facilities: "AC, Bagasi Kabin",
    total_seats: 14,
    available_seats: 2,
    base_fare: 135000,
    occupied_seats: ["1A", "2A", "2B", "2C", "3A", "3B", "3C", "4A", "4B", "5A", "5B", "5D"]
  },
  {
    id: "JAD-03",
    route: "Bandung (Pasteur) → Jakarta (Sudirman)",
    departure_time: "15:30 WIB",
    arrival_time: "18:50 WIB",
    duration: "3j 20m",
    fleet_class: "HiAce Premio Eksekutif",
    facilities: "AC, Reclining Seat, USB Port",
    total_seats: 14,
    available_seats: 11,
    base_fare: 150000,
    occupied_seats: ["1A", "2A", "3A"]
  }
];

const categoryRates = {
  dewasa: { label: "Dewasa", desc: "Dewasa (Reguler)", factor: 1.0 },
  pelajar: { label: "Pelajar (-15%)", desc: "Pelajar (Diskon 15%)", factor: 0.85 },
  lansia: { label: "Lansia (-20%)", desc: "Lansia (Diskon 20%)", factor: 0.80 },
  anak: { label: "Anak (-25%)", desc: "Anak-anak (Diskon 25%)", factor: 0.75 }
};

const SERVICE_FEE = 5000;
const MAX_QUOTA = 4;

// App State
let currentStep = 1;
let selectedScheduleId = "JAD-01";
let selectedSeats = ["2C", "4A"];
let passengers = [
  { seat: "2C", name: "Raka Pratama", phone: "0812-8841-2091", category: "dewasa" },
  { seat: "4A", name: "Sinta Maharani", phone: "0856-9102-4418", category: "pelajar" }
];

// Format Rupiah
function formatRupiah(number) {
  return "Rp " + number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// Lifecycle Init
document.addEventListener("DOMContentLoaded", () => {
  renderScheduleList();
  renderSeatGrid();
  renderPassengerTable();
  updateCalculations();
  if (window.lucide) {
    lucide.createIcons();
  }
});

// Step Transition
function goToStep(step) {
  if (step === 2 && !selectedScheduleId) {
    alert("Pilih jadwal keberangkatan terlebih dahulu!");
    return;
  }
  if (step === 3 && selectedSeats.length === 0) {
    alert("Pilih minimal 1 kursi sebelum melanjutkan ke data penumpang!");
    return;
  }

  currentStep = step;

  // Toggle visible section
  document.getElementById("step-1").style.display = (step === 1) ? "grid" : "none";
  document.getElementById("step-2").style.display = (step === 2) ? "grid" : "none";
  document.getElementById("step-3").style.display = (step === 3) ? "grid" : "none";

  // Toggle active tab header
  [1, 2, 3].forEach(s => {
    const tab = document.getElementById(`tab-step-${s}`);
    if (tab) {
      if (s === step) {
        tab.classList.add("active");
      } else {
        tab.classList.remove("active");
      }
    }
  });

  // Re-sync components for current step
  if (step === 2) {
    renderSeatGrid();
    updateSeatSelectionUI();
  } else if (step === 3) {
    syncPassengersWithSeats();
    renderPassengerTable();
    updateCalculations();
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
  if (window.lucide) {
    lucide.createIcons();
  }
}

// ==========================================
// STEP 1 FUNCTIONS
// ==========================================
function renderScheduleList() {
  const container = document.getElementById("schedule-list-items");
  if (!container) return;

  const filterClass = document.getElementById("fleet-filter").value;
  const filtered = schedulesData.filter(item => {
    if (filterClass !== "ALL" && item.fleet_class !== filterClass) return false;
    return true;
  });

  document.getElementById("schedule-count-badge").innerText = `${filtered.length} Jadwal`;

  container.innerHTML = filtered.map(item => {
    const isSelected = item.id === selectedScheduleId;
    const isWarning = item.available_seats <= 2;
    const badgeClass = isWarning ? "seat-status-pill warning" : "seat-status-pill mint";
    const badgeText = `Sisa ${item.available_seats} / ${item.total_seats} kursi`;

    return `
      <div class="schedule-card ${isSelected ? 'active' : ''}" onclick="selectSchedule('${item.id}')">
        <div class="sched-left">
          <span class="code-pill">${item.id}</span>
          <div>
            <div class="time-row">
              <span>${item.departure_time}</span>
              <span>→</span>
              <span>${item.arrival_time}</span>
              <span class="duration-tag">(${item.duration})</span>
            </div>
            <div class="armada-desc">
              ${item.fleet_class} • ${item.facilities}
            </div>
          </div>
        </div>

        <div class="sched-right">
          <span class="${badgeClass}">${badgeText}</span>
          <div style="font-size: 0.72rem; color: var(--color-text-muted);">Tarif dasar</div>
          <div class="sched-price-val">${formatRupiah(item.base_fare)}</div>
        </div>
      </div>
    `;
  }).join("");

  updateSelectedScheduleSummary();
}

function selectSchedule(id) {
  selectedScheduleId = id;
  const sched = schedulesData.find(s => s.id === id);
  if (sched) {
    // If selected seats contains any occupied seat of newly selected schedule, filter out
    selectedSeats = selectedSeats.filter(seat => !sched.occupied_seats.includes(seat));
  }
  renderScheduleList();
}

function updateSelectedScheduleSummary() {
  const sched = schedulesData.find(s => s.id === selectedScheduleId);
  if (!sched) return;

  document.getElementById("summary-sched-id").innerText = sched.id;
  document.getElementById("summary-sched-route").innerText = sched.route;
  document.getElementById("summary-sched-time").innerText = `${sched.departure_time} → ${sched.arrival_time} • ${sched.fleet_class}`;
  document.getElementById("summary-sched-price").innerText = formatRupiah(sched.base_fare);
  
  // Update step 2 subtitle
  document.getElementById("seat-step-subtitle").innerText = 
    `${sched.id} • ${sched.route} • ${sched.departure_time}`;
  document.getElementById("available-seats-badge").innerText = 
    `Sisa ${sched.available_seats} dari ${sched.total_seats} Kursi`;
}

function onRouteFilterChange() {
  renderScheduleList();
}

// ==========================================
// STEP 2 FUNCTIONS: SEAT MAP
// ==========================================
function renderSeatGrid() {
  const container = document.getElementById("seat-grid-container");
  if (!container) return;

  const sched = schedulesData.find(s => s.id === selectedScheduleId);
  const occupied = sched ? sched.occupied_seats : [];

  // Shuttle HiAce Premio 14 Seat Layout:
  // Row 1: 1A, Empty, Driver
  // Row 2: 2A, 2B, Aisle, 2C
  // Row 3: 3A, 3B, Aisle, 3C
  // Row 4: 4A, 4B, Aisle, 4C
  // Row 5: 5A, 5B, 5C, 5D
  
  const layout = [
    {
      type: "row",
      seats: [
        { code: "1A", width: "1" },
        { code: "EMPTY", width: "1" },
        { code: "DRIVER", width: "1.8" }
      ]
    },
    {
      type: "row",
      seats: [
        { code: "2A", width: "1" },
        { code: "2B", width: "1" },
        { code: "AISLE", width: "0.6" },
        { code: "2C", width: "1" }
      ]
    },
    {
      type: "row",
      seats: [
        { code: "3A", width: "1" },
        { code: "3B", width: "1" },
        { code: "AISLE", width: "0.6" },
        { code: "3C", width: "1" }
      ]
    },
    {
      type: "row",
      seats: [
        { code: "4A", width: "1" },
        { code: "4B", width: "1" },
        { code: "AISLE", width: "0.6" },
        { code: "4C", width: "1" }
      ]
    },
    {
      type: "row",
      seats: [
        { code: "5A", width: "1" },
        { code: "5B", width: "1" },
        { code: "5C", width: "1" },
        { code: "5D", width: "1" }
      ]
    }
  ];

  container.innerHTML = layout.map(row => {
    const seatHtml = row.seats.map(item => {
      if (item.code === "EMPTY") {
        return `<div class="seat-empty-space" style="flex: ${item.width};"></div>`;
      }
      if (item.code === "AISLE") {
        return `<div class="seat-aisle" style="flex: ${item.width};">Lorong</div>`;
      }
      if (item.code === "DRIVER") {
        return `
          <div class="seat-btn driver" style="flex: ${item.width};">
            <i data-lucide="compass" size="16"></i>
            <span>Pengemudi</span>
          </div>
        `;
      }

      const isOccupied = occupied.includes(item.code);
      const isSelected = selectedSeats.includes(item.code);
      let stateClass = "";
      if (isOccupied) stateClass = "occupied";
      else if (isSelected) stateClass = "selected";

      return `
        <button 
          type="button" 
          class="seat-btn ${stateClass}" 
          style="flex: ${item.width};"
          ${isOccupied ? 'disabled' : ''}
          onclick="toggleSeat('${item.code}')">
          ${item.code}
        </button>
      `;
    }).join("");

    return `<div class="seat-row">${seatHtml}</div>`;
  }).join("");

  updateSeatSelectionUI();
  if (window.lucide) lucide.createIcons();
}

function toggleSeat(seatCode) {
  const sched = schedulesData.find(s => s.id === selectedScheduleId);
  if (sched && sched.occupied_seats.includes(seatCode)) return;

  const idx = selectedSeats.indexOf(seatCode);
  if (idx > -1) {
    selectedSeats.splice(idx, 1);
  } else {
    if (selectedSeats.length >= MAX_QUOTA) {
      alert(`Maksimal ${MAX_QUOTA} kursi per transaksi.`);
      return;
    }
    selectedSeats.push(seatCode);
  }

  // Sort seats nicely
  selectedSeats.sort();
  renderSeatGrid();
}

function resetSeats() {
  selectedSeats = [];
  renderSeatGrid();
}

function updateSeatSelectionUI() {
  const sched = schedulesData.find(s => s.id === selectedScheduleId);
  const baseFare = sched ? sched.base_fare : 150000;

  // Badge list
  const pillsContainer = document.getElementById("selected-seat-pills");
  if (pillsContainer) {
    if (selectedSeats.length === 0) {
      pillsContainer.innerHTML = `<span style="font-size: 0.8rem; color: var(--color-text-muted);">Belum ada kursi dipilih</span>`;
    } else {
      pillsContainer.innerHTML = selectedSeats.map(s => `
        <span class="seat-badge">${s}</span>
      `).join("");
    }
  }

  // Quota counter
  document.getElementById("quota-counter").innerText = `${selectedSeats.length} / ${MAX_QUOTA} Maks`;
  const remaining = MAX_QUOTA - selectedSeats.length;
  document.getElementById("quota-helper-text").innerText = 
    `Tersedia ${sched ? sched.available_seats : 6} kursi kosong pada armada ini. Anda masih dapat memilih ${remaining} kursi lagi.`;

  // Estimate
  const estimatedFare = selectedSeats.length * baseFare;
  document.getElementById("estimated-base-fare").innerText = formatRupiah(estimatedFare);
}

// ==========================================
// STEP 3 FUNCTIONS: PASSENGERS & FARES
// ==========================================
function syncPassengersWithSeats() {
  // Ensure every selected seat has a passenger record or empty slot
  const currentSeatMap = {};
  passengers.forEach(p => {
    currentSeatMap[p.seat] = p;
  });

  const updatedPassengers = [];
  selectedSeats.forEach(seat => {
    if (currentSeatMap[seat]) {
      updatedPassengers.push(currentSeatMap[seat]);
    } else {
      updatedPassengers.push({
        seat: seat,
        name: "",
        phone: "",
        category: "dewasa"
      });
    }
  });

  passengers = updatedPassengers;
}

function renderPassengerTable() {
  const tbody = document.getElementById("passenger-table-body");
  if (!tbody) return;

  const sched = schedulesData.find(s => s.id === selectedScheduleId);
  const baseFare = sched ? sched.base_fare : 150000;

  document.getElementById("passenger-step-subtitle").innerText = 
    `${selectedScheduleId} • Kursi terpilih: ${selectedSeats.join(", ")}`;
  document.getElementById("passenger-count-badge").innerText = 
    `${passengers.length} Penumpang`;

  tbody.innerHTML = passengers.map((p, index) => {
    const rateInfo = categoryRates[p.category] || categoryRates.dewasa;
    const fare = Math.round(baseFare * rateInfo.factor);

    return `
      <tr>
        <td class="seat-code-highlight">${p.seat}</td>
        <td>
          <div style="font-weight: 600;">${p.name || '<em>Belum diisi</em>'}</div>
          <div class="passenger-phone">${p.phone || '-'}</div>
        </td>
        <td>
          <select class="form-control" style="padding: 4px 8px; font-size: 0.82rem;" onchange="changePassengerCategory(${index}, this.value)">
            <option value="dewasa" ${p.category === 'dewasa' ? 'selected' : ''}>Dewasa</option>
            <option value="pelajar" ${p.category === 'pelajar' ? 'selected' : ''}>Pelajar (-15%)</option>
            <option value="lansia" ${p.category === 'lansia' ? 'selected' : ''}>Lansia (-20%)</option>
            <option value="anak" ${p.category === 'anak' ? 'selected' : ''}>Anak (-25%)</option>
          </select>
        </td>
        <td style="font-weight: 700; font-family: monospace;">
          ${formatRupiah(fare)}
        </td>
        <td style="text-align: right;">
          <button type="button" class="btn-delete-row" title="Hapus Kursi" onclick="removePassengerSeat('${p.seat}')">
            <i data-lucide="trash-2" size="16"></i>
          </button>
        </td>
      </tr>
    `;
  }).join("");

  if (window.lucide) lucide.createIcons();
}

function changePassengerCategory(index, newCategory) {
  if (passengers[index]) {
    passengers[index].category = newCategory;
    renderPassengerTable();
    updateCalculations();
  }
}

function removePassengerSeat(seatCode) {
  selectedSeats = selectedSeats.filter(s => s !== seatCode);
  passengers = passengers.filter(p => p.seat !== seatCode);
  renderPassengerTable();
  updateCalculations();
}

function addOrUpdatePassenger() {
  const nameInput = document.getElementById("input-p-name");
  const phoneInput = document.getElementById("input-p-phone");
  const catInput = document.getElementById("input-p-category");

  const name = nameInput.value.trim();
  const phone = phoneInput.value.trim();
  const category = catInput.value;

  if (!name) {
    alert("Harap masukkan nama lengkap penumpang!");
    return;
  }

  // Find first passenger with empty name
  const emptySlot = passengers.find(p => !p.name);
  if (emptySlot) {
    emptySlot.name = name;
    emptySlot.phone = phone;
    emptySlot.category = category;
  } else {
    // If all existing selected seats have names, notify
    alert("Semua kursi yang dipilih telah memiliki data penumpang. Tambahkan kursi di Denah jika ingin menambah penumpang.");
  }

  nameInput.value = "";
  phoneInput.value = "";
  renderPassengerTable();
  updateCalculations();
}

function updateCalculations() {
  const sched = schedulesData.find(s => s.id === selectedScheduleId);
  const baseFare = sched ? sched.base_fare : 150000;

  document.getElementById("calc-base-text").innerText = `Dasar: ${formatRupiah(baseFare)}`;

  // Tally counts per category
  const tally = {};
  passengers.forEach(p => {
    tally[p.category] = (tally[p.category] || 0) + 1;
  });

  const breakdownContainer = document.getElementById("calc-breakdown-list");
  let subtotal = 0;

  const breakdownHtml = Object.keys(tally).map(catKey => {
    const count = tally[catKey];
    const catInfo = categoryRates[catKey] || categoryRates.dewasa;
    const unitPrice = Math.round(baseFare * catInfo.factor);
    const lineTotal = unitPrice * count;
    subtotal += lineTotal;

    return `
      <div class="breakdown-row">
        <span>${count}x ${catInfo.desc}</span>
        <span class="val">${formatRupiah(lineTotal)}</span>
      </div>
    `;
  }).join("");

  breakdownContainer.innerHTML = breakdownHtml || `<div style="font-size:0.8rem; color:var(--color-text-muted);">Tidak ada penumpang</div>`;

  const total = subtotal > 0 ? (subtotal + SERVICE_FEE) : 0;
  document.getElementById("calc-service-fee").innerText = formatRupiah(SERVICE_FEE);
  document.getElementById("calc-total-pay").innerText = formatRupiah(total);
}

// ==========================================
// TICKET MODAL FUNCTIONS
// ==========================================
function openPrintModal() {
  if (passengers.length === 0) {
    alert("Silakan masukkan data penumpang terlebih dahulu!");
    return;
  }

  const sched = schedulesData.find(s => s.id === selectedScheduleId);
  const travelDate = document.getElementById("travel-date").value;
  
  // Format nice date
  const dateObj = new Date(travelDate);
  const formattedDate = isNaN(dateObj) ? "18 Nov 2026" : dateObj.toLocaleDateString("id-ID", { day: 'numeric', month: 'short', year: 'numeric' });

  // Generate random / authentic booking code
  const randomSuffix = Math.random().toString(36).substring(2, 6).toUpperCase();
  const bookingCode = `NS-20261118-${randomSuffix}`;

  document.getElementById("modal-booking-code").innerText = bookingCode;
  document.getElementById("modal-route").innerText = sched ? sched.route : "Bandung → Jakarta";
  document.getElementById("modal-schedule-time").innerText = `${formattedDate} • ${sched ? sched.departure_time : '08:30 WIB'}`;
  document.getElementById("modal-fleet").innerText = sched ? sched.fleet_class : "HiAce Premio Eksekutif";

  const totalStr = document.getElementById("calc-total-pay").innerText;
  document.getElementById("modal-total-pay").innerText = totalStr;

  // Passenger list inside modal
  const pListHtml = passengers.map(p => `
    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; padding: 4px 0; border-bottom: 1px dashed #eedecb;">
      <div>
        <strong>Kursi ${p.seat}</strong>: ${p.name || 'Penumpang'}
        <span style="font-size: 0.75rem; color: var(--color-text-muted);">(${categoryRates[p.category].label})</span>
      </div>
      <div style="font-family: monospace; font-weight: 700;">
        ${formatRupiah(Math.round((sched ? sched.base_fare : 150000) * categoryRates[p.category].factor))}
      </div>
    </div>
  `).join("");

  document.getElementById("modal-passenger-list").innerHTML = pListHtml;

  document.getElementById("ticket-modal").classList.add("active");
  if (window.lucide) lucide.createIcons();
}

function closeModal() {
  document.getElementById("ticket-modal").classList.remove("active");
}

