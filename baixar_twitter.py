import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys

# Cores
COR_FUNDO = "#1a1a2e"
COR_SECUNDARIA = "#16213e"
COR_DESTAQUE = "#76b900"  # Verde NVIDIA
COR_TEXTO = "#ffffff"
COR_TEXTO_SEC = "#a0a0a0"
COR_ENTRADA = "#0f3460"
COR_BOTAO_HOVER = "#5a9e00"
COR_ERRO = "#e94560"
COR_SUCESSO = "#76b900"

class BaixadorX:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Baixador-X")
        self.janela.geometry("600x580")
        self.janela.configure(bg=COR_FUNDO)
        self.janela.resizable(False, False)
        
        # Centralizar janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (580 // 2)
        self.janela.geometry(f"600x580+{x}+{y}")
        
        self.pasta_destino = os.path.join(os.path.expanduser("~"), "Videos", "Videos X")
        
        # Criar pasta se não existir
        if not os.path.exists(self.pasta_destino):
            os.makedirs(self.pasta_destino, exist_ok=True)
        
        # Definir ícone da janela
        icon_path = os.path.join(os.path.dirname(__file__), "baixador_x.ico")
        if os.path.exists(icon_path):
            self.janela.iconbitmap(icon_path)
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        frame_principal = tk.Frame(self.janela, bg=COR_FUNDO)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=30, pady=(30, 0))
        
        # Logo/Título
        frame_titulo = tk.Frame(frame_principal, bg=COR_FUNDO)
        frame_titulo.pack(fill=tk.X, pady=(0, 20))
        
        # Ícone e título
        tk.Label(
            frame_titulo,
            text="⚡",
            font=("Segoe UI", 36),
            bg=COR_FUNDO,
            fg=COR_DESTAQUE
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        frame_texto_titulo = tk.Frame(frame_titulo, bg=COR_FUNDO)
        frame_texto_titulo.pack(side=tk.LEFT)
        
        tk.Label(
            frame_texto_titulo,
            text="BAIXADOR-X",
            font=("Segoe UI", 24, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).pack(anchor=tk.W)
        
        tk.Label(
            frame_texto_titulo,
            text="Downloader - Video Twitter/X",
            font=("Segoe UI", 10),
            bg=COR_FUNDO,
            fg=COR_TEXTO_SEC
        ).pack(anchor=tk.W)
        
        # Separador
        tk.Frame(frame_principal, bg=COR_DESTAQUE, height=2).pack(fill=tk.X, pady=(0, 20))
        
        # Campo do link
        frame_link = tk.Frame(frame_principal, bg=COR_FUNDO)
        frame_link.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            frame_link,
            text="LINK DO VÍDEO",
            font=("Segoe UI", 9, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO_SEC
        ).pack(anchor=tk.W, pady=(0, 5))
        
        frame_input = tk.Frame(frame_link, bg=COR_ENTRADA, highlightbackground=COR_DESTAQUE, highlightthickness=1)
        frame_input.pack(fill=tk.X)
        
        self.campo_link = tk.Entry(
            frame_input,
            font=("Segoe UI", 12),
            bg=COR_ENTRADA,
            fg=COR_TEXTO,
            insertbackground=COR_TEXTO,
            relief=tk.FLAT,
            bd=10
        )
        self.campo_link.pack(fill=tk.X)
        self.campo_link.insert(0, "Cole o link do Twitter/X aqui...")
        self.campo_link.bind("<FocusIn>", self.limpar_placeholder)
        self.campo_link.bind("<FocusOut>", self.restaurar_placeholder)
        
        # Campo pasta de destino
        frame_pasta = tk.Frame(frame_principal, bg=COR_FUNDO)
        frame_pasta.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            frame_pasta,
            text="SALVAR EM",
            font=("Segoe UI", 9, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO_SEC
        ).pack(anchor=tk.W, pady=(0, 5))
        
        frame_pasta_input = tk.Frame(frame_pasta, bg=COR_ENTRADA, highlightbackground=COR_DESTAQUE, highlightthickness=1)
        frame_pasta_input.pack(fill=tk.X)
        
        self.campo_pasta = tk.Entry(
            frame_pasta_input,
            font=("Segoe UI", 11),
            bg=COR_ENTRADA,
            fg=COR_TEXTO,
            insertbackground=COR_TEXTO,
            relief=tk.FLAT,
            bd=10,
            state="readonly"
        )
        self.campo_pasta.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Label para mostrar o caminho atual
        self.label_pasta = tk.Label(
            frame_pasta_input,
            text=self.pasta_destino,
            font=("Segoe UI", 9),
            bg=COR_ENTRADA,
            fg=COR_TEXTO_SEC,
            anchor=tk.W
        )
        self.label_pasta.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        botao_pasta = tk.Button(
            frame_pasta_input,
            text="📁 SELECIONAR",
            font=("Segoe UI", 9, "bold"),
            bg=COR_DESTAQUE,
            fg="#000000",
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.selecionar_pasta
        )
        botao_pasta.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Botão de download
        frame_botao = tk.Frame(frame_principal, bg=COR_FUNDO)
        frame_botao.pack(fill=tk.X, pady=(0, 15))
        
        self.botao_download = tk.Button(
            frame_botao,
            text="⬇  BAIXAR VÍDEO",
            font=("Segoe UI", 12, "bold"),
            bg=COR_DESTAQUE,
            fg="#000000",
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.iniciar_download
        )
        self.botao_download.pack(fill=tk.X)
        
        # Efeito hover no botão
        self.botao_download.bind("<Enter>", lambda e: self.botao_download.configure(bg=COR_BOTAO_HOVER))
        self.botao_download.bind("<Leave>", lambda e: self.botao_download.configure(bg=COR_DESTAQUE))
        
        # Status
        frame_status = tk.Frame(frame_principal, bg=COR_FUNDO)
        frame_status.pack(fill=tk.X, pady=(10, 0))
        
        self.label_status = tk.Label(
            frame_status,
            text="Pronto para baixar",
            font=("Segoe UI", 10),
            bg=COR_FUNDO,
            fg=COR_TEXTO_SEC
        )
        self.label_status.pack()
        
        # Barra de progresso
        self.barra_progresso = ttk.Progressbar(
            frame_status,
            mode='indeterminate',
            style='Custom.Horizontal.TProgressbar'
        )
        
        # Estilo da barra de progresso
        estilo = ttk.Style()
        estilo.theme_use('default')
        estilo.configure('Custom.Horizontal.TProgressbar',
                        background=COR_DESTAQUE,
                        troughcolor=COR_ENTRADA,
                        thickness=5)
        
        # Rodapé
        frame_rodape = tk.Frame(self.janela, bg=COR_SECUNDARIA)
        frame_rodape.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Label(
            frame_rodape,
            text="Formato: MP4 (compatível com WhatsApp)",
            font=("Segoe UI", 8),
            bg=COR_SECUNDARIA,
            fg=COR_TEXTO_SEC
        ).pack(pady=(10, 5))
        
        # Links do autor
        frame_links = tk.Frame(frame_rodape, bg=COR_SECUNDARIA)
        frame_links.pack(pady=(0, 10))
        
        tk.Label(
            frame_links,
            text="github.com/renatoapdl",
            font=("Segoe UI", 8),
            bg=COR_SECUNDARIA,
            fg=COR_DESTAQUE,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            frame_links,
            text="|",
            font=("Segoe UI", 8),
            bg=COR_SECUNDARIA,
            fg=COR_TEXTO_SEC
        ).pack(side=tk.LEFT)
        
        tk.Label(
            frame_links,
            text="linkedin.com/in/renatoabreuengenharia",
            font=("Segoe UI", 8),
            bg=COR_SECUNDARIA,
            fg=COR_DESTAQUE,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)
    
    def limpar_placeholder(self, event):
        if self.campo_link.get() == "Cole o link do Twitter/X aqui...":
            self.campo_link.delete(0, tk.END)
            self.campo_link.configure(fg=COR_TEXTO)
    
    def restaurar_placeholder(self, event):
        if not self.campo_link.get():
            self.campo_link.insert(0, "Cole o link do Twitter/X aqui...")
            self.campo_link.configure(fg=COR_TEXTO_SEC)
    
    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecionar pasta para salvar")
        if pasta:
            self.pasta_destino = pasta
            self.label_pasta.configure(text=pasta)
    
    def atualizar_status(self, mensagem, cor=COR_TEXTO_SEC):
        self.label_status.configure(text=mensagem, fg=cor)
        self.janela.update_idletasks()
    
    def iniciar_download(self):
        url = self.campo_link.get().strip()
        
        if not url or url == "Cole o link do Twitter/X aqui...":
            messagebox.showwarning("Aviso", "Por favor, insira o link do vídeo!")
            return
        
        if 'twitter.com' not in url and 'x.com' not in url:
            if not messagebox.askyesno("Aviso", "O link parece não ser do Twitter/X. Tentar mesmo assim?"):
                return
        
        # Desabilitar botão durante download
        self.botao_download.configure(state=tk.DISABLED, bg="#555555")
        self.barra_progresso.pack(fill=tk.X, pady=(10, 0))
        self.barra_progresso.start(10)
        
        # Rodar download em thread separada
        thread = threading.Thread(target=self.baixar_video, args=(url,))
        thread.daemon = True
        thread.start()
    
    def baixar_video(self, url):
        try:
            from yt_dlp import YoutubeDL
        except ImportError:
            self.atualizar_status("Instalando dependências...", COR_DESTAQUE)
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            from yt_dlp import YoutubeDL
        
        opcoes = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.pasta_destino, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            self.atualizar_status("Baixando vídeo...", COR_DESTAQUE)
            
            with YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = ydl.prepare_filename(info)
                nome_arquivo = os.path.basename(titulo)
            
            self.atualizar_status(f"✓ Concluído: {nome_arquivo}", COR_SUCESSO)
            messagebox.showinfo("Sucesso", f"Vídeo baixado com sucesso!\n\nSalvo em:\n{self.pasta_destino}")
            
        except Exception as e:
            self.atualizar_status(f"✗ Erro: {str(e)[:50]}...", COR_ERRO)
            messagebox.showerror("Erro", f"Falha ao baixar vídeo:\n{str(e)}")
        
        finally:
            self.barra_progresso.stop()
            self.barra_progresso.pack_forget()
            self.botao_download.configure(state=tk.NORMAL, bg=COR_DESTAQUE)
    
    def executar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = BaixadorX()
    app.executar()
