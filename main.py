from customtkinter import *
from customtkinter import filedialog
import os

app = CTk()

class functions():
    # Abre o arquivo txt
    def abrir_arquivo(self):
        self.arquivo = filedialog.askopenfile(title='Selecione um arquivo de texto', filetypes=[('Arquivo de texto', '*.txt')])

        if not self.arquivo == '' or not self.arquivo == None:
            self.nome_extensao = os.path.basename(self.arquivo.name)
            self.nome = os.path.splitext(self.nome_extensao)[0]
            self.tv_editor.add(self.nome)
            
            self.tb_editor_text = CTkTextbox(master=self.tv_editor.tab(self.nome), border_spacing=15, font=('consolas', 17, 'bold'))
            self.tb_editor_text.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')
            self.tv_editor.set(self.nome)
            self.tb_editor_text.insert('1.0', self.arquivo.read())

    # Salva o arquivo txt
    def salvar_arquivo(self):
        self.arquivo = filedialog.asksaveasfilename(title='Salvar como...',
                                                    defaultextension='.txt',
                                                    filetypes=[('Arquivo de texto', '*.txt')])
        if not self.arquivo == '' or not self.arquivo == None:
            self.conteudo = self.tb_editor_text.get('1.0', 'end')
            print(self.conteudo)
            with open(self.arquivo) as arquivo_:
                arquivo_.write(self.conteudo)

# Programa principal
class main(functions):
    def __init__(self):
        self.app = app
        self.configuration()
        self.widgets_frameprincipal()
        app.mainloop()
    
    def configuration(self):
        self.app.geometry("550x600")
        self.app.minsize(300, 300)
        self.app.title("Editor De Texto Avançado")

    def widgets_frameprincipal(self):
        # Editor
        self.tv_editor = CTkTabview(master=app, anchor='nw')
        self.tv_editor.place(relx=0.5, rely=0.53, relwidth=0.9, relheight=0.9,anchor='center')
        self.tv_editor.add('text')

        # Editor Text
        self.tb_editor_text = CTkTextbox(master=self.tv_editor.tab('text'), border_spacing=15, font=('consolas', 17, 'bold'))
        self.tb_editor_text.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')

        # Abrir arquivo
        self.bt_abrir = CTkButton(master=app, text='Abrir arquivo', command=self.abrir_arquivo)
        self.bt_abrir.place(relx=0.06, rely=0.04)
        
        # Salvar arquivo
        self.bt_salvar = CTkButton(master=app, text='Salvar arquivo', command=self.salvar_arquivo)
        self.bt_salvar.place(relx=0.33, rely=0.04)

if __name__ == "__main__":       
    main()