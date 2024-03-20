from tkinter import ttk, messagebox 
from tkinter import *

import re
import os
import sqlite3

class Utilisateurs:
    def __init__(self, root):
        self.root = root
        self.root.title("Nouveau client")
        self.root.geometry("800x600+100+100")

        # Formulaire pour ajouter un utilisateur
        gestion_form = Frame(self.root, bd=5, relief=GROOVE, bg="lightblue")
        gestion_form.place(x=10, y=50, width=530, height=700)

        gestion_title = ttk.Label(gestion_form, text="Information de l'utilisateur", font=("Helvetica", 26, "bold"))
        gestion_title.place(x=50, y=30)
        #les variables
        self.recherch_par = StringVar()
        self.rechrch = StringVar()
        

        # Id utilisateur
        id_utilisateur = Label(gestion_form, text="Id Contact", font=("times new roman", 18))
        id_utilisateur.place(x=30, y=90)

        id_txt = Entry(gestion_form, font=("times new roman", 18), bg="white")
        id_txt.place(x=200, y=90)

        # Nom complet
        nom_complet = Label(gestion_form, text="Nom complet", font=("times new roman", 18))
        nom_complet.place(x=30, y=130)

        nom_txt = Entry(gestion_form, font=("times new roman", 18), bg="white")
        nom_txt.place(x=200, y=130)

        # E-mail
        email = Label(gestion_form, text="E-mail", font=("times new roman", 18))
        email.place(x=30, y=170)

        email_txt = Entry(gestion_form, font=("times new roman", 18), bg="white")
        email_txt.place(x=200, y=170)

        # Sexe
        sexe = Label(gestion_form, text="Sexe", font=("times new roman", 18))
        sexe.place(x=30, y=210)

        sexe_txt = ttk.Combobox(gestion_form, font=("times new roman", 18), state="readonly")
        sexe_txt["values"] = ("Homme", "Femme" , "non")
        sexe_txt.place(x=200, y=210, width=160)
        sexe_txt.current(0)

        # Contact
        contact = Label(gestion_form, text="N° Téléphone", font=("times new roman", 18))
        contact.place(x=30, y=250)

        contact_txt = Entry(gestion_form, font=("times new roman", 18), bg="white")
        contact_txt.place(x=200, y=250)

        # Date de naissance
        date_naissance = Label(gestion_form, text="Date naissance", font=("times new roman", 18))
        date_naissance.place(x=30, y=290)

        date_naissance_txt = Entry(gestion_form, font=("times new roman", 18), bg="white")
        date_naissance_txt.place(x=200, y=290)
        
        # Adresse  
        adresse = Label(gestion_form, text="Adresse", font=("times new roman", 18))
        adresse.place(x=30, y=340)

        adresse_txt = Text(gestion_form, font=("times new roman", 14), bg="white")
        adresse_txt.place(x=200, y=340, width=245, height=100)

        # Bouton Ajouter
        btn_ajouter = Button(gestion_form,command=self.ajou_utulisateur, text="Ajouter", font=("times new roman", 16), bd=5, relief=GROOVE, bg="green")
        btn_ajouter.place(x=10, y=520, width=100)

        # Bouton Modifier
        btn_modifier = Button(gestion_form, command=self.Modifier,text="Modifier", font=("times new roman", 16), bd=5, relief=GROOVE, bg="orange")
        btn_modifier.place(x=140, y=520, width=100)

        # Bouton Supprimer
        btn_supprimer = Button(gestion_form,command=self.Supprimer, text="Supprimer", font=("times new roman", 16), bd=5, relief=GROOVE, bg="red")
        btn_supprimer.place(x=270, y=520, width=100)

        # Bouton rénitialiser 
        btn_rénitialiser = Button(gestion_form,command=self.reinisialisa, text="Rénitialiser", font=("times new roman", 16), bd=5, relief=GROOVE, bg="GRAY")
        btn_rénitialiser.place(x=400, y=520, width=100)

        #affichage bdd
        Details_frame = Frame(self.root, bd=5,relief=GROOVE, bg="lightblue")
        Details_frame.place(x=600,y=50,width=830,height=700)

        affiche_résultat = Label(Details_frame, text="Recherhce par :", font=("times new roman", 18,"bold"),bg="lightgray")
        affiche_résultat.place(x=30 ,y=40)

        #barre de recherche
        rech=ttk.Combobox(Details_frame,textvariable=self.recherch_par,font=("times new roman ",18), state="readonly")
        rech["values"] = ("Id","Nom","Cantact","Adresse")
        rech.place(x=220, y= 40, width=140,height=30)

        #barre de recherche par texte 
        rech_txt =Entry(Details_frame,textvariable=self.rechrch, font=("times new roman",14),bd=5,relief=GROOVE )
        rech_txt.place(x=400,y=40,width=140 ,height=30)
        
        #recherche btn
        btn_rech = Button(Details_frame,command=self.recherche_info, text=" Recherche",font=("times new roman",13),bd=10,bg="gray",relief=GROOVE)
        btn_rech.place(x=550,y=35,width=120,height=40)

        #recherche AFFICHER TOUS
        btn_affiche = Button(Details_frame,command=self.affiche_utulis, text=" Afficher tous",font=("times new roman",13),bd=10,bg="gray",relief=GROOVE)
        btn_affiche.place(x=680,y=35,width=120,height=40)
               
        #Affichage

        resultat_frame = Frame(Details_frame, bd=10, relief=GROOVE, bg="white")
        resultat_frame.place(x=10,y=200,width=790,height=400)

        #scrool horizental et vertical 
        SCROLL_x= Scrollbar(Details_frame, orient=HORIZONTAL)
        SCROLL_y=Scrollbar(Details_frame, orient=VERTICAL)
        self.tbl_reslt = ttk.Treeview(resultat_frame, columns=("id","nom","mail","sexe","contact","dat","adresse"),xscrollcommand=SCROLL_x.set, yscrollcommand=SCROLL_y.set)
        
        SCROLL_x.pack(side=BOTTOM, fill=X)
        SCROLL_y.pack(side=RIGHT, fill=Y)
        SCROLL_x.config(command=self.tbl_reslt.xview)
        SCROLL_y.config(command=self.tbl_reslt.yview)

        #  faire appel au colonnes
        self.tbl_reslt.heading("id", text="ID Contact")
        self.tbl_reslt.heading("nom", text="Nom complet")
        self.tbl_reslt.heading("mail", text="E-mail")
        self.tbl_reslt.heading("sexe", text="Sexe")
        self.tbl_reslt.heading("contact", text="Contact")
        self.tbl_reslt.heading("dat", text="Date_naissance")
        self.tbl_reslt.heading("adresse", text="Adresse")

        #afficher les headings

        self.tbl_reslt["show"]="headings"
        self.tbl_reslt.column("id",width=90)
        self.tbl_reslt.column("nom",width=120)
        self.tbl_reslt.column("mail",width=180)
        self.tbl_reslt.column("sexe",width=120)
        self.tbl_reslt.column("contact",width=120)
        self.tbl_reslt.column("dat", width=120)
        self.tbl_reslt.column("adresse",width=180)

        self.tbl_reslt.pack()
        self.tbl_reslt.bind("<ButtonRelease-1>", self.Sélectionne)
        self.affiche_utulis()
        conn = sqlite3.connect('hello.db')
        cur = conn.cursor()
        
        # CreatION DE LA BDD SI IL EXISTE PSA
        cur.execute('''
            CREATE TABLE IF NOT EXISTS projet (
                id INTEGER PRIMARY KEY,
                nom TEXT,
                mail TEXT,
                sexe TEXT,
                contact INTEGER,
                dat INTEGER,
                adresse TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        self.affiche_utulis()


         # INITIALISATION 
        self.id_txt = id_txt
        self.nom_txt = nom_txt
        self.email_txt = email_txt
        self.sexe_txt = sexe_txt
        self.contact_txt = contact_txt
        self.date_naissance_txt = date_naissance_txt
        self.adresse_txt = adresse_txt


    def ajou_utulisateur(self):
        # Vérification si tous les champs obligatoires sont remplis
        if any(value.get() == "" for value in [self.id_txt, self.nom_txt, self.email_txt, self.contact_txt]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires", parent=self.root)
            return

        # Validation de l'e-mail
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, self.email_txt.get()):
            messagebox.showerror("Erreur", "Adresse e-mail incorrecte", parent=self.root)
            return

        # Validation de l'adresse
        if len(self.adresse_txt.get("1.0", END)) <= 1:
            messagebox.showerror("Erreur", "Adresse incorrecte", parent=self.root)
            return

        # Validation du numéro de téléphone
        if not (self.contact_txt.get().isdigit() and len(self.contact_txt.get()) <= 10):
            messagebox.showerror("Erreur", "Numéro de téléphone invalide", parent=self.root)
            return

        conn = sqlite3.connect('hello.db')
        cur = conn.cursor()
        # Utilisation des marqueurs de substitution de paramètres (?)
        cur.execute("INSERT INTO projet VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (self.id_txt.get(), self.nom_txt.get(), self.email_txt.get(), self.sexe_txt.get(), 
                     self.contact_txt.get(), self.date_naissance_txt.get(), self.adresse_txt.get("1.0", END)))
        conn.commit()
        self.affiche_utulis()
        self.reinisialisa()
        conn.close()
        messagebox.showinfo("Succès", "Enregistrement effectué")

    def affiche_utulis(self):
        conn = sqlite3.connect('hello.db')
        cur = conn.cursor()

        # SUPPRIMER ET PRET à mettre à jour les données 
        self.tbl_reslt.delete(*self.tbl_reslt.get_children())

        cur.execute("SELECT * FROM projet")
        rows = cur.fetchall()

        for row in rows:
            self.tbl_reslt.insert("", END, values=row)

        conn.commit()
        conn.close()


    
    def Sélectionne(self, ev):
      cursors_row = self.tbl_reslt.focus()
      contents = self.tbl_reslt.item(cursors_row)
      row = contents["values"]
  
      # Mettez à jour les Entry et Text avec les valeurs de la ligne sélectionnée
      self.id_txt.delete(0, END)
      self.id_txt.insert(END, row[0])
  
      self.nom_txt.delete(0, END)
      self.nom_txt.insert(END, row[1])
  
      self.email_txt.delete(0, END)
      self.email_txt.insert(END, row[2])
  
      self.sexe_txt.set(row[3])
  
      self.contact_txt.delete(0, END)
      self.contact_txt.insert(END, row[4])
  
      self.date_naissance_txt.delete(0, END)
      self.date_naissance_txt.insert(END, row[5])
  
      self.adresse_txt.delete("1.0", END)
      self.adresse_txt.insert(END, row[6])
    
    def reinisialisa(self):
        self.id_txt.delete(0, END)
        self.nom_txt.delete(0, END)
        self.email_txt.delete(0, END)
        self.sexe_txt.set("")
        self.contact_txt.delete(0, END)
        self.date_naissance_txt.delete(0, END)
        self.adresse_txt.delete("1.0", END)

       

    def Modifier(self):
        conn = sqlite3.connect('hello.db')
        cur = conn.cursor()
        
        cur.execute("UPDATE projet SET nom=?, mail=?, sexe=?, contact=?, dat=?, adresse=? WHERE id=?",
                    (self.nom_txt.get(), self.email_txt.get(), self.sexe_txt.get(),
                     self.contact_txt.get(), self.date_naissance_txt.get(), self.adresse_txt.get("1.0", END), self.id_txt.get()))
        
        conn.commit()
        messagebox.showinfo("Succes", "Modification effectuée")
        self.affiche_utulis()
        self.reinitialiser()
        conn.close()


    def Supprimer(self):
        conn = sqlite3.connect('hello.db')
        cur = conn.cursor()
        cur.execute("DELETE from projet where id = ? ",(self.id_txt.get(),))
        conn.commit()
        self.affiche_utulis()
        self.reinisialisa()
        conn.close()
    
    def recherche_info(self):
        conn = sqlite3.connect('hello.db')
        cur = conn.cursor()
        query = "SELECT * FROM projet WHERE {} LIKE ?".format(self.recherch_par.get())
        search_value = '%' + str(self.rechrch.get()) + '%'
        cur.execute(query, (search_value.lower(),))
    
        rows = cur.fetchall()
        # Supprime toutes les lignes actuelles de l'affichage
        self.tbl_reslt.delete(*self.tbl_reslt.get_children())
    
        if len(rows) != 0:
            for row in rows:
                # Insère la ligne correspondante à la recherche
                self.tbl_reslt.insert('', END, values=row)
        else:
            messagebox.showinfo("Aucune correspondance", "Aucun résultat trouvé pour la recherche.")
    
        conn.commit()
        conn.close()
    
         
root = Tk()
obj = Utilisateurs(root)
root.mainloop()