from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate
import webbrowser
import sqlite3
import requests

root = Tk()


class validadores():
    def validate_entry2(self, text):
        if text == '':
            return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100


class relatorios():
    def printcliente(self):
        webbrowser.open("cliente.pdf")


    def gerar_relatorio_cliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigorel = self.et_codigo.get()
        self.nomerel = self.et_nome.get()
        self.telefonerel = self.et_telefone.get()
        self.cidaderel = self.et_cidade.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, f'Código:')
        self.c.drawString(50, 670, f'Nome:')
        self.c.drawString(50, 630, f'Telefone:')
        self.c.drawString(50, 600, f'Cidade:')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(150, 700, self.codigorel)
        self.c.drawString(150, 670, self.nomerel)
        self.c.drawString(150, 630, self.telefonerel)
        self.c.drawString(150, 600, self.cidaderel)

        self.c.rect(25, 425, 550, 400, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printcliente()


class funcs():
    def limpar_tela(self, tudo=True):
        if tudo == True:
            self.et_codigo.delete(0, END)
            self.et_nome.delete(0, END)
            self.et_telefone.delete(0, END)
            self.et_cidade.delete(0, END)
            self.et_bairro.delete(0, END)
            self.et_endereco.delete(0, END)


        else:
            self.et_codigo.delete(0, END)


    def conectar_db(self):
        self.banco = sqlite3.connect('clientes.db')
        self.cursor = self.banco.cursor()


    def desconnect(self):
        self.banco.close()


    def monta_tabela(self):
        
        self.conectar_db(), print("Conectando banco de dados")
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS clientes (cod INTEGER PRIMARY KEY, nome_cliente CHAR(40) NOT NULL, telefone INTEGER(20), cidade CHAR(40));")

        self.banco.commit()
        self.desconnect()


    def variaveis(self):
        self.codigo = self.et_codigo.get().replace(' ', '')
        self.nome = self.et_nome.get()
        self.telefone = self.et_telefone.get()
        self.cidade = self.et_cidade.get()
        self.cep = self.et_cep.get()
        self.endereco = self.et_endereco.get()
        self.bairro = self.et_bairro.get()


    def add_clientes(self):
        self.variaveis()
        if self.nome == '':
            msg = 'Para cadastrar um novo cliente é necessário\ndigitar um nome'
            messagebox.showinfo('Cadastro de clientes - ERROR', msg)
        else:

            self.conectar_db()

            self.cursor.execute(f"INSERT INTO clientes (nome_cliente, telefone, cidade) VALUES (?, ?, ?)", (self.nome, self.telefone, self.cidade))

            self.banco.commit()

            self.desconnect()
            self.select_lista()
            self.limpar_tela()


    def select_lista(self):
        self.tabela_clientes.delete(*self.tabela_clientes.get_children())
        self.conectar_db()

        lista = self.cursor.execute("SELECT cod, nome_cliente, telefone, cidade FROM clientes ORDER BY nome_cliente ASC;")

        for i in lista:
            self.tabela_clientes.insert("", END, values=i)
        self.desconnect()

    
    def buscar_cliente(self):
        self.conectar_db()
        
        self.et_nome.insert(END, '%')
        nome = self.et_nome.get()
        self.tabela_clientes.delete(*self.tabela_clientes.get_children())
        
        self.cursor.execute("SELECT cod, nome_cliente, telefone, cidade FROM clientes WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC" % nome)
        buscando_nome_cliente = self.cursor.fetchall()
        for i in buscando_nome_cliente:
            self.tabela_clientes.insert("", END, values=i)

        self.limpar_tela()
        self.desconnect()


    def OnDoubleClick(self, event):
        self.limpar_tela()
        self.tabela_clientes.selection()

        for n in self.tabela_clientes.selection():
            col1, col2, col3, col4 = self.tabela_clientes.item(n, 'values')
            self.et_codigo.insert(END, col1)
            self.et_nome.insert(END, col2)
            self.et_telefone.insert(END, col3)
            self.et_cidade.insert(END, col4)


    def deleta_cliente(self):
        self.variaveis()
        self.conectar_db()

        self.cursor.execute("DELETE FROM clientes WHERE cod = ?", ([self.codigo]))

        self.banco.commit()
        self.desconnect()
        self.limpar_tela(tudo=False)
        self.select_lista()


    def alterar_cliente(self):
        self.variaveis()
        self.conectar_db()

        self.cursor.execute("UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ? WHERE cod = ?", (self.nome, self.telefone, self.cidade, self.codigo))
        
        self.banco.commit()
        self.desconnect()
        self.select_lista()
        self.limpar_tela()

    def preencher_cep(self):
        url = f"https://viacep.com.br/ws/{self.et_cep.get()}/json/"

        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados = resposta.json()
            self.limpar_tela()
            self.et_cidade.insert(END, dados.get('localidade', 'Não informado'))
            self.et_endereco.insert(END, dados.get('logradouro', 'Não informado'))
            self.et_bairro.insert(END, dados.get('bairro', 'Não informado'))
        else:
            messagebox.showerror("Erro ao tentar preencher CEP", "CEP Inválido!")


    def verificar_entry(self, event=None):
        self.entry_focada = str(root.focus_get())[-7:].replace(".", "").replace("!", "")
        if self.entry_focada == 'entry':
            self.et_nome.focus_set()
        elif self.entry_focada == 'entry2':
            self.et_cep.focus_set()
        elif self.entry_focada == 'entry3':
            self.et_telefone.focus_set()
        elif self.entry_focada == 'entry4':
            self.et_cidade.focus_set()
        elif self.entry_focada == 'entry5':
            self.et_endereco.focus_set()
        elif self.entry_focada == 'entry6':
            self.et_bairro.focus_set()
        elif self.entry_focada == 'entry7':
            self.add_clientes()
        else:
            print("Não identificado")


    def enter_pressionado(self):
        root.bind("<KeyPress-Return>", self.verificar_entry) #verificar_entry)


class Application(funcs, relatorios, validadores):
    # Carregamento da aplicação
    def __init__(self):
        self.root = root
        self.validaentradas()
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.tabela_frame2()
        self.monta_tabela()
        self.select_lista()
        self.menu()
        self.enter_pressionado()
        root.mainloop()

    # Configurações
    def tela(self):
        # Configurações
        self.root.title("Cadastro de Clientes")
        self.root.configure(background="#483D8B")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=1280, height=720)
        self.root.minsize(width=650, height=400)

    # Frames
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg="#6959CD", highlightbackground="#191970", highlightthickness=4)
        self.frame_1.place(relx=0.024, rely=0.03, relwidth=0.95, relheight=0.45)

        self.frame_2 = Frame(self.root, bd=4, bg="#6959CD", highlightbackground="#191970", highlightthickness=4)
        self.frame_2.place(relx=0.024, rely=0.52, relwidth=0.95, relheight=0.45)

    # Widgets do frame 1
    def widgets_frame1(self):
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame()
        self.aba1.configure(background='#6959CD')
        
        self.abas.add(self.aba1, text='Aba 1')
        
        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)
        
        self.bt_canvas = Canvas(self.aba1, bd=0, bg='#684cb3', highlightbackground='gray', highlightthickness=3)
        self.bt_canvas.place(relx=0.19, rely=0.08, relwidth=0.229, relheight=0.19)
        
        # Botão limpar
        self.bt_limpar = Button(self.aba1, text='Limpar', bg="#7B68EE", fg="white", activebackground='#8e1ce3', activeforeground='#6b619e', font=("verdana", 8, 'bold'), command=self.limpar_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão buscar
        self.bt_buscar = Button(self.aba1, text='Buscar', bg="#9370DB", fg="white", font=("verdana", 8, 'bold'), command=self.buscar_cliente)
        self.bt_buscar.place(relx=0.31, rely=0.1, relwidth=0.1, relheight=0.15)
        
        # Botão novo
        self.bt_novo = Button(self.aba1, text='Novo', bg="#9370DB", fg="white", font=("verdana", 8, 'bold'), command=self.add_clientes)
        self.bt_novo.place(relx=0.65, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão alterar
        self.bt_alterar = Button(self.aba1, text='Alterar', bg="#9370DB", fg="white", font=("verdana", 8, 'bold'), command=self.alterar_cliente)
        self.bt_alterar.place(relx=0.76, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão apagar
        self.bt_apagar = Button(self.aba1, text='Apagar', bg="#7B68EE", fg="white", font=("verdana", 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.87, rely=0.1, relwidth=0.1, relheight=0.15)

        # Caixa de mensagem código
        self.lb_codigo = Label(self.aba1, text="Código", bg="#6959CD", fg="white")
        self.lb_codigo.place(relx=0.02, rely=0.05)

        self.et_codigo = Entry(self.aba1, validate="key", validatecommand=self.vcmd2)
        self.et_codigo.place(relx=0.02, rely=0.15, relwidth=0.07, relheight=0.12)

        # Caixa de mensagem nome
        self.lb_nome = Label(self.aba1, text="Nome", bg="#6959CD", fg="white")
        self.lb_nome.place(relx=0.02, rely=0.3)

        self.et_nome = Entry(self.aba1)
        self.et_nome.place(relx=0.02, rely=0.4, relwidth=0.6, relheight=0.1)

        # Caixa de mensagem CEP
        self.bt_cep = Button(self.aba1, text="CEP", bg="#EE4781", fg="white", command=self.preencher_cep)
        self.bt_cep.place(relx=0.67, rely=0.29, relheight=0.1)

        self.et_cep = Entry(self.aba1)
        self.et_cep.place(relx=0.67, rely=0.4, relwidth=0.3, relheight=0.1)

        # Caixa de mensagem telefone
        self.lb_telefone = Label(self.aba1, text="Telefone", bg="#6959CD", fg="white")
        self.lb_telefone.place(relx=0.02, rely=0.5)

        self.et_telefone = Entry(self.aba1)
        self.et_telefone.place(relx=0.02, rely=0.6, relwidth=0.45, relheight=0.1)
        
        # Caixa de mensagem cidade
        self.lb_cidade = Label(self.aba1, text="Cidade", bg="#6959CD", fg="white")
        self.lb_cidade.place(relx=0.52, rely=0.5)

        self.et_cidade = Entry(self.aba1)
        self.et_cidade.place(relx=0.52, rely=0.6, relwidth=0.45, relheight=0.1)
    
        # Caixa de mensagem endereço
        self.lb_endereco = Label(self.aba1, text="Endereço", bg="#6959CD", fg="white")
        self.lb_endereco.place(relx=0.02, rely=0.7)

        self.et_endereco = Entry(self.aba1)
        self.et_endereco.place(relx=0.02, rely=0.8, relwidth=0.45, relheight=0.1)

        # Caixa de mensagem bairro
        self.lb_bairro = Label(self.aba1, text="Bairro", bg="#6959CD", fg="white")
        self.lb_bairro.place(relx=0.52, rely=0.7)

        self.et_bairro = Entry(self.aba1)
        self.et_bairro.place(relx=0.52, rely=0.8, relwidth=0.45, relheight=0.1)

    # Tabela de clientes
    def tabela_frame2(self):
        self.tabela_clientes = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3", "col4"))
        self.tabela_clientes.heading("#0", text="")
        self.tabela_clientes.heading("#1", text="Código")
        self.tabela_clientes.heading("#2", text="Nome")
        self.tabela_clientes.heading("#3", text="Telefone")
        self.tabela_clientes.heading("#4", text="Cidade")

        self.tabela_clientes.column("#0", width=1)
        self.tabela_clientes.column("#1", width=50)
        self.tabela_clientes.column("#2", width=200)
        self.tabela_clientes.column("#3", width=125)
        self.tabela_clientes.column("#4", width=125)

        self.tabela_clientes.place(relx=0.025, rely=0.05, relwidth=0.95, relheight=0.90)

        # ScrollBar
        self.scroll_tabela = Scrollbar(self.frame_2, orient="vertical", command=self.tabela_clientes.yview)
        self.tabela_clientes.configure(yscroll=self.scroll_tabela.set)
        self.scroll_tabela.place(relx=0.94, rely=0.051, relwidth=0.04, relheight=0.897)
        self.tabela_clientes.bind("<Double-1>", self.OnDoubleClick)


    def menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)


        menubar.add_cascade(label= "Opções", menu=filemenu)
        menubar.add_cascade(label= "Relatórios", menu=filemenu2)
        filemenu.add_command(label="Sair", command=root.quit)
        filemenu.add_command(label="Limpa cliente", command=self.limpar_tela)

        filemenu2.add_command(label="Ficha do cliente", command=self.gerar_relatorio_cliente)

    def validaentradas(self):
        self.vcmd2 = (self.root.register(self.validate_entry2), "%P")

if __name__ == "__main__":
    Application()
