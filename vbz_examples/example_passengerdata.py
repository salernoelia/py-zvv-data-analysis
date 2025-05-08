import os
import pandas as pd

pd.options.display.float_format = '{:.4f}'.format

HALTESTELLEN = pd.read_csv("../datasets/fahrgastzahlen_2023_ogd/HALTESTELLEN.csv", sep=";")
TAGTYP = pd.read_csv("../datasets/fahrgastzahlen_2023_ogd/TAGTYP.csv", sep=";")
LINIE = pd.read_csv("../datasets/fahrgastzahlen_2023_ogd/LINIE.csv", sep=";")
GEFAESSGROESSE = pd.read_csv("../datasets/fahrgastzahlen_2023_ogd/GEFAESSGROESSE.csv", sep=";")

REISENDE = pd.read_csv("../datasets/fahrgastzahlen_2023_ogd/REISENDE.csv", sep=";")

REISENDE = REISENDE.drop('Linienname', axis=1)

reisende_haltestellen = pd.merge(REISENDE,HALTESTELLEN,how="left",
                         left_on=["Haltestellen_Id"],
                         right_on=["Haltestellen_Id"])

reisende_haltestellen_tagtyp = pd.merge(reisende_haltestellen,TAGTYP,how="left",
                         left_on=["Tagtyp_Id"],
                         right_on=["Tagtyp_Id"])

reisende_haltestellen_tagtyp_linie = pd.merge(reisende_haltestellen_tagtyp,LINIE,how="left",
                         left_on=["Linien_Id"],
                         right_on=["Linien_Id"])

reisende_full = pd.merge(reisende_haltestellen_tagtyp_linie,GEFAESSGROESSE,how="left",
                         left_on=["Plan_Fahrt_Id"],
                         right_on=["Plan_Fahrt_Id"])

pax_line_year = pd.DataFrame({'pax_per_year': [reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"]) \
                [['Einsteiger','Tage_DTV']].prod(axis=1).sum()]}).reset_index().round(0)

einsteiger_tage_dtv = reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"]) \
        [['Einsteiger','Tage_DTV']].prod(axis=1).div(365).sum(level=[0,1,2]).reset_index(name='pax_per_DTV').round(0)

einsteiger_tage_dwv = reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"]) \
        [['Einsteiger','Tage_DWV']].prod(axis=1).div(251).sum(level=[0,1,2]).reset_index(name='pax_per_DWV').round(0)

einsteiger_tage_sa = reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"]) \
            [['Einsteiger','Tage_SA']].prod(axis=1).div(52).sum(level=[0,1,2]).reset_index(name='pax_per_Sa').round(0)

einsteiger_tage_so = reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"]) \
            [['Einsteiger','Tage_SO']].prod(axis=1).div(62).sum(level=[0,1,2]).reset_index(name='pax_per_So').round(0)


einsteiger_tage_sa_n = reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"]) \
        [['Einsteiger','Tage_SA_N']].prod(axis=1).div(52).sum(level=[0,1,2]).reset_index(name='pax_per_Sa_N').round(0)

einsteiger_tage_so_n = reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"]) \
        [['Einsteiger','Tage_SO_N']].prod(axis=1).div(52).sum(level=[0,1,2]).reset_index(name='pax_per_So_N').round(0)

pax_line_year_day_type = [df.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"]) \
                        for df in [einsteiger_tage_dtv, einsteiger_tage_dwv, einsteiger_tage_sa, einsteiger_tage_so, \
                                   einsteiger_tage_sa_n, einsteiger_tage_so_n]]

pax_line_year_day_type = pd.concat(pax_line_year_day_type, axis=1).reset_index()

pax_stop_year = reisende_full.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]) \
                [['Einsteiger','Tage_DTV']].prod(axis=1).sum(level=[0,1,2]).reset_index(name='pax_per_year').round(0)

einsteiger_stops_tage_dtv = reisende_full.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]) \
        [['Einsteiger','Tage_DTV']].prod(axis=1).div(365).sum(level=[0,1,2]).reset_index(name='pax_per_DTV').round(0)

einsteiger_stops_tage_dwv = reisende_full.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]) \
        [['Einsteiger','Tage_DWV']].prod(axis=1).div(251).sum(level=[0,1,2]).reset_index(name='pax_per_DWV').round(0)

einsteiger_stops_tage_sa = reisende_full.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]) \
            [['Einsteiger','Tage_SA']].prod(axis=1).div(52).sum(level=[0,1,2]).reset_index(name='pax_per_Sa').round(0)

einsteiger_stops_tage_so = reisende_full.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]) \
            [['Einsteiger','Tage_SO']].prod(axis=1).div(62).sum(level=[0,1,2]).reset_index(name='pax_per_So').round(0)


einsteiger_stops_tage_sa_n = reisende_full.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"])\
        [['Einsteiger','Tage_SA_N']].prod(axis=1).div(52).sum(level=[0,1,2]).reset_index(name='pax_per_Sa_N').round(0)

einsteiger_stops_tage_so_n = reisende_full.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"])\
        [['Einsteiger','Tage_SO_N']].prod(axis=1).div(52).sum(level=[0,1,2]).reset_index(name='pax_per_So_N').round(0)

pax_stops_year_day_type = [df.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]) for df in \
[einsteiger_stops_tage_dtv, einsteiger_stops_tage_dwv, einsteiger_stops_tage_sa, einsteiger_stops_tage_so, \
 einsteiger_stops_tage_sa_n, einsteiger_stops_tage_so_n]]

pax_stops_year_day_type = pd.concat(pax_stops_year_day_type, axis=1).reset_index()


