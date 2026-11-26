"""
NusaShuttle - Konsol Pemesanan Tiket & Kursi Travel
Desktop GUI Implementation using Python Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox

class NusaShuttleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NusaShuttle - Konsol Pemesanan Tiket & Kursi Travel")
        self.geometry("1100x720")
        self.configure(bg="#fcf8f3")

        # Palette colors
        self.c_bg = "#fcf8f3"
        self.c_card = "#fdf5ea"
        self.c_white = "#ffffff"
        self.c_primary = "#714e36"
        self.c_primary_hover = "#593c28"
        self.c_border = "#eedcc8"
        self.c_text = "#2b231d"
        self.c_muted = "#786b60"
        self.c_teal = "#21595b"
        self.c_mint = "#e2f4ed"
        self.c_mint_text = "#1b6853"
        self.c_occupied = "#e9decb"

        # State Data
        self.schedules = [
            {
                "id": "JAD-01",
                "route": "Bandung (Pasteur) → Jakarta (Sudirman)",
                "departure": "08:30 WIB",
                "arrival": "11:45 WIB",
                "duration": "3j 15m",
                "fleet": "HiAce Premio Eksekutif",
                "facilities": "AC, Reclining Seat, USB Port",
                "available": 6,
                "total": 14,
                "fare": 150000,
                "occupied": ["1A", "2A", "2B", "3A", "3C", "4B", "5A", "5D"]
            },
            {
                "id": "JAD-02",
                "route": "Bandung (Pasteur) → Jakarta (Sudirman)",
                "departure": "11:00 WIB",
                "arrival": "14:15 WIB",
                "duration": "3j 15m",
                "fleet": "HiAce Commuter",
                "facilities": "AC, Bagasi Kabin",
                "available": 2,
                "total": 14,
                "fare": 135000,
                "occupied": ["1A", "2A", "2B", "2C", "3A", "3B", "3C", "4A", "4B", "5A", "5B", "5D"]
            },
            {
                "id": "JAD-03",
                "route": "Bandung (Pasteur) → Jakarta (Sudirman)",
                "departure": "15:30 WIB",
                "arrival": "18:50 WIB",
                "duration": "3j 20m",
                "fleet": "HiAce Premio Eksekutif",
                "facilities": "AC, Reclining Seat, USB Port",
                "available": 11,
                "total": 14,
                "fare": 150000,
                "occupied": ["1A", "2A", "3A"]
            }
        ]

        self.selected_sched_id = "JAD-01"
        self.selected_seats = ["2C", "4A"]
        self.passengers = [
            {"seat": "2C", "name": "Raka Pratama", "phone": "0812-8841-2091", "category": "Dewasa (100%)"},
            {"seat": "4A", "name": "Sinta Maharani", "phone": "0856-9102-4418", "category": "Pelajar (-15%)"}
        ]

        self.current_step = 1

        self.setup_header()
        self.setup_main_area()
        self.show_step(1)

    def setup_header(self):
        header = tk.Frame(self, bg=self.c_white, height=65, relief="solid", bd=1)
        header.pack(fill="x", side="top")

        # Brand
        brand_frame = tk.Frame(header, bg=self.c_white)
        brand_frame.pack(side="left", padx=20, pady=10)

        icon_lbl = tk.Label(brand_frame, text="🚌", font=("Segoe UI Emoji", 16), bg=self.c_primary, fg="white", width=3, height=1)
        icon_lbl.pack(side="left", padx=(0, 10))

        title_box = tk.Frame(brand_frame, bg=self.c_white)
        title_box.pack(side="left")
        tk.Label(title_box, text="NusaShuttle", font=("Segoe UI", 12, "bold"), fg=self.c_text, bg=self.c_white).pack(anchor="w")
        tk.Label(title_box, text="Konsol Pemesanan Tiket & Kursi Travel", font=("Segoe UI", 8), fg=self.c_muted, bg=self.c_white).pack(anchor="w")

        # Stepper Buttons in Center
        stepper_frame = tk.Frame(header, bg="#f7efe4", padx=4, pady=4)
        stepper_frame.pack(side="left", expand=True)

        self.step_btn1 = tk.Button(stepper_frame, text="1. Rute & Jadwal", font=("Segoe UI", 9, "bold"),
                                   relief="flat", cursor="hand2", command=lambda: self.show_step(1))
        self.step_btn1.pack(side="left", padx=2)

        self.step_btn2 = tk.Button(stepper_frame, text="2. Pilih Kursi & Kuota", font=("Segoe UI", 9, "bold"),
                                   relief="flat", cursor="hand2", command=lambda: self.show_step(2))
        self.step_btn2.pack(side="left", padx=2)

        self.step_btn3 = tk.Button(stepper_frame, text="3. Penumpang & Tarif", font=("Segoe UI", 9, "bold"),
                                   relief="flat", cursor="hand2", command=lambda: self.show_step(3))
        self.step_btn3.pack(side="left", padx=2)

        # Right Info Badges
        right_info = tk.Frame(header, bg=self.c_white)
        right_info.pack(side="right", padx=20)

        date_lbl = tk.Label(right_info, text="📅 18 Nov 2026", font=("Segoe UI", 9, "bold"),
                            bg=self.c_white, fg=self.c_text, relief="solid", bd=1, padx=8, pady=4)
        date_lbl.pack(side="left", padx=4)

        cashier_lbl = tk.Label(right_info, text="💼 Loket Pasteur • Sifa A.", font=("Segoe UI", 9, "bold"),
                               bg=self.c_teal, fg="white", padx=10, pady=4)
        cashier_lbl.pack(side="left", padx=4)

    def setup_main_area(self):
        self.main_container = tk.Frame(self, bg=self.c_bg)
        self.main_container.pack(fill="both", expand=True, padx=25, pady=20)

        # Container for Steps
        self.frame_step1 = tk.Frame(self.main_container, bg=self.c_bg)
        self.frame_step2 = tk.Frame(self.main_container, bg=self.c_bg)
        self.frame_step3 = tk.Frame(self.main_container, bg=self.c_bg)

        self.build_step1_ui()
        self.build_step2_ui()
        self.build_step3_ui()

    def show_step(self, step):
        self.current_step = step
        self.frame_step1.pack_forget()
        self.frame_step2.pack_forget()
        self.frame_step3.pack_forget()

        # Update Stepper button styles
        for i, btn in enumerate([self.step_btn1, self.step_btn2, self.step_btn3], 1):
            if i == step:
                btn.configure(bg=self.c_primary, fg="white")
            else:
                btn.configure(bg="#f7efe4", fg=self.c_text)

        if step == 1:
            self.frame_step1.pack(fill="both", expand=True)
            self.refresh_step1_cards()
        elif step == 2:
            self.frame_step2.pack(fill="both", expand=True)
            self.refresh_seat_map()
        elif step == 3:
            self.frame_step3.pack(fill="both", expand=True)
            self.refresh_passengers_and_calculation()

    # ==================== STEP 1 UI ====================
    def build_step1_ui(self):
        # Left Panel (Route Navigation)
        left = tk.Frame(self.frame_step1, bg=self.c_card, relief="solid", bd=1, padx=18, pady=18)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.configure(width=340)
        left.pack_propagate(False)

        tk.Label(left, text="Navigasi Rute", font=("Segoe UI", 12, "bold"), bg=self.c_card, fg=self.c_text).pack(anchor="w")
        tk.Label(left, text="Pilih koridor asal, tujuan, dan tanggal", font=("Segoe UI", 8), bg=self.c_card, fg=self.c_muted).pack(anchor="w", pady=(0, 15))

        tk.Label(left, text="Koridor Keberangkatan", font=("Segoe UI", 8, "bold"), bg=self.c_card, fg=self.c_text).pack(anchor="w")
        self.cb_route = ttk.Combobox(left, values=["Bandung (Pasteur) → Jakarta (Sudirman)"], state="readonly")
        self.cb_route.current(0)
        self.cb_route.pack(fill="x", pady=(2, 10))

        tk.Label(left, text="Tanggal Keberangkatan", font=("Segoe UI", 8, "bold"), bg=self.c_card, fg=self.c_text).pack(anchor="w")
        e_date = tk.Entry(left, relief="solid", bd=1)
        e_date.insert(0, "11/18/2026")
        e_date.pack(fill="x", pady=(2, 10))

        tk.Label(left, text="Kelas Armada", font=("Segoe UI", 8, "bold"), bg=self.c_card, fg=self.c_text).pack(anchor="w")
        self.cb_fleet = ttk.Combobox(left, values=["Semua Armada", "HiAce Premio Eksekutif", "HiAce Commuter"], state="readonly")
        self.cb_fleet.current(0)
        self.cb_fleet.pack(fill="x", pady=(2, 15))

        # Selected summary box
        summary_box = tk.Frame(left, bg=self.c_white, relief="solid", bd=1, padx=14, pady=14)
        summary_box.pack(fill="x", pady=(10, 0))

        self.lbl_sum_id = tk.Label(summary_box, text="JAD-01", font=("Segoe UI", 8, "bold"), bg="#f7ede1", fg=self.c_primary)
        self.lbl_sum_id.pack(anchor="e")

        self.lbl_sum_route = tk.Label(summary_box, text="Bandung (Pasteur) → Jakarta (Sudirman)", font=("Segoe UI", 9, "bold"), bg=self.c_white)
        self.lbl_sum_route.pack(anchor="w", pady=(2, 2))

        self.lbl_sum_time = tk.Label(summary_box, text="08:30 WIB → 11:45 WIB • HiAce Premio Eksekutif", font=("Segoe UI", 8), bg=self.c_white, fg=self.c_muted)
        self.lbl_sum_time.pack(anchor="w")

        tk.Frame(summary_box, bg="#e8decb", height=1).pack(fill="x", pady=10)

        price_row = tk.Frame(summary_box, bg=self.c_white)
        price_row.pack(fill="x", pady=(0, 12))
        tk.Label(price_row, text="Tarif Dasar / Kursi", font=("Segoe UI", 8), bg=self.c_white, fg=self.c_muted).pack(side="left")
        self.lbl_sum_price = tk.Label(price_row, text="Rp 150.000", font=("Courier New", 12, "bold"), bg=self.c_white, fg=self.c_text)
        self.lbl_sum_price.pack(side="right")

        btn_go_seats = tk.Button(summary_box, text="Lanjut Pilih Kursi  ➔", font=("Segoe UI", 9, "bold"),
                                 bg=self.c_primary, fg="white", relief="flat", cursor="hand2", pady=8, command=lambda: self.show_step(2))
        btn_go_seats.pack(fill="x")

        # Right Panel (Schedules list)
        self.right_schedules = tk.Frame(self.frame_step1, bg=self.c_card, relief="solid", bd=1, padx=20, pady=20)
        self.right_schedules.pack(side="right", fill="both", expand=True)

        header_r = tk.Frame(self.right_schedules, bg=self.c_card)
        header_r.pack(fill="x", pady=(0, 15))
        tk.Label(header_r, text="Daftar Jadwal Keberangkatan", font=("Segoe UI", 12, "bold"), bg=self.c_card, fg=self.c_text).pack(side="left")
        tk.Label(header_r, text="3 Jadwal", font=("Segoe UI", 8, "bold"), bg=self.c_teal, fg="white", padx=8, pady=2).pack(side="right")

        self.sched_cards_container = tk.Frame(self.right_schedules, bg=self.c_card)
        self.sched_cards_container.pack(fill="both", expand=True)

    def refresh_step1_cards(self):
        for w in self.sched_cards_container.winfo_children():
            w.destroy()

        for s in self.schedules:
            is_active = (s["id"] == self.selected_sched_id)
            card = tk.Frame(self.sched_cards_container, bg=self.c_white, relief="solid",
                            bd=2 if is_active else 1, padx=16, pady=14, cursor="hand2")
            card.pack(fill="x", pady=6)
            card.bind("<Button-1>", lambda e, sid=s["id"]: self.select_schedule(sid))

            # Left side
            c_left = tk.Frame(card, bg=self.c_white)
            c_left.pack(side="left")
            c_left.bind("<Button-1>", lambda e, sid=s["id"]: self.select_schedule(sid))

            tag = tk.Label(c_left, text=s["id"], font=("Courier New", 8, "bold"), bg="#f7ede1", fg=self.c_primary, padx=6, pady=2)
            tag.pack(side="left", padx=(0, 12))

            info_f = tk.Frame(c_left, bg=self.c_white)
            info_f.pack(side="left")
            t_lbl = tk.Label(info_f, text=f"{s['departure']}  ➔  {s['arrival']}  ({s['duration']})", font=("Segoe UI", 10, "bold"), bg=self.c_white)
            t_lbl.pack(anchor="w")
            d_lbl = tk.Label(info_f, text=f"{s['fleet']} • {s['facilities']}", font=("Segoe UI", 8), fg=self.c_muted, bg=self.c_white)
            d_lbl.pack(anchor="w")

            # Right side
            c_right = tk.Frame(card, bg=self.c_white)
            c_right.pack(side="right")
            c_right.bind("<Button-1>", lambda e, sid=s["id"]: self.select_schedule(sid))

            badge_bg = self.c_mint if s["available"] > 2 else "#fdf0e0"
            badge_fg = self.c_mint_text if s["available"] > 2 else "#b66814"
            rem_lbl = tk.Label(c_right, text=f"Sisa {s['available']} / {s['total']} kursi", font=("Segoe UI", 8, "bold"),
                               bg=badge_bg, fg=badge_fg, padx=8, pady=2)
            rem_lbl.pack(anchor="e")

            p_lbl = tk.Label(c_right, text=f"Rp {s['fare']:,}".replace(",", "."), font=("Courier New", 11, "bold"), bg=self.c_white)
            p_lbl.pack(anchor="e", pady=(4, 0))

    def select_schedule(self, sched_id):
        self.selected_sched_id = sched_id
        sched = next(s for s in self.schedules if s["id"] == sched_id)
        self.lbl_sum_id.config(text=sched["id"])
        self.lbl_sum_route.config(text=sched["route"])
        self.lbl_sum_time.config(text=f"{sched['departure']} → {sched['arrival']} • {sched['fleet']}")
        self.lbl_sum_price.config(text=f"Rp {sched['fare']:,}".replace(",", "."))
        self.refresh_step1_cards()

    # ==================== STEP 2 UI ====================
    def build_step2_ui(self):
        # Left Panel (Chassis & Seat Map)
        left = tk.Frame(self.frame_step2, bg=self.c_card, relief="solid", bd=1, padx=20, pady=20)
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))

        header_l = tk.Frame(left, bg=self.c_card)
        header_l.pack(fill="x", pady=(0, 10))
        tk.Label(header_l, text="Denah Kursi Armada Shuttle", font=("Segoe UI", 12, "bold"), bg=self.c_card).pack(side="left")
        self.lbl_s2_badge = tk.Label(header_l, text="Sisa 6 dari 14 Kursi", font=("Segoe UI", 8, "bold"), bg=self.c_mint, fg=self.c_mint_text, padx=8, pady=2)
        self.lbl_s2_badge.pack(side="right")

        # Legend Bar
        leg_bar = tk.Frame(left, bg=self.c_white, relief="solid", bd=1, padx=12, pady=6)
        leg_bar.pack(fill="x", pady=(0, 15))

        for text, color, bd in [("Tersedia", self.c_white, 1), ("Dipilih", self.c_primary, 0), ("Terisi", self.c_occupied, 1)]:
            box = tk.Label(leg_bar, text="  ", bg=color, relief="solid", bd=bd)
            box.pack(side="left", padx=(10, 4))
            tk.Label(leg_bar, text=text, font=("Segoe UI", 8), bg=self.c_white).pack(side="left", padx=(0, 15))

        # Bus Chassis Frame
        self.chassis = tk.Frame(left, bg=self.c_white, relief="solid", bd=1, padx=30, pady=25)
        self.chassis.pack(expand=True)

        # Right Panel (Quota Validation)
        right = tk.Frame(self.frame_step2, bg=self.c_card, relief="solid", bd=1, padx=20, pady=20)
        right.pack(side="right", fill="y")
        right.configure(width=340)
        right.pack_propagate(False)

        tk.Label(right, text="Validasi Kuota Kursi", font=("Segoe UI", 12, "bold"), bg=self.c_card).pack(anchor="w", pady=(0, 15))

        # Quota box
        q_box = tk.Frame(right, bg=self.c_white, relief="solid", bd=1, padx=12, pady=12)
        q_box.pack(fill="x", pady=(0, 12))

        q_head = tk.Frame(q_box, bg=self.c_white)
        q_head.pack(fill="x")
        tk.Label(q_head, text="Kuota Transaksi Aman", font=("Segoe UI", 8, "bold"), bg=self.c_white).pack(side="left")
        self.lbl_quota_count = tk.Label(q_head, text="2 / 4 Maks", font=("Courier New", 9, "bold"), bg=self.c_white)
        self.lbl_quota_count.pack(side="right")

        self.lbl_quota_info = tk.Label(q_box, text="Tersedia 6 kursi kosong pada armada ini. Anda masih dapat memilih 2 kursi lagi.",
                                       font=("Segoe UI", 8), fg=self.c_muted, bg=self.c_white, wraplength=280, justify="left")
        self.lbl_quota_info.pack(anchor="w", pady=(6, 0))

        # Selected Seats Box
        s_box = tk.Frame(right, bg=self.c_white, relief="solid", bd=1, padx=12, pady=12)
        s_box.pack(fill="x", pady=(0, 12))

        s_head = tk.Frame(s_box, bg=self.c_white)
        s_head.pack(fill="x")
        tk.Label(s_head, text="Kursi Dipilih", font=("Segoe UI", 8, "bold"), bg=self.c_white).pack(side="left")
        btn_reset = tk.Button(s_head, text="Reset Kursi", font=("Segoe UI", 8, "underline"), bg=self.c_white, fg=self.c_primary,
                              relief="flat", cursor="hand2", command=self.reset_seats)
        btn_reset.pack(side="right")

        self.seats_pill_frame = tk.Frame(s_box, bg=self.c_white)
        self.seats_pill_frame.pack(fill="x", pady=(8, 0))

        # Estimated Base Fare
        est_box = tk.Frame(right, bg=self.c_white, relief="solid", bd=1, padx=12, pady=12)
        est_box.pack(fill="x", pady=(0, 18))
        tk.Label(est_box, text="Estimasi Tarif Dasar", font=("Segoe UI", 8), bg=self.c_white, fg=self.c_muted).pack(anchor="w")
        self.lbl_est_fare = tk.Label(est_box, text="Rp 300.000", font=("Courier New", 13, "bold"), bg=self.c_white, fg=self.c_text)
        self.lbl_est_fare.pack(anchor="e")

        # Buttons
        btn_duo = tk.Frame(right, bg=self.c_card)
        btn_duo.pack(fill="x", side="bottom")

        tk.Button(btn_duo, text="⬅ Jadwal", font=("Segoe UI", 9, "bold"), bg=self.c_white, relief="solid", bd=1,
                  cursor="hand2", padx=10, pady=8, command=lambda: self.show_step(1)).pack(side="left", fill="x", expand=True, padx=(0, 4))
        tk.Button(btn_duo, text="Data Penumpang ➔", font=("Segoe UI", 9, "bold"), bg=self.c_primary, fg="white", relief="flat",
                  cursor="hand2", padx=10, pady=8, command=lambda: self.show_step(3)).pack(side="right", fill="x", expand=True, padx=(4, 0))

    def refresh_seat_map(self):
        for w in self.chassis.winfo_children():
            w.destroy()

        sched = next(s for s in self.schedules if s["id"] == self.selected_sched_id)
        occupied = sched["occupied"]

        rows = [
            [("1A", 1), ("", 1), ("Pengemudi", 2)],
            [("2A", 1), ("2B", 1), ("Lorong", 1), ("2C", 1)],
            [("3A", 1), ("3B", 1), ("Lorong", 1), ("3C", 1)],
            [("4A", 1), ("4B", 1), ("Lorong", 1), ("4C", 1)],
            [("5A", 1), ("5B", 1), ("5C", 1), ("5D", 1)],
        ]

        for r_idx, r in enumerate(rows):
            rf = tk.Frame(self.chassis, bg=self.c_white)
            rf.pack(pady=4)

            for code, span in r:
                if code == "":
                    tk.Label(rf, text="", width=6, bg=self.c_white).pack(side="left", padx=4)
                elif code == "Lorong":
                    tk.Label(rf, text="Lorong", width=6, font=("Segoe UI", 7, "italic"), fg=self.c_muted, bg=self.c_white).pack(side="left", padx=4)
                elif code == "Pengemudi":
                    tk.Label(rf, text="🧑‍✈️ Pengemudi", width=14, font=("Segoe UI", 8, "bold"), bg="#f7ece1", relief="solid", bd=1, pady=8).pack(side="left", padx=4)
                else:
                    is_occ = code in occupied
                    is_sel = code in self.selected_seats

                    bg = self.c_occupied if is_occ else (self.c_primary if is_sel else self.c_white)
                    fg = self.c_muted if is_occ else ("white" if is_sel else self.c_text)

                    b = tk.Button(rf, text=code, width=6, font=("Segoe UI", 9, "bold"), bg=bg, fg=fg,
                                  relief="solid", bd=1, pady=6, cursor="hand2" if not is_occ else "arrow",
                                  command=lambda c=code: self.toggle_seat(c) if not is_occ else None)
                    b.pack(side="left", padx=4)

        # Update right box labels
        for w in self.seats_pill_frame.winfo_children():
            w.destroy()

        for s in self.selected_seats:
            lbl = tk.Label(self.seats_pill_frame, text=s, font=("Segoe UI", 8, "bold"), bg=self.c_primary, fg="white", padx=8, pady=3)
            lbl.pack(side="left", padx=3)

        self.lbl_quota_count.config(text=f"{len(self.selected_seats)} / 4 Maks")
        rem = 4 - len(self.selected_seats)
        self.lbl_quota_info.config(text=f"Tersedia {sched['available']} kursi kosong pada armada ini. Anda masih dapat memilih {rem} kursi lagi.")

        est_fare = len(self.selected_seats) * sched["fare"]
        self.lbl_est_fare.config(text=f"Rp {est_fare:,}".replace(",", "."))

    def toggle_seat(self, code):
        if code in self.selected_seats:
            self.selected_seats.remove(code)
            self.passengers = [p for p in self.passengers if p["seat"] != code]
        else:
            if len(self.selected_seats) >= 4:
                messagebox.showwarning("Batas Kuota", "Maksimal pemesanan adalah 4 kursi per transaksi!")
                return
            self.selected_seats.append(code)
            self.selected_seats.sort()
            self.passengers.append({"seat": code, "name": "", "phone": "", "category": "Dewasa (100%)"})

        self.refresh_seat_map()

    def reset_seats(self):
        self.selected_seats = []
        self.passengers = []
        self.refresh_seat_map()

    # ==================== STEP 3 UI ====================
    def build_step3_ui(self):
        # Left Panel (Passenger List & Inputs)
        left = tk.Frame(self.frame_step3, bg=self.c_card, relief="solid", bd=1, padx=20, pady=20)
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))

        header_l = tk.Frame(left, bg=self.c_card)
        header_l.pack(fill="x", pady=(0, 10))
        tk.Label(header_l, text="Daftar Penumpang", font=("Segoe UI", 12, "bold"), bg=self.c_card).pack(side="left")
        self.lbl_s3_badge = tk.Label(header_l, text="2 Penumpang", font=("Segoe UI", 8, "bold"), bg=self.c_teal, fg="white", padx=8, pady=2)
        self.lbl_s3_badge.pack(side="right")

        # Input box
        in_box = tk.Frame(left, bg=self.c_white, relief="solid", bd=1, padx=12, pady=12)
        in_box.pack(fill="x", pady=(0, 15))

        tk.Label(in_box, text="Nama Lengkap", font=("Segoe UI", 8, "bold"), bg=self.c_white).grid(row=0, column=0, sticky="w", padx=4)
        self.e_pname = tk.Entry(in_box, relief="solid", bd=1, width=18)
        self.e_pname.grid(row=1, column=0, padx=4, pady=4)

        tk.Label(in_box, text="No. HP / WA", font=("Segoe UI", 8, "bold"), bg=self.c_white).grid(row=0, column=1, sticky="w", padx=4)
        self.e_pphone = tk.Entry(in_box, relief="solid", bd=1, width=15)
        self.e_pphone.grid(row=1, column=1, padx=4, pady=4)

        tk.Label(in_box, text="Kategori Tiket", font=("Segoe UI", 8, "bold"), bg=self.c_white).grid(row=0, column=2, sticky="w", padx=4)
        self.cb_pcat = ttk.Combobox(in_box, values=["Dewasa (100%)", "Pelajar (-15%)", "Lansia (-20%)"], state="readonly", width=14)
        self.cb_pcat.current(0)
        self.cb_pcat.grid(row=1, column=2, padx=4, pady=4)

        btn_add = tk.Button(in_box, text="Tambah", font=("Segoe UI", 8, "bold"), bg=self.c_primary, fg="white",
                            relief="flat", cursor="hand2", padx=10, command=self.add_passenger)
        btn_add.grid(row=1, column=3, padx=4, pady=4)

        # Passenger Table Frame
        self.table_frame = tk.Frame(left, bg=self.c_white, relief="solid", bd=1)
        self.table_frame.pack(fill="both", expand=True)

        # Right Panel (Calculation)
        right = tk.Frame(self.frame_step3, bg=self.c_card, relief="solid", bd=1, padx=20, pady=20)
        right.pack(side="right", fill="y")
        right.configure(width=340)
        right.pack_propagate(False)

        header_r = tk.Frame(right, bg=self.c_card)
        header_r.pack(fill="x", pady=(0, 15))
        tk.Label(header_r, text="Kalkulasi Tarif Kategori", font=("Segoe UI", 11, "bold"), bg=self.c_card).pack(side="left")
        self.lbl_calc_base = tk.Label(header_r, text="Dasar: Rp 150.000", font=("Courier New", 8), bg=self.c_card, fg=self.c_muted)
        self.lbl_calc_base.pack(side="right")

        # Breakdown List Frame
        self.breakdown_frame = tk.Frame(right, bg=self.c_white, relief="solid", bd=1, padx=12, pady=12)
        self.breakdown_frame.pack(fill="x", pady=(0, 15))

        # Summary box
        calc_box = tk.Frame(right, bg=self.c_white, relief="solid", bd=1, padx=12, pady=12)
        calc_box.pack(fill="x", pady=(0, 20))

        srv_row = tk.Frame(calc_box, bg=self.c_white)
        srv_row.pack(fill="x")
        tk.Label(srv_row, text="Biaya Layanan Loket", font=("Segoe UI", 8), bg=self.c_white, fg=self.c_muted).pack(side="left")
        tk.Label(srv_row, text="Rp 5.000", font=("Courier New", 8, "bold"), bg=self.c_white).pack(side="right")

        tk.Frame(calc_box, bg="#e8decb", height=1).pack(fill="x", pady=10)

        tot_row = tk.Frame(calc_box, bg=self.c_white)
        tot_row.pack(fill="x")
        tk.Label(tot_row, text="Total Pembayaran", font=("Segoe UI", 9, "bold"), bg=self.c_white).pack(side="left")
        self.lbl_tot_pay = tk.Label(tot_row, text="Rp 282.500", font=("Courier New", 14, "bold"), bg=self.c_white, fg=self.c_text)
        self.lbl_tot_pay.pack(side="right")

        # Buttons
        btn_duo = tk.Frame(right, bg=self.c_card)
        btn_duo.pack(fill="x", side="bottom")

        tk.Button(btn_duo, text="⬅ Pilih Kursi", font=("Segoe UI", 9, "bold"), bg=self.c_white, relief="solid", bd=1,
                  cursor="hand2", padx=10, pady=8, command=lambda: self.show_step(2)).pack(side="left", fill="x", expand=True, padx=(0, 4))
        tk.Button(btn_duo, text="🎟 Cetak Tiket", font=("Segoe UI", 9, "bold"), bg=self.c_primary, fg="white", relief="flat",
                  cursor="hand2", padx=10, pady=8, command=self.print_ticket).pack(side="right", fill="x", expand=True, padx=(4, 0))

    def refresh_passengers_and_calculation(self):
        for w in self.table_frame.winfo_children():
            w.destroy()

        sched = next(s for s in self.schedules if s["id"] == self.selected_sched_id)
        base_fare = sched["fare"]
        self.lbl_calc_base.config(text=f"Dasar: Rp {base_fare:,}".replace(",", "."))
        self.lbl_s3_badge.config(text=f"{len(self.passengers)} Penumpang")

        # Headers
        th = tk.Frame(self.table_frame, bg="#fbf4ea", relief="solid", bd=1)
        th.pack(fill="x")
        tk.Label(th, text="Kursi", font=("Segoe UI", 8, "bold"), width=8, bg="#fbf4ea").pack(side="left", padx=4, pady=6)
        tk.Label(th, text="Nama & Kontak", font=("Segoe UI", 8, "bold"), width=24, bg="#fbf4ea", anchor="w").pack(side="left", padx=4)
        tk.Label(th, text="Kategori Tiket", font=("Segoe UI", 8, "bold"), width=16, bg="#fbf4ea", anchor="w").pack(side="left", padx=4)
        tk.Label(th, text="Tarif", font=("Segoe UI", 8, "bold"), width=12, bg="#fbf4ea", anchor="e").pack(side="left", padx=4)

        subtotal = 0
        cat_counts = {}

        for idx, p in enumerate(self.passengers):
            rf = tk.Frame(self.table_frame, bg=self.c_white)
            rf.pack(fill="x", pady=2)

            tk.Label(rf, text=p["seat"], font=("Courier New", 9, "bold"), width=8, bg=self.c_white).pack(side="left", padx=4)

            name_box = tk.Frame(rf, bg=self.c_white, width=170)
            name_box.pack(side="left", padx=4)
            tk.Label(name_box, text=p["name"] or "(Belum diisi)", font=("Segoe UI", 8, "bold"), bg=self.c_white).pack(anchor="w")
            tk.Label(name_box, text=p["phone"] or "-", font=("Segoe UI", 7), fg=self.c_muted, bg=self.c_white).pack(anchor="w")

            factor = 0.85 if "Pelajar" in p["category"] else (0.80 if "Lansia" in p["category"] else 1.0)
            fare = int(base_fare * factor)
            subtotal += fare

            cat_name = "Dewasa (Reguler)" if factor == 1.0 else ("Pelajar (Diskon 15%)" if factor == 0.85 else "Lansia (Diskon 20%)")
            cat_counts[cat_name] = cat_counts.get(cat_name, 0) + 1

            tk.Label(rf, text=p["category"], font=("Segoe UI", 8), width=16, bg=self.c_white, anchor="w").pack(side="left", padx=4)
            tk.Label(rf, text=f"Rp {fare:,}".replace(",", "."), font=("Courier New", 9, "bold"), width=12, bg=self.c_white, anchor="e").pack(side="left", padx=4)

        # Refresh Breakdown
        for w in self.breakdown_frame.winfo_children():
            w.destroy()

        for cat_name, count in cat_counts.items():
            row = tk.Frame(self.breakdown_frame, bg=self.c_white)
            row.pack(fill="x", pady=2)
            unit = base_fare if "Dewasa" in cat_name else int(base_fare * 0.85)
            tk.Label(row, text=f"{count}x {cat_name}", font=("Segoe UI", 8), bg=self.c_white).pack(side="left")
            tk.Label(row, text=f"Rp {unit * count:,}".replace(",", "."), font=("Courier New", 8, "bold"), bg=self.c_white).pack(side="right")

        total = subtotal + 5000 if self.passengers else 0
        self.lbl_tot_pay.config(text=f"Rp {total:,}".replace(",", "."))

    def add_passenger(self):
        name = self.e_pname.get().strip()
        phone = self.e_pphone.get().strip()
        cat = self.cb_pcat.get()

        if not name:
            messagebox.showwarning("Validasi", "Masukkan nama penumpang!")
            return

        # Find first empty passenger
        empty = next((p for p in self.passengers if not p["name"]), None)
        if empty:
            empty["name"] = name
            empty["phone"] = phone
            empty["category"] = cat
        else:
            messagebox.showinfo("Informasi", "Semua kursi telah terisi nama penumpang.")

        self.e_pname.delete(0, tk.END)
        self.e_pphone.delete(0, tk.END)
        self.refresh_passengers_and_calculation()

    def print_ticket(self):
        if not self.passengers:
            messagebox.showwarning("Peringatan", "Belum ada tiket untuk dicetak.")
            return

        sched = next(s for s in self.schedules if s["id"] == self.selected_sched_id)
        msg = f"=== TIKET RESMI NUSASHUTTLE ===\n"
        msg += f"Kode Booking: NS-20261118-8A92\n"
        msg += f"Rute: {sched['route']}\n"
        msg += f"Jam: {sched['departure']} - {sched['arrival']}\n"
        msg += f"Armada: {sched['fleet']}\n\n"
        msg += "Daftar Penumpang:\n"
        for p in self.passengers:
            msg += f"- Kursi {p['seat']}: {p['name']} ({p['category']})\n"
        msg += f"\nTotal Pembayaran: {self.lbl_tot_pay.cget('text')}\n"
        msg += "Status: LUNAS\n"
        msg += "Kasir: Loket Pasteur • Sifa A."

        messagebox.showinfo("Tiket Berhasil Dicetak", msg)


if __name__ == "__main__":
    app = NusaShuttleApp()
    app.mainloop()

