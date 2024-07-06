import customtkinter
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import messagebox
import time
import threading
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import minimize
import math
from datetime import datetime, timedelta
from tkinter import font

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.iconbitmap("icon_app_test_1.ico")
        self.title("ZC Calculator")
        self.geometry("700x550")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        self.logo_image = customtkinter.CTkImage(Image.open("zero_precis.png"), size=(40, 40))
        self.large_test_image = customtkinter.CTkImage(Image.open("data_image_111.png"), size=(360, 125))
        self.vasicek_eds_image = customtkinter.CTkImage(Image.open("vasicek_eds_1.png"), size=(360, 125))
        self.cir_eds_image = customtkinter.CTkImage(Image.open("cir_eds_1.png"), size=(360, 125))
        self.marche_image = customtkinter.CTkImage(Image.open("marche_img.png"), size=(360, 125))
        self.courbes_zc_image = customtkinter.CTkImage(Image.open("courbes_zc.png"), size=(360, 125))
        self.image_icon_image = customtkinter.CTkImage(Image.open("image_icon_light.png"), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open("data_icon_black.png"),
                                                 dark_image=Image.open("data_icon_light.png"), size=(26, 26))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open("market_icon_black.png"),
                                                 dark_image=Image.open("market_icon_light.png"), size=(26, 26))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open("vasicek_icon_black.png"),
                                                     dark_image=Image.open("vasicek_icon_light.png"), size=(30, 30))
        self.cir_txt_image = customtkinter.CTkImage(light_image=Image.open("cir_icon_black.png"),
                                                     dark_image=Image.open("cir_icon_light.png"), size=(30, 30))
        self.zc_txt_image = customtkinter.CTkImage(light_image=Image.open("zc_icon_black.png"),
                                                     dark_image=Image.open("zc_icon_light.png"), size=(30, 30))
        self.importation_icon_image = customtkinter.CTkImage(Image.open("importation_icon_light.png"), size=(18, 18))
        self.calendar_icon_image = customtkinter.CTkImage(Image.open("calendar_icon_light.png"), size=(18, 18))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Le Zéro Précis", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Data",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Marché",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Vašíček",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")
        
        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Cox-Ingersoll-Ross",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.cir_txt_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")
        
        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Courbes Zéro Coupon",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.zc_txt_image, anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=8, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=30, pady=(30,5))

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=30, pady=(30,10))
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=350)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(90, 0))
        self.tabview.add("TMP BDT")
        self.tabview.add("TMP interbancaire")
        self.tabview.tab("TMP BDT").grid_columnconfigure(0, weight=1)
        self.tabview.tab("TMP interbancaire").grid_columnconfigure(0, weight=1)
        
        self.text_label = customtkinter.CTkLabel(self.tabview.tab("TMP BDT"), text="Entrer la date correspondante")
        self.text_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self.tabview.tab("TMP BDT"), textvariable=self.var, state="readonly")
        self.entry.grid(row=1, column=0, padx=(5,40), pady=(20, 10))
        self.home_frame_button_1 = customtkinter.CTkButton(self.tabview.tab("TMP BDT"), text="", image=self.calendar_icon_image, command=self.open_calendar, width=10)
        self.home_frame_button_1.grid(row=1, column=0, padx=(140,5), pady=(20, 10))
        
        self.home_frame_button_1_import = customtkinter.CTkButton(self.tabview.tab("TMP BDT"), text="Importer", image=self.importation_icon_image, compound="right", command=self.importer_ref_date)
        self.home_frame_button_1_import.grid(row=2, column=0, padx=20, pady=(30,5))
        
        self.progress_label_1 = customtkinter.CTkLabel(self.tabview.tab("TMP BDT"), text="Importation en cours...")
        
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("TMP interbancaire"), text="Entrer la date début et la date fin")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        self.var_debut = tk.StringVar()
        self.label_tab_2_1 = customtkinter.CTkLabel(self.tabview.tab("TMP interbancaire"), text="Date début :")
        self.label_tab_2_1.grid(row=1, column=0, padx=(5,180), pady=(20, 10))
        self.entry_debut = ttk.Entry(self.tabview.tab("TMP interbancaire"), textvariable=self.var_debut, state="readonly")
        self.entry_debut.grid(row=1, column=0, padx=(50,10), pady=(20, 10))
        self.home_frame_button_2 = customtkinter.CTkButton(self.tabview.tab("TMP interbancaire"), text="", image=self.calendar_icon_image, command=self.open_calendar_1, width=10)
        self.home_frame_button_2.grid(row=1, column=0, padx=(220,5), pady=(20, 10))
        
        self.var_fin = tk.StringVar()
        self.label_tab_2_2 = customtkinter.CTkLabel(self.tabview.tab("TMP interbancaire"), text="Date fin :")
        self.label_tab_2_2.grid(row=2, column=0, padx=(5,180), pady=(20, 10))
        self.entry_fin = ttk.Entry(self.tabview.tab("TMP interbancaire"), textvariable=self.var_fin, state="readonly")
        self.entry_fin.grid(row=2, column=0, padx=(50,10), pady=(20, 10))
        self.home_frame_button_3 = customtkinter.CTkButton(self.tabview.tab("TMP interbancaire"), text="", image=self.calendar_icon_image, command=self.open_calendar_2, width=10)
        self.home_frame_button_3.grid(row=2, column=0, padx=(220,5), pady=(20, 10))
              
        self.home_frame_button_2_import = customtkinter.CTkButton(self.tabview.tab("TMP interbancaire"), text="Importer", image=self.importation_icon_image, compound="right", command=self.importer_tmp_inter_dates)
        self.home_frame_button_2_import.grid(row=3, column=0, padx=20, pady=(30,5))
        
        self.progress_label = customtkinter.CTkLabel(self.tabview.tab("TMP interbancaire"), text="Importation en cours...")

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.marche_image)
        self.second_frame_large_image_label.grid(row=0, column=0, padx=30, pady=(30,20))
        
        self.second_frame_label_1 = customtkinter.CTkLabel(self.second_frame, text="TMP des BDTs     :", font=("Helvetica", 16))
        self.second_frame_label_1.grid(row=1, column=0, padx=(80,180), pady=(20, 10))
        
        self.second_frame_button_1 = customtkinter.CTkButton(self.second_frame, text="Afficher", width=80, command=self.affiche_data_ref)
        self.second_frame_button_1.grid(row=1, column=0, padx=(230,5), pady=(20, 10))
        
        self.second_frame_label_2 = customtkinter.CTkLabel(self.second_frame, text="Taux Zéro Coupon et Actuariel   :", font=("Helvetica", 16))
        self.second_frame_label_2.grid(row=2, column=0, padx=(80,180), pady=(20, 10))
        
        self.second_frame_button_2 = customtkinter.CTkButton(self.second_frame, text="Afficher", width=80, command=self.data_zc_actuariel)
        self.second_frame_button_2.grid(row=2, column=0, padx=(230,5), pady=(20, 10))
        
        self.second_frame_label_3 = customtkinter.CTkLabel(self.second_frame, text="Courbe Zéro Coupon     :", font=("Helvetica", 16))
        self.second_frame_label_3.grid(row=3, column=0, padx=(80,180), pady=(20, 10))
        
        self.second_frame_button_3 = customtkinter.CTkButton(self.second_frame, text="Afficher", width=80, command=self.courbe_zc)
        self.second_frame_button_3.grid(row=3, column=0, padx=(230,5), pady=(20, 10))
        
        self.second_frame_label_4 = customtkinter.CTkLabel(self.second_frame, text="Courbe Actuariel     :", font=("Helvetica", 16))
        self.second_frame_label_4.grid(row=4, column=0, padx=(80,180), pady=(20, 10))
        
        self.second_frame_button_4 = customtkinter.CTkButton(self.second_frame, text="Afficher", width=80, command=self.courbe_actuariel)
        self.second_frame_button_4.grid(row=4, column=0, padx=(230,5), pady=(20, 10))
        
        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)

        self.third_frame_large_image_label = customtkinter.CTkLabel(self.third_frame, text="", image=self.vasicek_eds_image)
        self.third_frame_large_image_label.grid(row=0, column=0, padx=30, pady=(30,20))
        
        self.third_frame_label_1 = customtkinter.CTkLabel(self.third_frame, text="Estimation et Backtesting     :", font=("Helvetica", 16))
        self.third_frame_label_1.grid(row=1, column=0, padx=(80,180), pady=(20, 10))
        
        self.third_frame_button_1 = customtkinter.CTkButton(self.third_frame, text="Afficher", width=80, command=self.affiche_backtesting_vas)
        self.third_frame_button_1.grid(row=1, column=0, padx=(230,5), pady=(20, 10))
        
        self.third_frame_label_2 = customtkinter.CTkLabel(self.third_frame, text="Courbe Zéro Coupon     :", font=("Helvetica", 16))
        self.third_frame_label_2.grid(row=2, column=0, padx=(80,180), pady=(20, 10))
        
        self.third_frame_button_2 = customtkinter.CTkButton(self.third_frame, text="Afficher", width=80, command=self.courbe_zc_vas)
        self.third_frame_button_2.grid(row=2, column=0, padx=(230,5), pady=(20, 10))
        
        # create fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame.grid_columnconfigure(0, weight=1)

        self.fourth_frame_large_image_label = customtkinter.CTkLabel(self.fourth_frame, text="", image=self.cir_eds_image)
        self.fourth_frame_large_image_label.grid(row=0, column=0, padx=30, pady=(30,20))
        
        self.fourth_frame_label_1 = customtkinter.CTkLabel(self.fourth_frame, text="Estimation et Backtesting     :", font=("Helvetica", 16))
        self.fourth_frame_label_1.grid(row=1, column=0, padx=(80,180), pady=(20, 10))
        
        self.fourth_frame_button_1 = customtkinter.CTkButton(self.fourth_frame, text="Afficher", width=80, command=self.affiche_backtesting_cir)
        self.fourth_frame_button_1.grid(row=1, column=0, padx=(230,5), pady=(20, 10))
        
        self.fourth_frame_label_2 = customtkinter.CTkLabel(self.fourth_frame, text="Courbe Zéro Coupon     :", font=("Helvetica", 16))
        self.fourth_frame_label_2.grid(row=2, column=0, padx=(80,180), pady=(20, 10))
        
        self.fourth_frame_button_2 = customtkinter.CTkButton(self.fourth_frame, text="Afficher", width=80, command=self.courbe_zc_cir)
        self.fourth_frame_button_2.grid(row=2, column=0, padx=(230,5), pady=(20, 10))
        
        # create fifth frame
        self.fifth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fifth_frame.grid_columnconfigure(0, weight=1)

        self.fifth_frame_large_image_label = customtkinter.CTkLabel(self.fifth_frame, text="", image=self.courbes_zc_image)
        self.fifth_frame_large_image_label.grid(row=0, column=0, padx=30, pady=(30,20))
        
        self.label_tab_2_zc = customtkinter.CTkLabel(self.fifth_frame, text="Entrer la date début et la date fin", font=("Helvetica", 16))
        self.label_tab_2_zc.grid(row=1, column=0, padx=20, pady=(20, 5))
        
        self.var_debut_zc = tk.StringVar()
        self.label_tab_2_1_zc = customtkinter.CTkLabel(self.fifth_frame, text="Date début :", font=("Helvetica", 16))
        self.label_tab_2_1_zc.grid(row=2, column=0, padx=(5,200), pady=(20, 10))
        self.entry_debut_zc = ttk.Entry(self.fifth_frame, textvariable=self.var_debut_zc, state="readonly")
        self.entry_debut_zc.grid(row=2, column=0, padx=(50,10), pady=(20, 10))
        self.home_frame_button_2_zc = customtkinter.CTkButton(self.fifth_frame, text="", image=self.calendar_icon_image, command=self.open_calendar_3, width=10)
        self.home_frame_button_2_zc.grid(row=2, column=0, padx=(220,5), pady=(20, 10))
        
        self.var_fin_zc = tk.StringVar()
        self.label_tab_2_2_zc = customtkinter.CTkLabel(self.fifth_frame, text="Date fin :", font=("Helvetica", 16))
        self.label_tab_2_2_zc.grid(row=3, column=0, padx=(5,180), pady=(20, 10))
        self.entry_fin_zc = ttk.Entry(self.fifth_frame, textvariable=self.var_fin_zc, state="readonly")
        self.entry_fin_zc.grid(row=3, column=0, padx=(50,10), pady=(20, 10))
        self.home_frame_button_3_zc = customtkinter.CTkButton(self.fifth_frame, text="", image=self.calendar_icon_image, command=self.open_calendar_4, width=10)
        self.home_frame_button_3_zc.grid(row=3, column=0, padx=(220,5), pady=(20, 10))
              
        self.fifth_frame_button_1 = customtkinter.CTkButton(self.fifth_frame, text="Afficher", width=90, command=self.affiche_zc_dates)
        self.fifth_frame_button_1.grid(row=4, column=0, padx=(50,5), pady=(20, 10))
        
        self.progress_label_zc = customtkinter.CTkLabel(self.fifth_frame, text="Calcul en cours...")
        
        # create sixth frame
        self.sixth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fifth_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
        
    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")
        
    def frame_5_button_event(self):
        self.select_frame_by_name("frame_5")
        
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def open_calendar(self):
        def set_selected_date():
            selected_date = cal.selection_get().strftime('%d/%m/%Y')
            self.var.set(selected_date)
            top.destroy()

        top = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top.iconbitmap(icon_path)

        import datetime
        today = datetime.date.today()

        mindate = datetime.date(year=2001, month=1, day=1)
        maxdate = today + datetime.timedelta(days=5)

        cal = Calendar(top, font="Arial 12 bold", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1")
        cal.pack(fill="both", expand=True)

        ttk.Button(top, text="OK", command=set_selected_date).pack()
        
    def open_calendar_1(self):
        def set_selected_date_1():
            selected_date_debut = cal_1.selection_get().strftime('%d/%m/%Y')
            self.var_debut.set(selected_date_debut)
            top_1.destroy()

        top_1 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_1.iconbitmap(icon_path)

        import datetime
        today = datetime.date.today()

        mindate = datetime.date(year=2001, month=1, day=1)
        maxdate = today + datetime.timedelta(days=5)

        cal_1 = Calendar(top_1, font="Arial 12 bold", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1")
        cal_1.pack(fill="both", expand=True)

        ttk.Button(top_1, text="OK", command=set_selected_date_1).pack()
        
    def open_calendar_2(self):
        def set_selected_date_2():
            selected_date_fin = cal_2.selection_get().strftime('%d/%m/%Y')
            self.var_fin.set(selected_date_fin)
            top_2.destroy()

        top_2 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_2.iconbitmap(icon_path)

        import datetime
        today = datetime.date.today()

        mindate = datetime.date(year=2001, month=1, day=1)
        maxdate = today + datetime.timedelta(days=5)

        cal_2 = Calendar(top_2, font="Arial 12 bold", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1")
        cal_2.pack(fill="both", expand=True)

        ttk.Button(top_2, text="OK", command=set_selected_date_2).pack()
        
    def importer_ref_date(self):
        
        
        entered_text = self.var.get()
        global ref_date
        ref_date = entered_text
        
        
        if entered_text:
            
            date_ref = datetime.strptime(entered_text, '%d/%m/%Y')
            jour_ref = date_ref.day
            mois_ref_tst = date_ref.month
            mois_ref = "{:02d}".format(mois_ref_tst)
            annee_ref = date_ref.year
            
            url = "https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-secondaire/Taux-de-reference-des-bons-du-tresor?date="+str(jour_ref)+"%2F"+mois_ref+"%2F"+str(annee_ref)+"&block=e1d6b9bbf87f86f8ba53e8518e882982#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982"

            # Téléchargement du contenu de la page web
            response = requests.get(url)
            html_content = response.content

            # Utilisation de BeautifulSoup pour analyser le contenu HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # Recherche de la première table dans le contenu HTML
            table = soup.find("table")

            if table is None:
                messagebox.showwarning("Warning", "Ancune table pour ce jour !")

            else:
                global data
                data = []
                
                self.home_frame_button_1_import.configure(state="disabled")
            
                self.progress_label_1.grid(row=3, column=0, padx=20, pady=5)
                
                def scrape_and_update_ui_1():
                    try:
                        for row in table.find_all("tr"):
                            cells = row.find_all("td")
                            if len(cells) > 0:
                                date_echeance = cells[0].get_text().strip()
                                transaction = cells[1].get_text().strip()
                                taux = cells[2].get_text().strip()
                                date_valeur = cells[3].get_text().strip()
                                data.append([date_echeance, transaction, taux, date_valeur])
                                
                        self.progress_label_1.grid_forget()
                        self.home_frame_button_1_import.configure(state="normal")
                        headers = ["Date d'échéance", "Transaction", "Taux", "Date de valeur"]
                        global df
                        df = pd.DataFrame(data, columns=headers)
                        
                        messagebox.showinfo("Information", "Importation terminé")
                        
                        
                        
                    except Exception as e:
                        self.home_frame_button_1_import.configure(state="normal")
                        self.progress_label_1.grid_forget()
                        messagebox.showerror("Erreur", "Erreur, Veuillez réessayer !")
                
                scraping_thread = threading.Thread(target=scrape_and_update_ui_1)
                scraping_thread.start()
                
        else:
            messagebox.showerror("Erreur", "Veuillez entrer une date !")
                
                
    def importer_tmp_inter_dates(self):
        
        entered_text = self.var.get()
        entered_text_1 = self.var_debut.get()
        entered_text_2 = self.var_fin.get()
        
        if entered_text_1 and entered_text_2:
            
            if entered_text:
                
                date = datetime.strptime(entered_text, '%d/%m/%Y').date()
                date_1 = datetime.strptime(entered_text_1, '%d/%m/%Y').date()
                date_2 = datetime.strptime(entered_text_2, '%d/%m/%Y').date()
                    
                    
                
                if date_1 < date and date < date_2:
                    
                    
                    jour_date_debut = date_1.day
                    mois_date_debut_tst = date_1.month
                    mois_date_debut = "{:02d}".format(mois_date_debut_tst)
                    annee_date_debut = date_1.year
                    
                    jour_date_fin = date_2.day
                    mois_date_fin_tst = date_2.month
                    mois_date_fin = "{:02d}".format(mois_date_fin_tst)
                    annee_date_fin = date_2.year
                    
                    url_1 = "https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire?limit=0&startDate="+str(jour_date_debut)+"%2F"+mois_date_debut+"%2F"+str(annee_date_debut)+"&endDate="+str(jour_date_fin)+"%2F"+mois_date_fin+"%2F"+str(annee_date_fin)+"&block=ae14ce1a4ee29af53d5645f51bf0e97d#address-d3239ec6d067cd9381f137545720a6c9-ae14ce1a4ee29af53d5645f51bf0e97d"

                    # Télécharger le contenu HTML de l'URL
                    response = requests.get(url_1)
                    html = response.text

                    # Analyser le HTML avec BeautifulSoup
                    soup = BeautifulSoup(html, 'html.parser')

                    # Trouver tous les éléments <span class='other'> à l'intérieur de la classe "pages"
                    span_elements = soup.select('.pages span.other')

                    # Extraire le contenu texte du dernier élément trouvé
                    if span_elements:
                        dernier_span = span_elements[-1]
                        contenu = dernier_span.get_text()
                    
                    global data_1
                    data_1 = []
                    
                    self.home_frame_button_2_import.configure(state="disabled")

                    self.progress_label.grid(row=4, column=0, padx=20, pady=5)
                    
                    def scrape_and_update_ui():
                        try:
                            for ind in range(1,int(contenu)+1):



                                if ind == 1:
                                    url = url_1
                                else:
                                    nv_ind = (ind-1)*10
                                    url = "https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire?limit=0&startDate="+str(jour_date_debut)+"%2F"+mois_date_debut+"%2F"+str(annee_date_debut)+"&endDate="+str(jour_date_fin)+"%2F"+mois_date_fin+"%2F"+str(annee_date_fin)+"&block=ae14ce1a4ee29af53d5645f51bf0e97d&offset="+str(nv_ind)+"#address-d3239ec6d067cd9381f137545720a6c9-ae14ce1a4ee29af53d5645f51bf0e97d"

                                headers = {
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                                }
                                response = requests.get(url, headers=headers)


                                # Téléchargement du contenu de la page web
                                html_content = response.content

                                # Utilisation de BeautifulSoup pour analyser le contenu HTML
                                soup = BeautifulSoup(html_content, "html.parser")

                                # Recherche de la première table dans le contenu HTML
                                table = soup.find("table")

                                # Parcours des lignes de la table et extraction des données
                                for row_1 in table.find_all("tr"):
                                    cells_1 = row_1.find_all("td")
                                    if len(cells_1) > 0:
                                        date_1 = cells_1[0].get_text().strip()
                                        tmp_1 = cells_1[1].get_text().strip()
                                        data_1.append([date_1, tmp_1])

                                time.sleep(0.21)
                            self.progress_label.grid_forget()

                            headers_1 = ["Date", "TMP"]
                            global df_1
                            df_1 = pd.DataFrame(data_1, columns=headers_1)

                            self.home_frame_button_2_import.configure(state="normal")
                            messagebox.showinfo("Information", "Importation terminé")
                        except Exception as e:
                            self.home_frame_button_2_import.configure(state="normal")
                            self.progress_label.grid_forget()
                            messagebox.showerror("Erreur", "Erreur, Veuillez réessayer !")

                    scraping_thread = threading.Thread(target=scrape_and_update_ui)
                    scraping_thread.start()
                    
                    
                else:
                    if date_1 > date_2:
                        messagebox.showerror("Erreur", "Veuillez entrer les dates exactement, INVERSER LES DATES !")
                    else:
                        messagebox.showerror("Erreur", "La date référence n'est pas dans l'intervalle des dates !")
                    
                    
            else:
                messagebox.showerror("Erreur", "La date référence n'est pas entrer !")
                
        else:
            messagebox.showerror("Erreur", "Veuillez entrer les deux dates !")
                
                
    def affiche_data_ref(self):
        def populate_table(tree, dataframe):
            for row in dataframe.values:
                row_data = [str(item).strip('[]') for item in row]
                tree.insert("", "end", values=row_data)
                    
        top_3 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_3.iconbitmap(icon_path)
        
        columns = df.columns.tolist()
        
        tree = ttk.Treeview(top_3, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
            
        populate_table(tree, df)
        tree.pack(fill="both", expand=True)
        
    def data_zc_actuariel(self):
        import numpy as np
        data_tst_1 = data
        colonnes = ["Date d'échéance","Transaction","Taux","Date de valeur"]
        data_tst = pd.DataFrame(data_tst_1, columns=colonnes)
        last_index = data_tst.index[-1]
        data_tst = data_tst.drop(last_index)
        data_tst['Date d\'échéance'] = pd.to_datetime(data_tst['Date d\'échéance'], format='%d/%m/%Y')
        data_tst['Taux'] = data_tst['Taux'].str.rstrip(' %').str.replace(',', '.').astype(float)
        data_tst['Date de valeur'] = pd.to_datetime(data_tst['Date de valeur'], format='%d/%m/%Y')
        data_tst['Taux'] = data_tst['Taux'].astype(float) / 100
        
        # Convertir les colonnes de date en datetime
        data_tst["Date d'échéance"] = pd.to_datetime(data_tst["Date d'échéance"], dayfirst=True)
        data_tst["Date de valeur"] = pd.to_datetime(data_tst["Date de valeur"], dayfirst=True)

        # Calculer la différence de maturité en jours
        data_tst["Maturité (jours)"] = (data_tst["Date d'échéance"] - data_tst["Date de valeur"]).dt.days
        data_tst["Maturité (annee)"] = (data_tst["Date d'échéance"] - data_tst["Date de valeur"]).dt.days / 365
        # Calculer les taux actuariels
        def calculate_actuarial_rate(row):
            tm = row["Taux"]
            mr = row["Maturité (jours)"]
            if mr >= 365:
                ta = tm
            else:
                ta = ((1 + tm * mr / 360) ** (365 / mr)) - 1
            return ta

        data_tst["Taux Actuariel"] = data_tst.apply(calculate_actuarial_rate, axis=1)

        maturites_jours = data_tst["Maturité (jours)"]
        taux_actuariel = data_tst["Taux Actuariel"]

        # Conversion des maturités en années
        maturites_annees = np.array(maturites_jours) 

        # Création de la fonction d'interpolation linéaire
        interp_function = interp1d(maturites_annees, taux_actuariel, kind='linear')

        # Maturités pour lesquelles vous voulez calculer les taux
        maturites_calcul_jours = [91, 182, 365, 730, 1095, 1460, 1825, 2190, 2555, 2920, 3285, 3650, 4015, 4380, 4745, 5110, 5475, 5840, 6205, 6570, 6935, 7300, 7665, 8030, 8395, 8760]
        maturites_calcul_jours_1 = maturites_calcul_jours
        maturites_calcul_annee = [element / 365 for element in maturites_calcul_jours_1]

        # Calcul des taux interpolés
        taux_interpoles = interp_function(maturites_calcul_jours)

        # Conversion en DataFrame pandas
        data_interp = {'Maturité jours': maturites_calcul_jours,'Maturité annee': maturites_calcul_annee , 'Taux actuariel': taux_interpoles}
        data_interpolation = pd.DataFrame(data_interp)
        
        nouvelle_liste = []

        for index, row in data_interpolation.iterrows():
            r = row["Taux actuariel"]
            n = int(row["Maturité annee"])

            if n <= 1:
                nouvelle_liste.append(r)
            else:
                numerator = 0

                for i in range(2, n+1):
                    numerator += (1 / (1 + r) ** (i-1)) - (1 / (1 + nouvelle_liste[i]) ** (i-1))

                last_term = numerator + (1 / (1 + r) ** n)
                taux_zero_coupon = ((1 / last_term) ** (1 / n)) - 1
                nouvelle_liste.append(taux_zero_coupon)
                
        data_interpolation['Taux zero coupon'] = nouvelle_liste
        
        global data_3
        data_3 = data_interpolation
        def populate_table(tree, dataframe):
            for row in dataframe.values:
                row_data = [str(item).strip('[]') for item in row]
                tree.insert("", "end", values=row_data)
                    
        top_4 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_4.iconbitmap(icon_path)
        
        columns = data_3.columns.tolist()
        
        tree = ttk.Treeview(top_4, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
            
        populate_table(tree, data_3)
        tree.pack(fill="both", expand=True)
        
    
    def courbe_zc(self):
        x = data_3["Maturité jours"]
        y = data_3["Taux zero coupon"]
        
        top_5 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_5.iconbitmap(icon_path)
        
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel('Maturités en jours')
        ax.set_ylabel('Taux ZC')
        ax.set_title('Taux Zero Coupon')

        canvas = FigureCanvasTkAgg(fig, master=top_5)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def courbe_actuariel(self):
        x = data_3["Maturité jours"]
        y = data_3["Taux actuariel"]
        
        top_6 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_6.iconbitmap(icon_path)
        
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel('Maturités en jours')
        ax.set_ylabel('Taux ACT')
        ax.set_title('Taux Actuariel')

        canvas = FigureCanvasTkAgg(fig, master=top_6)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def affiche_backtesting_vas(self):
        import numpy as np
        data_tst_2 = data_1
        colonnes_1 = ["Date","TMP"]
        data_tst_1 = pd.DataFrame(data_tst_2, columns=colonnes_1)
        data_tst_1['TMP'] = data_tst_1['TMP'].str.rstrip(' %').str.replace(',', '.').astype(float)
        data_tst_1['TMP'] = data_tst_1['TMP'].astype(float) / 100
        print(data_tst_1)
        rt_values = data_tst_1["TMP"].values
        rt_values_rev = rt_values[::-1]
        rt_minus_1_values = np.roll(rt_values_rev, -1)

        def vasicek_log_likelihood(params, rt, rt_minus_1):
            a, b, s = params
            n = len(rt_values)

            modified_term = b * (1 - np.exp(-a))

            log_likelihood = -((n-1 ) * np.log(2 * np.pi * s ** 2))/ 2  - 0.5 * np.sum(((rt -  rt_minus_1 * np.exp(-a) - modified_term )) ** 2) / s ** 2

            return -log_likelihood


        # Initial guess for parameters
        initial_params = [1.0, 1.0, -1.0]

        # Run optimization
        result = minimize(vasicek_log_likelihood, initial_params, args=(rt_values_rev, rt_minus_1_values), method='Nelder-Mead')

        estimated_a, estimated_b, estimated_s = result.x
        
        global a_vas
        a_vas = estimated_a
        global b_vas
        b_vas = estimated_b
        global sigma_vas
        sigma_vas = estimated_s
        
        # Paramètres de l'équation
        theta = estimated_b
        k = estimated_a

        # Préparation des données pour le backtesting
        n_days = len(rt_values_rev)
        predictions = [rt_values_rev[0]]  # La première valeur est l'observation initiale

        # Calculer les prédictions en utilisant l'équation de récurrence
        for i in range(1, n_days):
            predicted_value = theta * (1 - np.exp(-k)) + np.exp(-k) * rt_values_rev[i-1]
            predictions.append(predicted_value)
        
        x = df_1["Date"]
        y1 = rt_values_rev
        y2 = predictions
        
        top_7 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_7.iconbitmap(icon_path)

        fig, ax = plt.subplots()
        ax.plot( y1, label='Marché')
        ax.plot( y2, label='Vasicek', color='orange')

        ax.set_xlabel('Temps')
        ax.set_ylabel('Taux')
        ax.set_title('Backtesting')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=top_7)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def courbe_zc_vas(self):
        data_tst_vas = df_1
        data_tst_vas['TMP'] = data_tst_vas['TMP'].str.rstrip(' %').str.replace(',', '.').astype(float)
        data_tst_vas['TMP'] = data_tst_vas['TMP'].astype(float) / 100
        valeur_a_chercher = ref_date
        index = data_tst_vas.index[data_tst_vas['Date'] == valeur_a_chercher].tolist()[0]
        observed_rt = data_tst_vas['TMP'][index]
        a = a_vas
        sigma = sigma_vas

        rt_values = data_3['Taux zero coupon'].values
        
        date_string = ref_date

        date_obj = datetime.strptime(date_string, "%d/%m/%Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")

        # Définition de la fonction d'erreur à minimiser
        def error_function(q):
            b = b_vas - (sigma * q) / a
            t = pd.to_datetime(formatted_date)
            maturities = [91, 182, 364, 730, 1095, 1460, 1825, 2198, 2555, 2920, 3285, 3650, 4015, 4380, 4745, 5110, 5475, 5840, 6205]
            calculated_rates = []

            def calculate_l():
                return b - (sigma ** 2) / (2 * a ** 2)

            def calculate_R(t, T):
                l = calculate_l()
                time_diff_in_years = (T - t).days / 365.0
                exp_term = -a * time_diff_in_years
                R = l + (observed_rt - l) * (1 - math.exp(exp_term)) / (a * time_diff_in_years) + (sigma ** 2) * (1 - math.exp(exp_term)) ** 2 / (time_diff_in_years * 4 * a ** 3)
                return R

            for maturity in maturities:
                T = t + pd.DateOffset(days=maturity)
                zero_coupon_rate = calculate_R(t, T)
                calculated_rates.append(zero_coupon_rate)

            calculated_rates = np.array(calculated_rates)
            squared_error = np.sum((rt_values - calculated_rates) ** 2)
            return squared_error

        # Estimation initiale pour le paramètre q
        initial_q = 1.0

        # Minimisation de la fonction d'erreur
        result = minimize(error_function, initial_q, method='Nelder-Mead')

        # Récupération du paramètre q optimal
        optimal_q = result.x[0]
        
        r_infini = b_vas - optimal_q*sigma_vas/a_vas - (sigma_vas**2) / (2 * a_vas**2)
        a = a_vas
        sigma = sigma_vas
        ob = observed_rt
        b = b_vas
        
        date_string_1 = ref_date

        date_obj_1 = datetime.strptime(date_string_1, "%d/%m/%Y")
        formatted_date_1 = date_obj_1.strftime("%d-%m-%Y")
        
        taux_zc_v_prm = []

        def Calcul_B(T, t):
            time_diff_in_years = (T - t).days / 365
            B = ( sigma**2 * ( 1 - np.exp( - a * time_diff_in_years) )**2 ) / ( 4 * (a**3) * time_diff_in_years )
            return B

        def Calcul_A(T, t):
            time_diff_in_years = (T - t).days / 365
            A = ( ob - r_infini ) * ( ( 1 - np.exp( - a * time_diff_in_years) ) ) / ( a * time_diff_in_years)
            return A

        def Calcul_R(T, t):
            R = r_infini + Calcul_A(T, t) + Calcul_B(T, t)
            return R

        date_str = formatted_date_1
        t = datetime.strptime(date_str, "%d-%m-%Y").date()
        maturite = [91, 182, 364, 730, 1095, 1460, 1825, 2198, 2555, 2920, 3285, 3650, 4015, 4380, 4745, 5110, 5475, 5840, 6205]

        for m in maturite:
            T = t + timedelta(days=m)
            taux_zc_v_prm.append(Calcul_R(T, t))
            
        t_zc_marche = data_3["Taux zero coupon"]
        partie_t_zc_marche = t_zc_marche[:19]
        
        x = maturite
        y1 = partie_t_zc_marche
        y2 = taux_zc_v_prm
        
        top_8 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_8.iconbitmap(icon_path)

        fig, ax = plt.subplots()
        ax.plot(x, y1, label='ZC Marché')
        ax.plot(x, y2, label='ZC AVEC PRIME Vasicek', color='orange')

        ax.set_xlabel('Maturités')
        ax.set_ylabel('Taux ZC')
        ax.set_title('ZC Marché Vs ZC Vasicek')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=top_8)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def affiche_backtesting_cir(self):
        data_tst_3 = data_1
        colonnes_3 = ["Date","TMP"]
        data_tst_3 = pd.DataFrame(data_tst_3, columns=colonnes_3)
        data_tst_3['TMP'] = data_tst_3['TMP'].str.rstrip(' %').str.replace(',', '.').astype(float)
        data_tst_3['TMP'] = data_tst_3['TMP'].astype(float) / 100
        
        rt_values = data_tst_3["TMP"].values

        # Fonction d'erreur à minimiser (somme des carrés des écarts)
        def error_function(params, rt_values):
            a, b = params
            rt_diff = np.diff(rt_values)
            rt_sqrt = np.sqrt(rt_values[:-1])
            error_term = (rt_diff / rt_sqrt) - (a * b / rt_sqrt) + (a * rt_sqrt)
            sum_squared_errors = np.sum(error_term ** 2)
            return sum_squared_errors

        # Estimation initiale des paramètres
        initial_params = [1.0, 1.0]

        # Minimisation de la fonction d'erreur
        result = minimize(error_function, initial_params, args=(rt_values,), method='Nelder-Mead')

        # Récupération des paramètres estimés
        estimated_a, estimated_b = result.x
        rt_diff = np.diff(rt_values)
        rt_sqrt = np.sqrt(rt_values[:-1])
        error_term = (rt_diff / rt_sqrt) - (estimated_a * estimated_b / rt_sqrt) + (estimated_a * rt_sqrt)
        estimated_sigma = np.std(error_term)
        
        valeur_a_chercher = ref_date

        index = data_tst_3.index[data_tst_3['Date'] == valeur_a_chercher].tolist()[0]
        observed_rt = data_tst_3['TMP'][index]
        global observed_rt_cir
        observed_rt_cir = observed_rt
        
        aux = data_3.iloc[0:19]
        global data_zc_marche_17
        data_zc_marche_17 = aux
        
        rt_val = aux["Taux zero coupon"].values
        
        global a_cir
        a_cir = estimated_a
        global b_cir
        b_cir = estimated_b
        global sigma_cir
        sigma_cir = estimated_sigma
        
        sigma = estimated_sigma
        
        date_string_1 = ref_date

        date_obj_1 = datetime.strptime(date_string_1, "%d/%m/%Y")
        formatted_date_1 = date_obj_1.strftime("%Y-%m-%d")

        # Définition de la fonction d'erreur à minimiser
        def error_function(q):
            a=(q*sigma_cir)+a_cir
            b=(b_cir*a_cir)/a
            t = pd.to_datetime(formatted_date_1)
            maturities = [91, 182, 364, 730, 1095, 1460, 1825, 2198, 2555, 2920, 3285, 3650, 4015, 4380, 4745, 5110, 5475, 5840, 6205]
            calculated_rates = []

            def calculate_A0(t, T):
                gamma = math.sqrt((a ** 2) + (2 *(sigma ** 2)))
                time_diff_in_years = (T - t).days / 365.0
                numerator = 2 * gamma * np.exp(((a + gamma) / 2) * time_diff_in_years)
                denominator = 2 * gamma + (a + gamma) * (np.exp(gamma * time_diff_in_years) - 1)
                return numerator / denominator

            def calculate_B(t, T):
                gamma = math.sqrt(a ** 2 + 2 * sigma ** 2)
                time_diff_in_years = (T - t).days / 365.0
                numerator = 2 * (np.exp(gamma * (time_diff_in_years)) - 1)
                denominator = (2 * gamma) + (a + gamma) * (np.exp(gamma * time_diff_in_years) - 1)
                return numerator / denominator

            def calculate_R(t, T):
                time_diff_in_years = (T - t).days / 365.0
                A0 = calculate_A0(t, T)
                B = calculate_B(t, T)
                R = -2 * a * b * np.log(A0) / (sigma ** 2 * time_diff_in_years) + observed_rt / time_diff_in_years * B
                return R

            for maturity in maturities:
                T = t + pd.DateOffset(days=maturity)
                zero_coupon_rate = calculate_R(t, T)
                calculated_rates.append(zero_coupon_rate)

            calculated_rates = np.array(calculated_rates)
            squared_error = np.sum((rt_val - calculated_rates) ** 2)
            return squared_error

        # Estimation initiale pour le paramètre q
        initial_q = 1.0

        # Minimisation de la fonction d'erreur
        result = minimize(error_function, initial_q, method='Nelder-Mead')

        # Récupération du paramètre q optimal
        optimal_q = result.x[0]
        
        global q_cir
        q_cir = optimal_q
        
        # Paramètres de l'équation
        theta = estimated_b
        k = estimated_a
        
        rt_values_rev = rt_values[::-1]

        # Préparation des données pour le backtesting
        n_days = len(rt_values_rev)
        predictions = [rt_values_rev[0]]  # La première valeur est l'observation initiale

        # Calculer les prédictions en utilisant l'équation de récurrence
        for i in range(1, n_days):
            predicted_value = k * (theta - rt_values_rev[i-1]) + rt_values_rev[i-1]
            predictions.append(predicted_value)
        
        x = df_1["Date"]
        y1 = rt_values_rev
        y2 = predictions
        
        top_8 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_8.iconbitmap(icon_path)

        fig, ax = plt.subplots()
        ax.plot( y1, label='Marché')
        ax.plot( y2, label='CIR', color='orange')

        ax.set_xlabel('Temps')
        ax.set_ylabel('Taux')
        ax.set_title('Backtesting')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=top_8)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def courbe_zc_cir(self):
        observed_rt = observed_rt_cir

        q = q_cir
        a=(q*sigma_cir)+a_cir
        b=(b_cir*a_cir)/a

        sigma = sigma_cir

        def calculate_A0(t, T):
            gamma = math.sqrt(a ** 2 + 2 * sigma ** 2)
            time_diff_in_years = (T - t).days / 365.0
            numerator = 2 * gamma * np.exp((((a + gamma) / 2)) * time_diff_in_years)
            denominator = 2 * gamma + (a + gamma) * (np.exp(gamma * time_diff_in_years) - 1)
            return numerator / denominator

        def calculate_B(t, T):
            gamma = math.sqrt(a ** 2 + 2 * sigma ** 2)
            time_diff_in_years = (T - t).days / 365.0
            numerator = 2 * (np.exp(gamma * time_diff_in_years) - 1)
            denominator = 2 * gamma + (a + gamma) * (np.exp(gamma * time_diff_in_years) - 1)
            return numerator / denominator

        def calculate_R(t, T):
            time_diff_in_years = (T - t).days / 365.0
            A0 = calculate_A0(t, T)
            B = calculate_B(t, T)
            R = -2 * a * b * np.log(A0) / (sigma ** 2 * time_diff_in_years) + (observed_rt*B) / time_diff_in_years
            return R

        ddd = []
        
        date_string_1 = ref_date

        date_obj_1 = datetime.strptime(date_string_1, "%d/%m/%Y")
        formatted_date_1 = date_obj_1.strftime("%Y-%m-%d")
        
        t = pd.to_datetime(formatted_date_1)
        maturities = [91, 182, 364, 730, 1095, 1460, 1825, 2198, 2555, 2920, 3285, 3650, 4015, 4380, 4745, 5110, 5475, 5840, 6205]

        for maturity in maturities:
            T = t + pd.DateOffset(days=maturity)
            zero_coupon_rate = calculate_R(t, T)
            ddd.append(zero_coupon_rate)
        
        t_zc_marche = data_zc_marche_17["Taux zero coupon"]
        
        x = maturities
        y1 = t_zc_marche
        y2 = ddd
        
        top_9 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_9.iconbitmap(icon_path)

        fig, ax = plt.subplots()
        ax.plot(x, y1, label='ZC Marché')
        ax.plot(x, y2, label='ZC AVEC PRIME CIR', color='orange')

        ax.set_xlabel('Maturités')
        ax.set_ylabel('Taux ZC')
        ax.set_title('ZC Marché Vs ZC CIR')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=top_9)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def open_calendar_3(self):
        def set_selected_date_1_zc():
            selected_date_debut_zc = cal_1_zc.selection_get().strftime('%d/%m/%Y')
            self.var_debut_zc.set(selected_date_debut_zc)
            top_10.destroy()

        top_10 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_10.iconbitmap(icon_path)

        import datetime
        today = datetime.date.today()

        mindate = datetime.date(year=2001, month=1, day=1)
        maxdate = today + datetime.timedelta(days=5)

        cal_1_zc = Calendar(top_10, font="Arial 12 bold", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1")
        cal_1_zc.pack(fill="both", expand=True)

        ttk.Button(top_10, text="OK", command=set_selected_date_1_zc).pack()
        
    def open_calendar_4(self):
        def set_selected_date_2_zc():
            selected_date_fin_zc = cal_2_zc.selection_get().strftime('%d/%m/%Y')
            self.var_fin_zc.set(selected_date_fin_zc)
            top_11.destroy()

        top_11 = tk.Toplevel(self)
        icon_path = "icon_app_test_1.ico"
        top_11.iconbitmap(icon_path)

        import datetime
        today = datetime.date.today()

        mindate = datetime.date(year=2001, month=1, day=1)
        maxdate = today + datetime.timedelta(days=5)

        cal_2_zc = Calendar(top_11, font="Arial 12 bold", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1")
        cal_2_zc.pack(fill="both", expand=True)

        ttk.Button(top_11, text="OK", command=set_selected_date_2_zc).pack()
        
        
    def affiche_zc_dates(self):
        
        entered_text_1_zc = self.var_debut_zc.get()
        entered_text_2_zc = self.var_fin_zc.get()
        
        if entered_text_1_zc and entered_text_2_zc:
            
            date_debut_zc = datetime.strptime(entered_text_1_zc, '%d/%m/%Y')
            date_fin_zc = datetime.strptime(entered_text_2_zc, '%d/%m/%Y')
            
            if date_debut_zc < date_fin_zc:
                
                
                def calculer_taux_zero_coupon(table):

                   if table is not None and not table.empty:
                    if len(table) > 0:
                       table = table.iloc[:-1]

                    # Convertir les colonnes de date en datetime
                    table["Date d'échéance"] = pd.to_datetime(table["Date d'échéance"], dayfirst=True)
                    table["Date de valeur"] = pd.to_datetime(table["Date de valeur"], dayfirst=True)
                    # Conversion du type de données de la colonne "Taux" si nécessaire
                    if table["Taux"].dtype == 'object':
                        table["Taux"] = table["Taux"].str.replace(',', '.').str.rstrip('%').astype(float) / 100

                # Convertir les colonnes de date en datetime
                    table["Date d'échéance"] = pd.to_datetime(table["Date d'échéance"], dayfirst=True)
                    table["Date de valeur"] = pd.to_datetime(table["Date de valeur"], dayfirst=True)

                # Calculer la différence de maturité en jours
                    table["Maturité (jours)"] = (table["Date d'échéance"] - table["Date de valeur"]).dt.days
                    table["Maturité (anne)"] = (table["Date d'échéance"] - table["Date de valeur"]).dt.days / 365
                # Calculer les taux actuariels
                    
                    def calculate_actuarial_rate(row):
                        tm = row["Taux"]
                        mr = row["Maturité (jours)"]
                        if mr >= 365:
                            ta = tm
                        else:
                            ta = ((1 + tm * mr / 360) ** (365 / mr)) - 1
                        return ta

                    table["Taux Actuariel"] = table.apply(calculate_actuarial_rate, axis=1)

                    # Interpolation linéaire

                    interp_function = interp1d(table["Maturité (jours)"], table["Taux Actuariel"], kind='linear')

                    # Maturités pour lesquelles vous voulez calculer les taux zéro coupon
                    maturites_calcul_jours = [91, 182, 365, 730, 1095, 1460, 1825, 2190, 2555, 2920, 3285, 3650, 4015, 4380, 4745, 5110, 5475, 5840, 6205, 6570, 6935, 7300, 7665, 8030, 8395, 8760, 9125]

                    # Calcul des taux zéro coupon
                    taux_interpoles = interp_function(maturites_calcul_jours)
                    taux_interpoles=taux_interpoles.tolist()

                    data = {'Maturité (jours)': maturites_calcul_jours, 'Taux actuariel': taux_interpoles}
                    df_taux_zc = pd.DataFrame(data)

                    ZC=[]
                    ZC = taux_interpoles[:3]

                    for N in range(2,26):
                        rN = taux_interpoles[N+1]
                        sum_term = 0

                        if ZC[0] != 0:
                            for i in range(1,N):
                                sum_term = sum_term + (1 / (1 + rN) ** (i)) - (1 / (1 + ZC[i+1]) ** (i))

                        terme = 1 / ((1 + rN) ** (N))
                        ZCC = (sum_term + terme)
                        ZCN = 1 / ZCC
                        ZCN1 = ZCN ** (1/(N))
                        ZCN3 = ZCN1 - 1
                        ZC.append(ZCN3)
                    df_taux_zc["Taux zéro coupon"] = ZC

                    return df_taux_zc

                dates_extraction = []

                tables_taux_zc = []
                data_dict = {}

                jour_date_debut_zc = date_debut_zc.day
                mois_date_debut_zc_tst = date_debut_zc.month
                mois_date_debut_zc = "{:02d}".format(mois_date_debut_zc_tst)
                annee_date_debut_zc = date_debut_zc.year

                jour_date_fin_zc = date_fin_zc.day
                mois_date_fin_zc_tst = date_fin_zc.month
                mois_date_fin_zc = "{:02d}".format(mois_date_fin_zc_tst)
                annee_date_fin_zc = date_fin_zc.year
                
                self.fifth_frame_button_1.configure(state="disabled")

                self.progress_label_zc.grid(row=5, column=0, padx=20, pady=5)

                tables_taux_zc = []
                data_dict = {}

                def scrape_and_update_ui_zc():
                        try:
                            date_debut = datetime(annee_date_debut_zc, int(mois_date_debut_zc), jour_date_debut_zc)
                            date_fin = datetime(annee_date_fin_zc, int(mois_date_fin_zc), jour_date_fin_zc)
                            
                            while date_debut <= date_fin:
                                # Formattez la date pour l'URL
                                date_formattee = date_debut.strftime("%d/%m/%Y")

                                url = f"https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-secondaire/Taux-de-reference-des-bons-du-tresor?date={date_formattee}&block=e1d6b9bbf87f86f8ba53e8518e882982#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982"

                                # Téléchargement du contenu de la page web
                                response = requests.get(url)
                                html_content = response.content

                                # Utilisation de BeautifulSoup pour analyser le contenu HTML
                                soup = BeautifulSoup(html_content, "html.parser")

                                # Recherche de toutes les tables sur la page
                                tables = soup.find_all("table")

                                
                                if tables:
                                    
                                    data = []

                                    for row in tables[0].find_all("tr"):
                                        cells = row.find_all("td")
                                        if len(cells) > 0:
                                            date_echeance = cells[0].get_text().strip()
                                            transaction = cells[1].get_text().strip()
                                            taux = cells[2].get_text().strip()
                                            date_valeur = cells[3].get_text().strip()
                                            data.append([date_echeance, transaction, taux, date_valeur])

                                    headers = ["Date d'échéance", "Transaction", "Taux", "Date de valeur"]
                                    df_table = pd.DataFrame(data, columns=headers)

                                    if not df_table.empty:
                                        df_taux_zero_coupon = calculer_taux_zero_coupon(df_table)

                                        # Ajoutez les taux zéro coupon au dictionnaire avec la date comme clé
                                        data_dict[date_debut.strftime('%Y-%m-%d')] = df_taux_zero_coupon['Taux zéro coupon'].tolist()

                                # Incrémentation de la date de début pour passer à la date suivante
                                date_debut += timedelta(days=1)
                            
                            self.progress_label_zc.grid_forget()
                            self.fifth_frame_button_1.configure(state="normal")
                            
                            df_contingence = pd.DataFrame.from_dict(data_dict, orient='index', columns=[91, 182, 365, 730, 1095, 1460, 1825, 2190, 2555, 2920, 3285, 3650, 4015, 4380, 4745, 5110, 5475, 5840, 6205, 6570, 6935, 7300, 7665, 8030, 8395, 8760, 9125])

                            # Renommez les colonnes
                            df_contingence.columns = df_contingence.columns.rename(None)

                            # Transposez le dataframe pour avoir les maturités en colonnes et les dates en lignes
                            df_contingence = df_contingence.T

                            data_4 = df_contingence

                            top_12 = tk.Toplevel(self)
                            icon_path = "icon_app_test_1.ico"
                            top_12.iconbitmap(icon_path)

                            columns = ['Maturités'] + df_contingence.columns.tolist()
                            tree = ttk.Treeview(top_12, columns=columns, show="headings")

                            # Configurez les en-têtes de colonne
                            for col in columns:
                                tree.heading(col, text=col)
                                tree.column(col, width=100, anchor="center")

                            for index, row in df_contingence.iterrows():
                                row_data = [index] + [str(item).strip('[]') for item in row]
                                tree.insert("", "end", values=row_data)

                            tree.pack(fill="both", expand=True)
                            
                        except Exception as e:
                            self.fifth_frame_button_1.configure(state="normal")
                            self.progress_label_zc.grid_forget()
                            messagebox.showerror("Erreur", "Erreur, veuillez réessayer !")
                            
                scraping_thread = threading.Thread(target=scrape_and_update_ui_zc)
                scraping_thread.start()
                
            else:
                messagebox.showerror("Erreur", "Veuillez entrer les dates exactement, INVERSER LES DATES !")
                
        else:
            messagebox.showerror("showerror", "Veuillez entrer les deux dates !")
        
        
           

if __name__ == "__main__":
    app = App()
    app.mainloop()

