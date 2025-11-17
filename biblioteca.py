import customtkinter as ctk
from tkinter import messagebox



# Livros no sistema: [ID, Título, Autor, Gênero, Editora, Status, Cliente_Aluguel]
livros_db = [
    [1, "O Nome do Vento", "Patrick Rothfuss", "Fantasia", "Arqueiro", "Disponível", None],
    [2, "1984", "George Orwell", "Distopia", "Companhia das Letras", "Alugado", "cliente1"],
    [3, "Pequeno Príncipe", "Antoine de Saint-Exupéry", "Infantil", "Agir", "Disponível", None],
    [4, "A Metamorfose", "Franz Kafka", "Ficção", "Penguin", "Disponível", None],
    [5, "Dom Casmurro", "Machado de Assis", "Romance", "Ateliê", "Alugado", "outro_cliente"]
]

# Credenciais de Login: {usuario: senha, tipo}
usuarios_db = {
    "cliente1": {"senha": "123", "tipo": "cliente"},
    "admin": {"senha": "456", "tipo": "administrador"}
}pip install customtkinter



def buscar_livros(termo, filtro):

    if not termo:
        return livros_db
    
    termo = termo.lower()
    resultados = []
    
    # Índices na lista de livros: 1=Título, 2=Autor, 3=Gênero, 4=Editora
    indice_filtro = {"titulo": 1, "autor": 2, "gênero": 3, "editora": 4}.get(filtro)

    if indice_filtro is not None:
        for livro in livros_db:
            if str(livro[indice_filtro]).lower().find(termo) != -1:
                resultados.append(livro)
    
    return resultados

def adicionar_livro(titulo, autor, genero, editora):
    
    novo_id = max(livro[0] for livro in livros_db) + 1 if livros_db else 1
    livros_db.append([novo_id, titulo, autor, genero, editora, "Disponível", None])
    return True



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
      
        self.title("Biblioteca")
        self.geometry("800x600")
        ctk.set_appearance_mode("System")  # Light/Dark
        ctk.set_default_color_theme("blue")
        
        self.usuario_logado = None
        self.tipo_usuario = None
        
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
       
        self.exibir_login()

    def limpar_tela(self):
    
        for widget in self.winfo_children():
            widget.destroy()

   
    
    def exibir_login(self):
        self.limpar_tela()
        
        frame_login = ctk.CTkFrame(self)
        frame_login.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Para centralizar os elementos no frame de login
        frame_login.columnconfigure(0, weight=1)
        frame_login.columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_login, text="LOGIN", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(20, 30))
        
        
        ctk.CTkLabel(frame_login, text="Usuário:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_usuario = ctk.CTkEntry(frame_login, width=200)
        self.entry_usuario.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        
        ctk.CTkLabel(frame_login, text="Senha:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_senha = ctk.CTkEntry(frame_login, show="*", width=200)
        self.entry_senha.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
       
        ctk.CTkButton(frame_login, text="Entrar", command=self.processar_login).grid(row=3, column=0, columnspan=2, pady=30, padx=20)

    def exibir_cliente(self):
        self.limpar_tela()
        self.title("Biblioteca - Cliente")
        
    
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Linha da tabela
        
      
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        frame_topo.columnconfigure(0, weight=1)
        ctk.CTkLabel(frame_topo, text=f"Bem-vindo(a), {self.usuario_logado}!", font=ctk.CTkFont(size=18)).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(frame_topo, text="Sair", command=self.logout, width=80).grid(row=0, column=1, sticky="e")

        # Seção de Filtro
        frame_filtro = ctk.CTkFrame(self)
        frame_filtro.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.filtro_var = ctk.StringVar(value="titulo")
        
        ctk.CTkLabel(frame_filtro, text="Buscar Livros:").pack(side="left", padx=(10, 5), pady=10)
        self.entry_busca = ctk.CTkEntry(frame_filtro, width=250)
        self.entry_busca.pack(side="left", padx=5, pady=10)
        
        ctk.CTkLabel(frame_filtro, text="Por:").pack(side="left", padx=(10, 5), pady=10)
        ctk.CTkOptionMenu(frame_filtro, variable=self.filtro_var, values=["titulo", "autor", "gênero", "editora"]).pack(side="left", padx=5, pady=10)
        
        ctk.CTkButton(frame_filtro, text="Pesquisar", command=self.atualizar_tabela).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(frame_filtro, text="Mostrar Todos", command=lambda: self.atualizar_tabela(limpar_busca=True)).pack(side="left", padx=10, pady=10)

   
        self.tabela_livros = ctk.CTkScrollableFrame(self)
        self.tabela_livros.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.tabela_livros.columnconfigure(0, weight=1) # Coluna para o conteúdo
        
   
        self.atualizar_tabela()

    def exibir_administrador(self):
        self.exibir_cliente() # O Administrador tem todas as funcionalidades do Cliente
        self.title("Biblioteca - Administrador")

        
        frame_admin = ctk.CTkFrame(self)
        frame_admin.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
     
        ctk.CTkLabel(frame_admin, text="Funcionalidades do Administrador", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=8, pady=(10, 5))

      
        ctk.CTkLabel(frame_admin, text="Título:").grid(row=1, column=0, padx=5, pady=5)
        self.admin_titulo = ctk.CTkEntry(frame_admin, width=120)
        self.admin_titulo.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(frame_admin, text="Autor:").grid(row=1, column=2, padx=5, pady=5)
        self.admin_autor = ctk.CTkEntry(frame_admin, width=120)
        self.admin_autor.grid(row=1, column=3, padx=5, pady=5)
        
        ctk.CTkLabel(frame_admin, text="Gênero:").grid(row=1, column=4, padx=5, pady=5)
        self.admin_genero = ctk.CTkEntry(frame_admin, width=120)
        self.admin_genero.grid(row=1, column=5, padx=5, pady=5)

        ctk.CTkLabel(frame_admin, text="Editora:").grid(row=1, column=6, padx=5, pady=5)
        self.admin_editora = ctk.CTkEntry(frame_admin, width=120)
        self.admin_editora.grid(row=1, column=7, padx=5, pady=5)
        
        ctk.CTkButton(frame_admin, text="Adicionar Livro", command=self.processar_adicionar_livro).grid(row=2, column=0, columnspan=8, pady=10)
        
        # Reconfigura a grade principal para o frame de Admin
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(2, weight=1) # Mantém a tabela

   
    
    def processar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if usuario in usuarios_db and usuarios_db[usuario]["senha"] == senha:
            self.usuario_logado = usuario
            self.tipo_usuario = usuarios_db[usuario]["tipo"]
            
            if self.tipo_usuario == "cliente":
                self.exibir_cliente()
            elif self.tipo_usuario == "administrador":
                self.exibir_administrador()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")

    def logout(self):
        self.usuario_logado = None
        self.tipo_usuario = None
        self.exibir_login()
        
    def atualizar_tabela(self, limpar_busca=False):
        """Atualiza a tabela de livros com base na pesquisa."""
        
        # Limpar widgets existentes na tabela
        for widget in self.tabela_livros.winfo_children():
            widget.destroy()

        if limpar_busca:
            self.entry_busca.delete(0, 'end')
        
        termo = self.entry_busca.get()
        filtro = self.filtro_var.get()
        
        # Realiza a busca
        livros_para_exibir = buscar_livros(termo, filtro)

        # Cabeçalhos da Tabela
        headers = ["ID", "Título", "Autor", "Gênero", "Editora", "Status"]
        if self.tipo_usuario == "administrador":
            headers.append("Cliente Aluguel")

        for col, header in enumerate(headers):
            ctk.CTkLabel(self.tabela_livros, text=header, font=ctk.CTkFont(weight="bold")).grid(row=0, column=col, padx=5, pady=5, sticky="w")

        # Conteúdo da Tabela
        for row_idx, livro in enumerate(livros_para_exibir):
            # A linha do livro contém: [ID, Título, Autor, Gênero, Editora, Status, Cliente_Aluguel]
            for col_idx, dado in enumerate(livro[:-1]): # Exibe as 6 primeiras colunas (sem Cliente_Aluguel)
                ctk.CTkLabel(self.tabela_livros, text=str(dado)).grid(row=row_idx + 1, column=col_idx, padx=5, pady=2, sticky="w")

            # Adiciona a coluna "Cliente Aluguel" apenas para o Administrador
            if self.tipo_usuario == "administrador":
                cliente_aluguel = livro[6] if livro[6] else "-"
                ctk.CTkLabel(self.tabela_livros, text=str(cliente_aluguel)).grid(row=row_idx + 1, column=len(headers) - 1, padx=5, pady=2, sticky="w")
                
    def processar_adicionar_livro(self):
        """Coleta dados e adiciona um novo livro."""
        titulo = self.admin_titulo.get()
        autor = self.admin_autor.get()
        genero = self.admin_genero.get()
        editora = self.admin_editora.get()
        
        if titulo and autor and genero and editora:
            adicionar_livro(titulo, autor, genero, editora)
            messagebox.showinfo("Sucesso", f"Livro '{titulo}' adicionado com sucesso!")
            # Limpa os campos
            self.admin_titulo.delete(0, 'end')
            self.admin_autor.delete(0, 'end')
            self.admin_genero.delete(0, 'end')
            self.admin_editora.delete(0, 'end')
            # Atualiza a tabela
            self.atualizar_tabela(limpar_busca=True)
        else:
            messagebox.showerror("Erro", "Todos os campos de livro devem ser preenchidos.")



if __name__ == "__main__":
    app = App()
    app.mainloop()