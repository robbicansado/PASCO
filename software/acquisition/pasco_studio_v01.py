"""PASCO Studio V0.1 — aquisição óptica e METEO V10.
Dependências: pip install pyserial matplotlib
Executar: python pasco_studio_v01.py
"""
import csv
import re
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from collections import deque
from datetime import datetime
from statistics import median

import serial
from serial.tools import list_ports
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

OPT_RE = re.compile(r'A1\s*=\s*(\d+)\s*;\s*A2\s*=\s*(\d+)')
TEMP_RE = re.compile(r'Meteo\s*->\s*T\(C\)\s*:\s*(-?\d+(?:[.,]\d+)?)', re.I)

class PascoStudio:
    def __init__(self, root):
        self.root = root
        root.title('PASCO Studio V0.1 | Aquisição Experimental')
        root.geometry('1080x760')
        self.ser = None
        self.started = None
        self.paused = False
        self.records = []
        self.points = deque(maxlen=250)
        self.filter_values = deque(maxlen=5)
        self.temp_first = None
        self.mode = tk.StringVar(value='Óptica (A1 / A2)')
        self.port = tk.StringVar(value='')
        self.status = tk.StringVar(value='Desconectado')
        self.latest = tk.StringVar(value='Aguardando dados...')
        self.delta = tk.StringVar(value='Δ: —')
        self._make_ui()
        self.refresh_ports()
        root.after(100, self.poll)
        root.protocol('WM_DELETE_WINDOW', self.close)

    def _make_ui(self):
        top = ttk.Frame(self.root, padding=12)
        top.pack(fill='x')
        ttk.Label(top, text='PASCO Studio', font=('Segoe UI', 20, 'bold')).pack(side='left', padx=(0, 20))
        ttk.Label(top, text='Módulo:').pack(side='left')
        modes = ttk.Combobox(top, textvariable=self.mode, values=['Óptica (A1 / A2)', 'Temperatura (METEO V10)'], state='readonly', width=25)
        modes.pack(side='left', padx=6)
        modes.bind('<<ComboboxSelected>>', lambda _: self.change_mode())
        ttk.Label(top, text='Porta:').pack(side='left', padx=(10, 0))
        self.port_combo = ttk.Combobox(top, textvariable=self.port, width=12, state='readonly')
        self.port_combo.pack(side='left', padx=6)
        ttk.Button(top, text='Atualizar', command=self.refresh_ports).pack(side='left')
        self.connect_btn = ttk.Button(top, text='Conectar', command=self.toggle_connection)
        self.connect_btn.pack(side='left', padx=8)

        controls = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        controls.pack(fill='x')
        self.pause_btn = ttk.Button(controls, text='Pausar', command=self.toggle_pause)
        self.pause_btn.pack(side='left', padx=(0, 6))
        ttk.Button(controls, text='Zerar aquisição', command=self.reset).pack(side='left', padx=6)
        ttk.Button(controls, text='Exportar CSV', command=self.export_csv).pack(side='left', padx=6)
        ttk.Button(controls, text='Exportar gráfico PNG', command=self.export_png).pack(side='left', padx=6)
        ttk.Button(controls, text='Exportar tabela', command=self.export_table).pack(side='left', padx=6)
        ttk.Label(controls, textvariable=self.status).pack(side='right')

        indicators = ttk.Frame(self.root, padding=(12, 2, 12, 8))
        indicators.pack(fill='x')
        ttk.Label(indicators, textvariable=self.latest, font=('Segoe UI', 15, 'bold')).pack(side='left')
        ttk.Label(indicators, textvariable=self.delta, font=('Segoe UI', 12)).pack(side='right')

        self.fig = Figure(figsize=(10, 4.4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=12)
        self.table = ttk.Treeview(self.root, height=8, show='headings')
        self.table.pack(fill='both', padx=12, pady=(8, 12))
        self.change_mode()

    def refresh_ports(self):
        ports = [p.device for p in list_ports.comports()]
        self.port_combo['values'] = ports
        if self.port.get() not in ports:
            self.port.set(ports[0] if ports else '')

    def toggle_connection(self):
        if self.ser:
            self.disconnect()
            return
        if not self.port.get():
            messagebox.showwarning('Porta serial', 'Selecione uma porta COM e clique em Conectar.')
            return
        try:
            self.ser = serial.Serial(self.port.get(), 9600, timeout=0)
            self.ser.reset_input_buffer()
            self.status.set('Conectado: ' + self.port.get())
            self.connect_btn.config(text='Desconectar')
        except serial.SerialException as exc:
            messagebox.showerror('Falha na conexão', f'{exc}\n\nFeche o Monitor Serial do Arduino IDE.')

    def disconnect(self):
        if self.ser:
            self.ser.close()
            self.ser = None
        self.status.set('Desconectado')
        self.connect_btn.config(text='Conectar')

    def change_mode(self):
        self.reset()
        if self.mode.get().startswith('Óptica'):
            self.columns = ('tempo_s', 'A1_ADC', 'A2_ADC', 'delta_A2_ADC')
            self.ax.set_ylabel('Leitura ADC (0–1023)')
            self.ax.set_ylim(0, 1023)
        else:
            self.columns = ('tempo_s', 'temperatura_bruta_C', 'temperatura_filtrada_C', 'delta_T_C')
            self.ax.set_ylabel('Temperatura (°C)')
        self.table['columns'] = self.columns
        for col in self.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=160, anchor='center')
        self.draw()

    def reset(self):
        self.records.clear()
        self.points.clear()
        self.filter_values.clear()
        self.started = None
        self.temp_first = None
        self.opt_first = None
        self.latest.set('Aguardando dados...')
        self.delta.set('Δ: —')
        for item in self.table.get_children():
            self.table.delete(item)
        self.draw()

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.config(text='Retomar' if self.paused else 'Pausar')
        self.status.set('Aquisição pausada' if self.paused else ('Conectado' if self.ser else 'Desconectado'))
        if self.ser and not self.paused:
            self.ser.reset_input_buffer()

    def poll(self):
        try:
            if self.ser and not self.paused:
                processed = 0
                while self.ser.in_waiting and processed < 60:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    processed += 1
                    self.consume(line)
                if processed:
                    self.draw()
        except (serial.SerialException, OSError) as exc:
            self.disconnect()
            self.status.set(f'Conexão perdida: {exc}')
        self.root.after(100, self.poll)

    def consume(self, line):
        if self.mode.get().startswith('Óptica'):
            match = OPT_RE.search(line)
            if not match:
                return
            a1, a2 = map(int, match.groups())
            if self.started is None:
                self.started = time.monotonic()
                self.opt_first = a2
            t = time.monotonic() - self.started
            delta = a2 - self.opt_first
            row = (round(t, 3), a1, a2, delta)
            self.points.append((t, a1, a2))
            self.latest.set(f'A1: {a1} ADC    |    A2: {a2} ADC')
            self.delta.set(f'ΔA2: {delta:+d} ADC')
        else:
            match = TEMP_RE.search(line)
            if not match:
                return
            raw = float(match.group(1).replace(',', '.'))
            self.filter_values.append(raw)
            filtered = median(self.filter_values)
            if self.started is None:
                self.started = time.monotonic()
                self.temp_first = filtered
            t = time.monotonic() - self.started
            delta = filtered - self.temp_first
            row = (round(t, 3), round(raw, 3), round(filtered, 3), round(delta, 3))
            self.points.append((t, raw, filtered))
            self.latest.set(f'Temperatura: {filtered:.2f} °C')
            self.delta.set(f'ΔT: {delta:+.2f} °C')
        self.records.append(row)
        self.table.insert('', 'end', values=row)
        children = self.table.get_children()
        if len(children) > 200:
            self.table.delete(children[0])
        self.table.yview_moveto(1)

    def draw(self):
        self.ax.clear()
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('Tempo (s)')
        if self.mode.get().startswith('Óptica'):
            self.ax.set_title('Aquisição óptica — A1 e A2')
            self.ax.set_ylabel('Leitura ADC (0–1023)')
            self.ax.set_ylim(0, 1023)
            if self.points:
                t, a1, a2 = zip(*self.points)
                self.ax.plot(t, a1, label='A1 · placa vermelha')
                self.ax.plot(t, a2, label='A2 · placa azul')
                self.ax.legend(loc='best')
        else:
            self.ax.set_title('METEO — Temperatura em tempo real')
            self.ax.set_ylabel('Temperatura (°C)')
            if self.points:
                t, raw, filt = zip(*self.points)
                self.ax.plot(t, raw, label='Bruta', alpha=0.35)
                self.ax.plot(t, filt, label='Mediana (5)', linewidth=2)
                self.ax.legend(loc='best')
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def _save_path(self, ext, label):
        name = f'pasco_{"optica" if self.mode.get().startswith("Óptica") else "meteo"}_{datetime.now():%Y%m%d_%H%M%S}.{ext}'
        return filedialog.asksaveasfilename(defaultextension='.' + ext, initialfile=name, filetypes=[(label, '*.' + ext)])

    def _write_csv(self, path):
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(self.columns)
            writer.writerows(self.records)

    def export_csv(self):
        if not self.records:
            messagebox.showinfo('Sem dados', 'Faça uma aquisição antes de exportar.')
            return
        path = self._save_path('csv', 'Planilha CSV')
        if path:
            self._write_csv(path)
            self.status.set('CSV salvo: ' + path)

    def export_table(self):
        if not self.records:
            messagebox.showinfo('Sem dados', 'Faça uma aquisição antes de exportar.')
            return
        path = self._save_path('csv', 'Tabela CSV')
        if path:
            self._write_csv(path)
            self.status.set('Tabela salva: ' + path)

    def export_png(self):
        if not self.records:
            messagebox.showinfo('Sem dados', 'Faça uma aquisição antes de exportar.')
            return
        path = self._save_path('png', 'Imagem PNG')
        if path:
            self.fig.savefig(path, dpi=180, bbox_inches='tight')
            self.status.set('Gráfico salvo: ' + path)

    def close(self):
        self.disconnect()
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    PascoStudio(root)
    root.mainloop()