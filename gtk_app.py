import gi
import sqlite3
from datetime import datetime
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

//hhhmmm

class GtkApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Pemesanan Tiket Pesawat dan Kereta")
        self.set_border_width(10)
        self.set_default_size(480, 520)

        self.tiket_list = []

        vbox = Gtk.VBox(spacing=8)
        self.add(vbox)

        self.combo_jenis = Gtk.ComboBoxText()
        self.combo_jenis.append_text("Pesawat")
        self.combo_jenis.append_text("Kereta")
        self.combo_jenis.set_active(0)
        self.combo_jenis.connect("changed", self.on_jenis_changed)
        vbox.pack_start(Gtk.Label(label="Jenis Tiket:"), False, False, 0)
        vbox.pack_start(self.combo_jenis, False, False, 0)

        self.entry_nama = Gtk.Entry()
        vbox.pack_start(Gtk.Label(label="Nama Penumpang:"), False, False, 0)
        vbox.pack_start(self.entry_nama, False, False, 0)

        hbox_dari = Gtk.HBox(spacing=6)
        vbox.pack_start(Gtk.Label(label="Dari:"), False, False, 0)
        vbox.pack_start(hbox_dari, False, False, 0)

        self.combo_dari = Gtk.ComboBoxText()
        self.dari_list = ["Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Medan"]
        for lokasi in self.dari_list:
            self.combo_dari.append_text(lokasi)
        self.combo_dari.set_active(0)
        hbox_dari.pack_start(self.combo_dari, True, True, 0)

        btn_tambah_dari = Gtk.Button(label="+")
        btn_tambah_dari.set_tooltip_text("Tambah lokasi asal")
        btn_tambah_dari.set_size_request(30, 30)
        btn_tambah_dari.connect("clicked", self.on_tambah_dari_clicked)
        hbox_dari.pack_start(btn_tambah_dari, False, False, 0)

        hbox_tujuan = Gtk.HBox(spacing=6)
        vbox.pack_start(Gtk.Label(label="Tujuan:"), False, False, 0)
        vbox.pack_start(hbox_tujuan, False, False, 0)

        self.combo_tujuan = Gtk.ComboBoxText()
        self.tujuan_list = ["Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Medan"]
        for tujuan in self.tujuan_list:
            self.combo_tujuan.append_text(tujuan)
        self.combo_tujuan.set_active(0)
        hbox_tujuan.pack_start(self.combo_tujuan, True, True, 0)

        btn_tambah_tujuan = Gtk.Button(label="+")
        btn_tambah_tujuan.set_tooltip_text("Tambah tujuan baru")
        btn_tambah_tujuan.set_size_request(30, 30)
        btn_tambah_tujuan.connect("clicked", self.on_tambah_tujuan_clicked)
        hbox_tujuan.pack_start(btn_tambah_tujuan, False, False, 0)

        self.hbox_operator = Gtk.HBox(spacing=6)
        vbox.pack_start(Gtk.Label(label="Maskapai/Kereta:"), False, False, 0)
        vbox.pack_start(self.hbox_operator, False, False, 0)

        self.combo_maskapai = Gtk.ComboBoxText()
        self.maskapai_list = ["Garuda Indonesia", "Lion Air", "AirAsia", "Batik Air"]
        for m in self.maskapai_list:
            self.combo_maskapai.append_text(m)
        self.combo_maskapai.set_active(0)
        self.hbox_operator.pack_start(self.combo_maskapai, True, True, 0)

        self.combo_kereta = Gtk.ComboBoxText()
        self.kereta_list = ["Argo Bromo", "Taksaka", "Mutiara Selatan", "Gajayana"]
        for k in self.kereta_list:
            self.combo_kereta.append_text(k)
        self.combo_kereta.set_active(0)

        self.entry_tanggal = Gtk.Entry()
        self.entry_tanggal.set_placeholder_text("Format: YYYY-MM-DD")
        vbox.pack_start(Gtk.Label(label="Tanggal Keberangkatan:"), False, False, 0)
        vbox.pack_start(self.entry_tanggal, False, False, 0)

        self.entry_harga = Gtk.Entry()
        self.entry_harga.set_text("0")
        vbox.pack_start(Gtk.Label(label="Harga Tiket (Rp):"), False, False, 0)
        vbox.pack_start(self.entry_harga, False, False, 0)

        self.entry_jumlah = Gtk.Entry()
        self.entry_jumlah.set_text("1")
        vbox.pack_start(Gtk.Label(label="Jumlah Tiket:"), False, False, 0)
        vbox.pack_start(self.entry_jumlah, False, False, 0)

        self.btn_pesan = Gtk.Button(label="Pesan Tiket")
        self.btn_pesan.connect("clicked", self.on_pesan_clicked)
        vbox.pack_start(self.btn_pesan, False, False, 0)

        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textbuffer = self.textview.get_buffer()
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.add(self.textview)
        vbox.pack_start(scrolled, True, True, 0)

        self.on_jenis_changed(None)

    def on_jenis_changed(self, combo):
        for child in self.hbox_operator.get_children():
            self.hbox_operator.remove(child)

        jenis = self.combo_jenis.get_active_text()
        if jenis == "Pesawat":
            self.hbox_operator.pack_start(self.combo_maskapai, True, True, 0)
            self.combo_maskapai.show()
            self.combo_kereta.hide()
        else:
            self.hbox_operator.pack_start(self.combo_kereta, True, True, 0)
            self.combo_kereta.show()
            self.combo_maskapai.hide()

        self.hbox_operator.show_all()

    def on_tambah_dari_clicked(self, widget):
        self.tambah_lokasi_dialog("Tambah Lokasi Asal", self.combo_dari, self.dari_list)

    def on_tambah_tujuan_clicked(self, widget):
        self.tambah_lokasi_dialog("Tambah Tujuan Baru", self.combo_tujuan, self.tujuan_list)

    def tambah_lokasi_dialog(self, title, combo_box, daftar_lokasi):
        dialog = Gtk.Dialog(title, self, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.set_default_size(200, 100)

        box = dialog.get_content_area()
        label = Gtk.Label(label="Masukkan nama lokasi:")
        box.add(label)

        entry = Gtk.Entry()
        box.add(entry)
        entry.show()
        label.show()

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            lokasi_baru = entry.get_text().strip()
            if lokasi_baru == "":
                self.show_message("Nama lokasi tidak boleh kosong.")
            elif lokasi_baru in daftar_lokasi:
                self.show_message("Lokasi sudah ada di daftar.")
            else:
                daftar_lokasi.append(lokasi_baru)
                combo_box.append_text(lokasi_baru)
                combo_box.set_active(len(daftar_lokasi) - 1)
        dialog.destroy()

    def on_pesan_clicked(self, widget):
        jenis = self.combo_jenis.get_active_text()
        nama = self.entry_nama.get_text().strip()
        dari = self.combo_dari.get_active_text()
        tujuan = self.combo_tujuan.get_active_text()
        tanggal = self.entry_tanggal.get_text().strip()
        harga_text = self.entry_harga.get_text().strip()
        jumlah_text = self.entry_jumlah.get_text().strip()

        operator = self.combo_maskapai.get_active_text() if jenis == "Pesawat" else self.combo_kereta.get_active_text()

        if not nama or not dari or not tujuan or not tanggal or not operator:
            self.show_message("Semua field harus diisi.")
            return
        if dari == tujuan:
            self.show_message("Lokasi asal dan tujuan tidak boleh sama.")
            return
        if not self.validate_date(tanggal):
            self.show_message("Format tanggal salah! Gunakan YYYY-MM-DD.")
            return
        if not harga_text.isdigit() or int(harga_text) < 0:
            self.show_message("Harga harus angka positif.")
            return
        if not jumlah_text.isdigit() or int(jumlah_text) <= 0:
            self.show_message("Jumlah tiket harus angka lebih dari 0.")
            return

        harga = int(harga_text)
        jumlah = int(jumlah_text)

        for _ in range(jumlah):
            tiket = {
                "jenis": jenis,
                "nama": nama,
                "dari": dari,
                "tujuan": tujuan,
                "tanggal": tanggal,
                "harga": harga,
                "operator": operator
            }
            self.tiket_list.append(tiket)

        self.update_textview()
        self.clear_entries()

    def validate_date(self, date_str):
        import re
        from datetime import datetime
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(pattern, date_str):
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def update_textview(self):
        teks = "Daftar Tiket Dipesan:\n\n"
        total_harga = 0
        for i, t in enumerate(self.tiket_list, start=1):
            teks += (f"{i}. {t['jenis']} - Nama: {t['nama']}, Dari: {t['dari']}, Tujuan: {t['tujuan']}, "
                     f"Tanggal: {t['tanggal']}, Operator: {t['operator']}, Harga: Rp {t['harga']:,}\n")
            total_harga += t['harga']

        teks += f"\nTotal Harga: Rp {total_harga:,}"
        self.textbuffer.set_text(teks)

    def clear_entries(self):
        self.entry_nama.set_text("")
        self.combo_dari.set_active(0)
        self.combo_tujuan.set_active(0)
        self.entry_tanggal.set_text("")
        self.entry_harga.set_text("0")
        self.entry_jumlah.set_text("1")
        self.combo_jenis.set_active(0)
        self.combo_maskapai.set_active(0)

    def show_message(self, message):
        dialog = Gtk.MessageDialog(parent=self, flags=0,
                                   message_type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.OK,
                                   text=message)
        dialog.run()
        dialog.destroy()


if __name__ == "__main__":
    win = GtkApp()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
