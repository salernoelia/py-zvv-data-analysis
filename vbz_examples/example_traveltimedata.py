import os
import pandas as pd

wd = os.chdir("*\\01_Daten\\01_Input\\")

haltepunkt = pd.read_csv("haltepunkt.csv")
haltestelle = pd.read_csv("haltestelle.csv")

fahrz = pd.read_csv('fahrzeiten_soll_ist_20200809_20200815.csv')

fahrz_haltepkt_from = pd.merge(fahrz,haltepunkt,how="left",
                         left_on=["halt_punkt_id_von","halt_punkt_diva_von","halt_id_von"],
                         right_on=["halt_punkt_id","halt_punkt_diva","halt_id"])

fahrz_haltepkt_from.rename(columns={'GPS_Latitude': 'GPS_Latitude_von', 'GPS_Longitude': 'GPS_Longitude_von',
                               'GPS_Bearing': 'GPS_Bearing_von', 'halt_punkt_ist_aktiv': 'halt_punkt_ist_aktiv_von'},
                      inplace=True)

fahrz_haltepkt = pd.merge(fahrz_haltepkt_from,haltepunkt,how="left",
                         left_on=["halt_punkt_id_nach","halt_punkt_diva_nach","halt_id_nach"],
                         right_on=["halt_punkt_id","halt_punkt_diva","halt_id"])

fahrz_haltepkt.rename(columns={'GPS_Latitude': 'GPS_Latitude_nach', 'GPS_Longitude': 'GPS_Longitude_nach',
                               'GPS_Bearing': 'GPS_Bearing_nach', 'halt_punkt_ist_aktiv': 'halt_punkt_ist_aktiv_nach'},
                      inplace=True)

fahrz_haltepkt_haltestelle_from = pd.merge(fahrz_haltepkt,haltestelle,how="left",
                         left_on=["halt_id_von","halt_diva_von","halt_kurz_von1"],
                         right_on=["halt_id","halt_diva","halt_kurz"])

fahrz_haltepkt_haltestelle_from.rename(columns={'halt_lang': 'halt_lang_von', 'halt_ist_aktiv': 'halt_ist_aktiv_von'},
                      inplace=True)

fahrz_haltepkt_haltestelle = pd.merge(fahrz_haltepkt_haltestelle_from,haltestelle,how="left",
                         left_on=["halt_id_nach","halt_diva_nach","halt_kurz_nach1"],
                         right_on=["halt_id","halt_diva","halt_kurz"])

fahrz_haltepkt_haltestelle.rename(columns={'halt_lang': 'halt_lang_nach', 'halt_ist_aktiv': 'halt_ist_aktiv_nach'},
                      inplace=True)

fahrz_haltepkt_haltestelle['punct_cat'] = fahrz_haltepkt_haltestelle.apply(lambda x:
                                            'delay' if x["ist_an_nach1"] - x["soll_an_nach"] >= 120 else 'too early'
                                            if x["ist_ab_nach"] - x["soll_ab_nach"]<= -60 else "punctual", axis=1)

count_punct_cat = fahrz_haltepkt_haltestelle.groupby(['linie', 'punct_cat']).size().rename('count')

percent_punct = 100 * (count_punct_cat / count_punct_cat.groupby(level=0).sum())

punctuality = percent_punct.to_frame(name='percent')

punctuality = pd.merge(count_punct_cat,punctuality,how="left",
                         left_on=["linie","punct_cat"],
                         right_on=["linie","punct_cat"])





