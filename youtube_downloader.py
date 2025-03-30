import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("520x650")
        self.root.resizable(False, False)
        
        self.qualities = {
            'mp4': {
                '4K': 'bestvideo[height<=2160]+bestaudio/best[ext=mp4]',
                '1440p': 'bestvideo[height<=1440]+bestaudio/best[ext=mp4]',
                '1080p': 'bestvideo[height<=1080]+bestaudio/best[ext=mp4]',
                '720p': 'bestvideo[height<=720]+bestaudio/best[ext=mp4]',
                '480p': 'bestvideo[height<=480]+bestaudio/best[ext=mp4]',
                'Melhor disponível': 'bestvideo+bestaudio/best[ext=mp4]'
            },
            'mkv': {
                '4K': 'bestvideo[height<=2160]+bestaudio/best',
                '1080p': 'bestvideo[height<=1080]+bestaudio/best',
                'Melhor qualidade': 'bestvideo+bestaudio/best'
            },
            'mp3': {
                '320kbps': 'ba[abr<=320]/bestaudio/best',
                '256kbps': 'ba[abr<=256]/bestaudio/best',
                '192kbps': 'ba[abr<=192]/bestaudio/best',
                '128kbps': 'ba[abr<=128]/bestaudio/best'
            }
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="YouTube Downloader", 
                 font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=3, pady=10)
        
        # Campo para o URL
        ttk.Label(main_frame, text="URL do vídeo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky=tk.W)
        
        # Seleção de tipo
        ttk.Label(main_frame, text="Tipo de mídia:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.media_type = tk.StringVar(value="mp4")
        ttk.Radiobutton(main_frame, text="MP4", variable=self.media_type, 
                       value="mp4", command=self.update_quality_options).grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(main_frame, text="MKV", variable=self.media_type, 
                       value="mkv", command=self.update_quality_options).grid(row=2, column=2, sticky=tk.W)
        ttk.Radiobutton(main_frame, text="MP3", variable=self.media_type, 
                       value="mp3", command=self.update_quality_options).grid(row=3, column=1, sticky=tk.W)
        
        # Seleção de qualidade
        ttk.Label(main_frame, text="Qualidade:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.quality_combo = ttk.Combobox(main_frame, state="readonly", width=15)
        self.quality_combo.grid(row=4, column=1, sticky=tk.W, padx=5)
        self.update_quality_options()
        
        # Seleção de pasta
        ttk.Label(main_frame, text="Pasta de destino:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.folder_path = tk.StringVar(value=os.path.join(os.path.expanduser('~'), 'Downloads'))
        ttk.Entry(main_frame, textvariable=self.folder_path, width=40, state='readonly').grid(
            row=5, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Button(main_frame, text="Selecionar", command=self.select_folder).grid(row=5, column=2, padx=5)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=450, mode='determinate')
        self.progress.grid(row=6, column=0, columnspan=3, pady=20)
        
        # Botão de download
        ttk.Button(main_frame, text="Baixar", command=self.start_download).grid(row=7, column=0, columnspan=3, pady=10)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=8, column=0, columnspan=3)
        
        # Console de logs
        self.log_text = tk.Text(main_frame, height=6, width=60, state='disabled')
        self.log_text.grid(row=9, column=0, columnspan=3, pady=10)
    
    def update_quality_options(self):
        media_type = self.media_type.get()
        self.quality_combo['values'] = list(self.qualities[media_type].keys())
        self.quality_combo.current(0)
    
    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
    
    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent_str = re.sub(r'\x1b\[[0-9;]*[mK]', '', d.get('_percent_str', '0%'))
            speed_str = re.sub(r'\x1b\[[0-9;]*[mK]', '', d.get('_speed_str', ''))
            
            try:
                percent = float(percent_str.strip().rstrip('%'))
                self.progress['value'] = percent
                self.status_var.set(f"Baixando... {percent:.1f}% @ {speed_str}")
                self.log_message(f"Progresso: {percent:.1f}% | Velocidade: {speed_str}")
            except ValueError:
                self.progress['value'] = 50
                self.status_var.set("Baixando...")
                
            self.root.update_idletasks()
            
        elif d['status'] == 'finished':
            self.status_var.set("✅ Download concluído!")
            self.progress['value'] = 100
            self.log_message("Download concluído com sucesso!")
    
    def start_download(self):
        url = self.url_entry.get().strip()
        media_type = self.media_type.get()
        quality = self.quality_combo.get()
        output_path = self.folder_path.get()
        
        if not url or not any(domain in url for domain in ['youtube.com', 'youtu.be']):
            messagebox.showerror("Erro", "Por favor, insira um URL válido do YouTube")
            return
        
        if not os.path.exists(output_path):
            messagebox.showerror("Erro", "Pasta de destino não existe")
            return
        
        try:
            self.progress['value'] = 0
            self.status_var.set("Iniciando download...")
            self.log_message(f"Iniciando download: {url}")
            self.log_message(f"Tipo: {media_type.upper()} | Qualidade: {quality}")
            self.root.update_idletasks()
            
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'noplaylist': True,
                'quiet': True,
                'no_color': True,
                'format_sort': ['res:2160', 'res:1440', 'res:1080', 'res:720', 'res:480'],
                'ignoreerrors': True,
                'retries': 10,
                'fragment_retries': 10,
                'skip_unavailable_fragments': True
            }
            
            if media_type in ['mp4', 'mkv']:
                ydl_opts['format'] = self.qualities[media_type][quality]
                ydl_opts['merge_output_format'] = media_type
            else:  # mp3
                ydl_opts['format'] = self.qualities[media_type][quality]
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality[:-4],  # Remove 'kbps'
                }]
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    self.log_message("Obtendo informações do vídeo...")
                    info = ydl.extract_info(url, download=False)
                    self.log_message(f"Título: {info.get('title', 'Desconhecido')}")
                    self.log_message(f"Duração: {self.format_duration(info.get('duration', 0))}")
                    self.log_message(f"Visualizações: {info.get('view_count', 'Desconhecido')}")
                    
                    self.log_message("Iniciando download...")
                    ydl.download([url])
                    
                    messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
                    self.status_var.set("Pronto")
                    self.progress['value'] = 0
                    
                except yt_dlp.utils.DownloadError as e:
                    if "Requested format is not available" in str(e):
                        messagebox.showwarning("Aviso", "Qualidade solicitada não disponível. Tentando qualidade alternativa...")
                        self.fallback_quality_download(url, media_type, output_path)
                    else:
                        raise
                        
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no download: {str(e)}")
            self.status_var.set("Erro durante o download")
            self.progress['value'] = 0
            self.log_message(f"ERRO: {str(e)}")
        finally:
            self.root.update_idletasks()
    
    def fallback_quality_download(self, url, media_type, output_path):
        """Tenta baixar com qualidades alternativas quando a selecionada não está disponível"""
        qualities = list(self.qualities[media_type].keys())
        current_quality = self.quality_combo.get()
        current_index = qualities.index(current_quality)
        
        for quality in qualities[current_index + 1:]:
            try:
                self.log_message(f"Tentando qualidade alternativa: {quality}")
                self.status_var.set(f"Tentando {quality}...")
                
                ydl_opts = {
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                    'format': self.qualities[media_type][quality],
                    'merge_output_format': media_type,
                    'quiet': True,
                    'no_color': True,
                    'ignoreerrors': True
                }
                
                if media_type == 'mp3':
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality[:-4],
                    }]
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                messagebox.showinfo("Sucesso", f"Download concluído em qualidade {quality}")
                self.status_var.set("Pronto")
                return
                
            except Exception as e:
                self.log_message(f"Falha na qualidade {quality}: {str(e)}")
                continue
        
        messagebox.showerror("Erro", "Não foi possível baixar em nenhuma qualidade disponível")
    
    def format_duration(self, seconds):
        """Formata a duração em segundos para HH:MM:SS"""
        if not seconds:
            return "Desconhecido"
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

if __name__ == '__main__':
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()