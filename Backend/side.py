# car_scraper.py (Modified to use direct URLs)
import time
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from database import CarDatabase
import datetime

class CarScraper:
    def __init__(self):
        self.db = CarDatabase()
        self.base_url = "https://www.cardekho.com"
        self.spec_urls = [
            # Your provided URLs with "#specification" appended,
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_Visia.htm",
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_Visia_Plus.htm",
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_Visia_AMT.htm",
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_N_Connecta.htm",
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_Tekna_Plus_AMT.htm",
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_Visia.htm",
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_Visia_Plus.htm",
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_Tekna_Plus_AMT.htm",
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_N_Connecta.htm",
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_Tekna.htm",
            "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_N_Connecta_AMT.htm",
           "https://www.cardekho.com/overview/Nissan_Magnite/Nissan_Magnite_N_Connecta_Turbo.htm",
            "https://www.cardekho.com/overview/Honda_Amaze/Honda_Amaze_V.htm",
            "https://www.cardekho.com/overview/Honda_Amaze/Honda_Amaze_VX.htm",
            "https://www.cardekho.com/overview/Honda_Amaze/Honda_Amaze_V_CVT.htm",
            "https://www.cardekho.com/overview/Honda_Amaze/Honda_Amaze_ZX.htm",
           "https://www.cardekho.com/overview/Honda_Amaze/Honda_Amaze_VX_CVT.htm",
            "https://www.cardekho.com/overview/Honda_Amaze/Honda_Amaze_ZX_CVT.htm",
            "https://www.cardekho.com/overview/MG_Comet_EV/MG_Comet_EV_Executive.htm",
            "https://www.cardekho.com/overview/MG_Comet_EV/MG_Comet_EV_Excite.htm",
            "https://www.cardekho.com/overview/MG_Comet_EV/MG_Comet_EV_Excite_FC.htm",
            "https://www.cardekho.com/overview/MG_Comet_EV/MG_Comet_EV_Exclusive_FC.htm",
            "https://www.cardekho.com/overview/MG_Comet_EV/MG_Comet_EV_Blackstorm_Edition.htm",
            "https://www.cardekho.com/overview/MG_Comet_EV/MG_Comet_EV_100_Year_Limited_Edition.htm",
            "https://www.cardekho.com/overview/Toyota_Glanza/Toyota_Glanza_E.htm",
            "https://www.cardekho.com/overview/Toyota_Glanza/Toyota_Glanza_S_AMT.htm",
            "https://www.cardekho.com/overview/Toyota_Glanza/Toyota_Glanza_S_CNG.htm",
            "https://www.cardekho.com/overview/Toyota_Glanza/Toyota_Glanza_G.htm",
            "https://www.cardekho.com/overview/Toyota_Glanza/Toyota_Glanza_V.htm",
            "https://www.cardekho.com/overview/Maruti_Eeco/Maruti_Eeco_7_Seater_STD.htm",
            "https://www.cardekho.com/overview/Toyota_Glanza/Toyota_Glanza_V.htm",
            "https://www.cardekho.com/overview/Toyota_Glanza/Toyota_Glanza_V_AMT.htm",
            "https://www.cardekho.com/overview/Maruti_Celerio/Maruti_Celerio_LXI.htm",
            "https://www.cardekho.com/overview/Maruti_Celerio/Maruti_Celerio_VXI.htm",
            "https://www.cardekho.com/overview/Maruti_Celerio/Maruti_Celerio_VXI_AMT.htm",
            "https://www.cardekho.com/overview/Maruti_Celerio/Maruti_Celerio_ZXI_Plus.htm",
            "https://www.cardekho.com/overview/Maruti_Celerio/Maruti_Celerio_ZXI_AMT.htm",
            "https://www.cardekho.com/overview/Maruti_Celerio/Maruti_Celerio_VXI_CNG.htm",
            "https://www.cardekho.com/overview/Maruti_Celerio/Maruti_Celerio_ZXI_Plus_AMT.htm",
            "https://www.cardekho.com/overview/Renault_Triber/Renault_Triber_RXE.htm",
            "https://www.cardekho.com/overview/Renault_Triber/Renault_Triber_RXE_CNG.htm",
            "https://www.cardekho.com/overview/Renault_Triber/Renault_Triber_RXL_CNG.htm",
            "https://www.cardekho.com/overview/Renault_Triber/Renault_Triber_RXT.htm",
            "https://www.cardekho.com/overview/Renault_Triber/Renault_Triber_RXZ_Dual_Tone.htm",
            "https://www.cardekho.com/overview/Renault_Triber/Renault_Triber_RXT_CNG.htm",
            "https://www.cardekho.com/overview/Honda_Amaze_2nd_Gen/Honda_Amaze_2nd_Gen_S_CVT.htmhttps://www.cardekho.com/overview/Honda_Amaze_2nd_Gen/Honda_Amaze_2nd_Gen_VX_Elite.htm",
            "https://www.cardekho.com/overview/Renault_Triber/Renault_Triber_RXT_CNG.htm",
            "https://www.cardekho.com/overview/Renault_Triber/Renault_Triber_RXZ_EASY-R_AMT.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_E.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_S.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_E_CNG.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_E_CNG.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_S_AMT.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_S_Plus_AMT.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_G_Turbo.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_V_Turbo_Dual_Tone.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_G_Turbo_AT.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_V_Turbo_AT_Dual_Tone.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Smart.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Smart_Plus.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Adventure.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Empowered.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Adventure_LR.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Empowered_Plus.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Adventure_LR_AC_FC.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Adventure_S_LR_AC_FC.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Empowered_LR_AC_FC.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Empowered_Plus_LR_AC_FC.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Empowered_Plus_S_LR_AC_FC.htm",
            "https://www.cardekho.com/overview/Tata_Tiago_EV/Tata_Tiago_EV_XE_MR.htm",
            "https://www.cardekho.com/overview/Tata_Tiago_EV/Tata_Tiago_EV_XT_MR.htm",
            "https://www.cardekho.com/overview/Renault_Kiger/Renault_Kiger_RXE.htm",
            "https://www.cardekho.com/overview/Renault_Kiger/Renault_Kiger_RXE_CNG.htm",
            "https://www.cardekho.com/overview/Renault_Kiger/Renault_Kiger_RXL_CNG.htm",
            "https://www.cardekho.com/overview/Renault_Kiger/Renault_Kiger_RXT_Opt_DT.htm",
            "https://www.cardekho.com/overview/Renault_Kiger/Renault_Kiger_RXT_Opt_CNG.htm",
            "https://www.cardekho.com/overview/Renault_Kiger/Renault_Kiger_RXZ_Turbo.htm",
            "https://www.cardekho.com/overview/Mahindra_Bolero_Neo/Mahindra_Bolero_Neo_N4.htm",
           "https://www.cardekho.com/overview/Tata_Tigor/Tata_Tigor_XM.htm",
            "https://www.cardekho.com/overview/Tata_Tigor/Tata_Tigor_XZ.htm",
            "https://www.cardekho.com/overview/Tata_Tigor/Tata_Tigor_XT_CNG.htm",
            "https://www.cardekho.com/overview/Tata_Tigor/Tata_Tigor_XZ_Plus_Lux.htm",
            "https://www.cardekho.com/overview/Tata_Tigor/Tata_Tigor_XZ_Plus_CNG.htm",
            "https://www.cardekho.com/overview/Maruti_Ciaz/Maruti_Ciaz_Sigma.htm",
            "https://www.cardekho.com/overview/Maruti_Ciaz/Maruti_Ciaz_Delta.htm",
            "https://www.cardekho.com/overview/Maruti_Ciaz/Maruti_Ciaz_Alpha.htm",
            "https://www.cardekho.com/overview/Mahindra_Bolero_Pik_Up_Extra_Long/Mahindra_Bolero_Pik_Up_Extra_Long_1.3_T_CBC_MS.htm",
            "https://www.cardekho.com/overview/Citroen_C3/Citroen_C3_Puretech_82_Live.htm",
            "https://www.cardekho.com/overview/Citroen_C3/Citroen_C3_Puretech_82_Feel.htm",
            "https://www.cardekho.com/overview/Citroen_C3/Citroen_C3_Puretech_82_Shine_DT.htm",
            "https://www.cardekho.com/overview/Citroen_C3/Citroen_C3_Shine_Dark_Edition.htm",
            "https://www.cardekho.com/overview/Citroen_C3/Citroen_C3_Shine_Turbo_Dark_Edition.htm",
            "https://www.cardekho.com/overview/Tata_Altroz_Racer/Tata_Altroz_Racer_R1.htm",
            "https://www.cardekho.com/overview/Citroen_Basalt/Citroen_Basalt_You.htm",
            "https://www.cardekho.com/overview/Citroen_Basalt/Citroen_Basalt_Plus.htm",
            "https://www.cardekho.com/overview/Maruti_Super_Carry/Maruti_Super_Carry_Cab_Chassis.htm",
            "https://www.cardekho.com/overview/Maruti_Super_Carry/Maruti_Super_Carry_STD.htm",
            "https://www.cardekho.com/overview/Maruti_Super_Carry/Maruti_Super_Carry_STD_CNG.htm",
            "https://www.cardekho.com/overview/Maruti_Dzire_Tour_S/Maruti_Dzire_Tour_S_STD.htm",
            "https://www.cardekho.com/overview/Maruti_Dzire_Tour_S/Maruti_Dzire_Tour_S_CNG.htm",
            "https://www.cardekho.com/overview/Mahindra_Bolero_Maxi_Truck_Plus/Mahindra_Bolero_Maxi_Truck_Plus_CBC_PS_1.2.htm",
            "https://www.cardekho.com/overview/Mahindra_Bolero_Maxi_Truck_Plus/Mahindra_Bolero_Maxi_Truck_Plus_1.2.htm",
            "https://www.cardekho.com/overview/Mahindra_Bolero_Maxi_Truck_Plus/Mahindra_Bolero_Maxi_Truck_Plus_CNG_PS.htm",
           "https://www.cardekho.com/overview/Tata_Yodha_Pickup/Tata_Yodha_Pickup_Eco.htm",
            "https://www.cardekho.com/overview/Tata_Yodha_Pickup/Tata_Yodha_Pickup_4x4.htm",
            "https://www.cardekho.com/overview/Maruti_Ertiga_Tour/Maruti_Ertiga_Tour_STD.htm",
            "https://www.cardekho.com/overview/Honda_Amaze_2nd_Gen/Honda_Amaze_2nd_Gen_E.htm"
            "https://www.cardekho.com/overview/Honda_Amaze_2nd_Gen/Honda_Amaze_2nd_Gen_VX_Elite_CVT.htm",
            "https://www.cardekho.com/overview/Mahindra_BOLERO_PIK_UP_Extra_Strong/Mahindra_BOLERO_PIK_UP_Extra_Strong_CBC_1.3T_MS.htm",
            "https://www.cardekho.com/overview/Mahindra_BOLERO_PIK_UP_Extra_Strong/Mahindra_BOLERO_PIK_UP_Extra_Strong_CBC_4WD_PS.htm",
            "https://www.cardekho.com/overview/Maruti_Wagon_R_tour/Maruti_Wagon_R_tour_H3_PETROL.htm",
            "https://www.cardekho.com/overview/Maruti_Wagon_R_tour/Maruti_Wagon_R_tour_H3_CNG.htm",
            "https://www.cardekho.com/overview/Hyundai_i20_N-Line/Hyundai_i20_N-Line_N6.htm",
            "https://www.cardekho.com/overview/Hyundai_i20_N-Line/Hyundai_i20_N-Line_N6_Dual_Tone.htm",
            "https://www.cardekho.com/overview/Maruti_Eeco_Cargo/Maruti_Eeco_Cargo_STD.htm",
            "https://www.cardekho.com/overview/Maruti_Eeco_Cargo/Maruti_Eeco_Cargo_STD_CNG.htm",
            "https://www.cardekho.com/overview/Maruti_Eeco_Cargo/Maruti_Eeco_Cargo_STD_AC_CNG.htm",
            "https://www.cardekho.com/overview/MG_Windsor_EV/MG_Windsor_EV_Excite.htm",
            "https://www.cardekho.com/overview/MG_Windsor_EV/MG_Windsor_EV_Exclusive.htm",
            "https://www.cardekho.com/overview/Honda_City/Honda_City_SV.htm",
            "https://www.cardekho.com/overview/Honda_City/Honda_City_SV_Reinforced.htm",
            "https://www.cardekho.com/overview/Honda_City/Honda_City_V_Elegant.htm",
            "https://www.cardekho.com/overview/Honda_City/Honda_City_V_Reinforced.htm",
            "https://www.cardekho.com/overview/Honda_City/Honda_City_V_Reinforced.htm",
            "https://www.cardekho.com/overview/Honda_City/Honda_City_V_Elegant_CVT.htm",
            "https://www.cardekho.com/overview/Honda_City/Honda_City_VX_Apex_Edition.htm",
            "https://www.cardekho.com/overview/Honda_City/Honda_City_V_Apex_Edition_CVT.htm",
            "https://www.cardekho.com/overview/Honda_Amaze/Honda_Amaze_VX_CVT.htm",
            "https://www.cardekho.com/overview/Hyundai_Alcazar/Hyundai_Alcazar_Executive.htm",
            "https://www.cardekho.com/overview/Skoda_Kushaq/Skoda_Kushaq_1.0L_Classic.htm",
            "https://www.cardekho.com/overview/Skoda_Kushaq/Skoda_Kushaq_1.0L_Onyx_AT.htm",
            "https://www.cardekho.com/overview/Skoda_Kushaq/Skoda_Kushaq_1.0L_Signature.htm",
            "https://www.cardekho.com/overview/Skoda_Kushaq/Skoda_Kushaq_1.0L_Signature.htm",
            "https://www.cardekho.com/overview/Skoda_Kushaq/Skoda_Kushaq_1.0L_Sportline.htm",
            "https://www.cardekho.com/overview/Maruti_XL6/Maruti_XL6_Zeta.htm",
            "https://www.cardekho.com/overview/Maruti_XL6/Maruti_XL6_Zeta_CNG.htm",
            "https://www.cardekho.com/overview/Maruti_XL6/Maruti_XL6_Zeta_AT.htm",
            "https://www.cardekho.com/overview/Maruti_XL6/Maruti_XL6_Alpha_Plus_Dual_Tone.htm",
            "https://www.cardekho.com/overview/Maruti_XL6/Maruti_XL6_Alpha_Plus_AT.htm",
            "https://www.cardekho.com/overview/Maruti_XL6/Maruti_XL6_Alpha_Plus_AT_Dual_Tone.htm",
            "https://www.cardekho.com/overview/Maruti_Jimny/Maruti_Jimny_Zeta.htm",
            "https://www.cardekho.com/overview/Maruti_Jimny/Maruti_Jimny_Alpha.htm",
            "https://www.cardekho.com/overview/Maruti_Jimny/Maruti_Jimny_Alpha_Dual_Tone.htm",
            "https://www.cardekho.com/overview/Maruti_Jimny/Maruti_Jimny_Alpha_AT.htm",
            "https://www.cardekho.com/overview/Maruti_Jimny/Maruti_Jimny_Alpha_Dual_Tone_AT.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_G_Turbo.htm",
            "https://www.cardekho.com/overview/Toyota_Taisor/Toyota_Taisor_V_Turbo_AT_Dual_Tone.htm",
            "https://www.cardekho.com/overview/Honda_Elevate/Honda_Elevate_SV.htm",
            "https://www.cardekho.com/overview/Honda_Elevate/Honda_Elevate_V.htm",
            "https://www.cardekho.com/overview/Honda_Elevate/Honda_Elevate_V_Reinforced.htm",
            "https://www.cardekho.com/overview/Honda_Elevate/Honda_Elevate_V_CVT.htm",
            "https://www.cardekho.com/overview/Honda_Elevate/Honda_Elevate_V_CVT_Reinforced.htm",
            "https://www.cardekho.com/overview/Honda_Elevate/Honda_Elevate_VX_Apex_Edition.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.0_Comfortline.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.0_Highline_AT.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.0_Highline_Plus.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.0_GT_Line.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Adventure.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Smart_Plus.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Empowered_S.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Empowered_Plus_S.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Adventure_LR_AC_FC.htm",
            "https://www.cardekho.com/overview/Tata_Punch_EV/Tata_Punch_EV_Empowered_Plus_S_LR_AC_FC.htm",
            "https://www.cardekho.com/overview/Tata_Tiago_EV/Tata_Tiago_EV_XT_LR.htm",
            "https://www.cardekho.com/overview/Renault_Kiger/Renault_Kiger_RXT_Opt_Turbo_CVT_DT.htm",
            "https://www.cardekho.com/overview/Renault_Kiger/Renault_Kiger_RXZ_Turbo_DT.htm",
            "https://www.cardekho.com/overview/Renault_Kiger/Renault_Kiger_RXZ_Turbo_CVT.htm",
            "https://www.cardekho.com/overview/Renault_Kiger/Renault_Kiger_RXZ_Turbo_CVT_DT.htm",
            "https://www.cardekho.com/overview/Tata_Nexon_EV/Tata_Nexon_EV_Creative_Plus_MR.htm",
            "https://www.cardekho.com/overview/Tata_Nexon_EV/Tata_Nexon_EV_Fearless_Plus_MR.htm",
            "https://www.cardekho.com/overview/Tata_Nexon_EV/Tata_Nexon_EV_Fearless_Plus_S_MR.htm",
            "https://www.cardekho.com/overview/Tata_Nexon_EV/Tata_Nexon_EV_Empowered_MR.htm",
            "https://www.cardekho.com/overview/Tata_Nexon_EV/Tata_Nexon_EV_Fearless_45.htm",
            "https://www.cardekho.com/overview/Mahindra_Bolero_Neo/Mahindra_Bolero_Neo_N8.htm",
            "https://www.cardekho.com/overview/Mahindra_Bolero_Neo/Mahindra_Bolero_Neo_N10_Option.htm",
            "https://www.cardekho.com/overview/Maruti_Ciaz/Maruti_Ciaz_Zeta.htm",
            "https://www.cardekho.com/overview/Maruti_Ciaz/Maruti_Ciaz_Zeta_AT.htm",
            "https://www.cardekho.com/overview/MG_Astor/MG_Astor_Sprint.htm",
            "https://www.cardekho.com/overview/MG_Astor/MG_Astor_Select_BLACKSTORM.htm",
            "https://www.cardekho.com/overview/MG_Astor/MG_Astor_Shine.htm",
            "https://www.cardekho.com/overview/MG_Astor/MG_Astor_Select_BLACKSTORM_CVT.htm",
            "https://www.cardekho.com/overview/Citroen_C3/Citroen_C3_Shine_Turbo_Dark_Edition_AT.htm",
            "https://www.cardekho.com/overview/Citroen_Basalt/Citroen_Basalt_Max_Turbo_Dark_Edition.htm",
            "https://www.cardekho.com/overview/Isuzu_D-Max/Isuzu_D-Max_CBC_HR_2.0.htm",
            "https://www.cardekho.com/overview/Isuzu_D-Max/Isuzu_D-Max_Flat_Deck_HR_2.0.htm",
            "https://www.cardekho.com/overview/Isuzu_D-Max/Isuzu_D-Max_Flat_Deck_HR_AC_1.2.htm",
            "https://www.cardekho.com/overview/Isuzu_D-Max/Isuzu_D-Max_Flat_Deck_HR_AC_2.0.htm",
            "https://www.cardekho.com/overview/Tata_Tigor_EV/Tata_Tigor_EV_XT.htm",
            "https://www.cardekho.com/overview/Tata_Tigor_EV/Tata_Tigor_EV_XE.htm",
            "https://www.cardekho.com/overview/Hyundai_Venue_N_Line/Hyundai_Venue_N_Line_N6_Turbo.htm",
            "https://www.cardekho.com/overview/Hyundai_Venue_N_Line/Hyundai_Venue_N_Line_N6_Turbo_DT.htm",
            "https://www.cardekho.com/overview/Hyundai_Venue_N_Line/Hyundai_Venue_N_Line_N8_Turbo.htm",
            "https://www.cardekho.com/overview/Hyundai_Venue_N_Line/Hyundai_Venue_N_Line_N8_Turbo_DT.htm",
            "https://www.cardekho.com/overview/Hyundai_Venue_N_Line/Hyundai_Venue_N_Line_N8_turbo_DCT.htm",
            "https://www.cardekho.com/overview/Hyundai_Venue_N_Line/Hyundai_Venue_N_Line_N8_turbo_DCT_DT.htm",
            "https://www.cardekho.com/overview/Isuzu_S-CAB/Isuzu_S-CAB_Hi-Ride_AC.htm",
            "https://www.cardekho.com/overview/Citroen_eC3/Citroen_eC3_Feel.htm",
            "https://www.cardekho.com/overview/Citroen_eC3/Citroen_eC3_Shine.htm",
            "https://www.cardekho.com/overview/Citroen_eC3/Citroen_eC3_Shine_DT.htm",
            "https://www.cardekho.com/overview/Toyota_Innova_Crysta/Toyota_Innova_Crysta_2.4_GX_7Str.htm",
            "https://www.cardekho.com/overview/Toyota_Innova_Crysta/Toyota_Innova_Crysta_2.4_GX_8Str.htm",
            "https://www.cardekho.com/overview/Toyota_Innova_Crysta/Toyota_Innova_Crysta_2.4_GX_Plus_7Str.htm",
            "https://www.cardekho.com/overview/Toyota_Innova_Crysta/Toyota_Innova_Crysta_2.4_VX_8Str.htm",
            "https://www.cardekho.com/overview/Toyota_Innova_Crysta/Toyota_Innova_Crysta_2.4_VX_7Str.htm",
            "https://www.cardekho.com/overview/Jeep_Compass/Jeep_Compass_2.0_Sport.htm",
            "https://www.cardekho.com/overview/Jeep_Compass/Jeep_Compass_2.0_Sport_Sandstorm.htm",
            "https://www.cardekho.com/overview/Jeep_Compass/Jeep_Compass_2.0_Longitude_Sandstorm.htm",
            "https://www.cardekho.com/overview/Jeep_Compass/Jeep_Compass_2.0_Longitude_Sandstorm_AT.htm",
            "https://www.cardekho.com/overview/Jeep_Compass/Jeep_Compass_2.0_Longitude_Opt.htm",
            "https://www.cardekho.com/overview/Jeep_Compass/Jeep_Compass_2.0_Limited_Opt.htm",
            "https://www.cardekho.com/overview/Jeep_Compass/Jeep_Compass_2.0_Limited_Opt_FWD_AT.htm",
            "https://www.cardekho.com/overview/Jeep_Compass/Jeep_Compass_2.0_Night_Eagle.htm",
            "https://www.cardekho.com/overview/Jeep_Compass/Jeep_Compass_2.0_Model_S_Opt_4x4_AT.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.0_GT_Line_AT.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.5_GT_DSG.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.0_Topline_AT_ES.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.5_GT_Plus_Sports.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.5_GT_Plus_Sports_DSG.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.0_Highline_Plus.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.0_Highline.htm",
            "https://www.cardekho.com/overview/Volkswagen_Taigun/Volkswagen_Taigun_1.0_Highline_AT.htm",
            "https://www.cardekho.com/overview/Tata_Nexon_EV/Tata_Nexon_EV_Empowered_45.htm",
            "https://www.cardekho.com/overview/Tata_Nexon_EV/Tata_Nexon_EV_Empowered_Plus_45_Red_Dark.htm",
            "https://www.cardekho.com/overview/Force_Gurkha/Force_Gurkha_2.6_Diesel.htm",
            "https://www.cardekho.com/overview/MG_ZS_EV/MG_ZS_EV_Executive.htm",
            "https://www.cardekho.com/overview/MG_ZS_EV/MG_ZS_EV_100_Year_Limited_Edition.htm",
            "https://www.cardekho.com/overview/MG_ZS_EV/MG_ZS_EV_Exclusive_Plus_DT.htm",
            "https://www.cardekho.com/overview/MG_ZS_EV/MG_ZS_EV_Essence.htm",
            "https://www.cardekho.com/overview/MG_ZS_EV/MG_ZS_EV_Essence.htm",
            "https://www.cardekho.com/overview/MG_ZS_EV/MG_ZS_EV_Essence_DT.htm",
            "https://www.cardekho.com/overview/MG_ZS_EV/MG_ZS_EV_Excite_Pro.htm",
            "https://www.cardekho.com/overview/MG_Hector_Plus/MG_Hector_Plus_Select_Pro_7_Str.htm",
            "https://www.cardekho.com/overview/MG_Hector_Plus/MG_Hector_Plus_Select_Pro_7_Str.htm",
            "https://www.cardekho.com/overview/Hyundai_Creta_N_Line/Hyundai_Creta_N_Line_N8_Dual_Tone.htm",
            "https://www.cardekho.com/overview/Hyundai_Creta_N_Line/Hyundai_Creta_N_Line_N8_DCT_Dual_Tone.htm",
            "https://www.cardekho.com/overview/Force_Gurkha_5_Door/Force_Gurkha_5_Door_Diesel.htm",
            "https://www.cardekho.com/overview/Toyota_Innova_Crysta/Toyota_Innova_Crysta_2.4_Zx_7Str.htm",
            "https://www.cardekho.com/overview/Toyota_Innova_Crysta/Toyota_Innova_Crysta_2.4_VX_7Str.htm",
            "https://www.cardekho.com/overview/Toyota_Innova_Crysta/Toyota_Innova_Crysta_2.4_GX_Plus_8Str.htm",
            "https://www.cardekho.com/overview/Toyota_Innova_Crysta/Toyota_Innova_Crysta_2.4_GX_Plus_7Str.htm",
            "https://www.cardekho.com/overview/Kia_Seltos/Kia_Seltos_X-Line_Diesel_AT.htm",
            "https://www.cardekho.com/overview/Kia_Seltos/Kia_Seltos_X-Line_Turbo_DCT.htm",
            "https://www.cardekho.com/overview/Mahindra_XEV_9e/Mahindra_XEV_9e_Pack_One.htm",
            "https://www.cardekho.com/overview/Mahindra_XEV_9e/Mahindra_XEV_9e_Pack_Two.htm",
            "https://www.cardekho.com/overview/Mahindra_XEV_9e/Mahindra_XEV_9e_Pack_Three_Select.htm",
            "https://www.cardekho.com/overview/Mahindra_XEV_9e/Mahindra_XEV_9e_Pack_Three.htm",
            "https://www.cardekho.com/overview/Tata_Harrier/Tata_Harrier_Adventure_Plus_A_AT.htm",
            "https://www.cardekho.com/overview/Tata_Harrier/Tata_Harrier_Fearless_AT.htm",
            "https://www.cardekho.com/overview/Tata_Harrier/Tata_Harrier_Fearless_Plus_Stealth_AT.htm",
            "https://www.cardekho.com/overview/Toyota_Hilux/Toyota_Hilux_STD.htm",
            "https://www.cardekho.com/overview/Force_Urbania/Force_Urbania_3615WB_14Str.htm",
            "https://www.cardekho.com/overview/Force_Urbania/Force_Urbania_3350WB_10Str.htm",
            "https://www.cardekho.com/overview/Force_Urbania/Force_Urbania_4400WB_17Str.htm",
            "https://www.cardekho.com/overview/Force_Urbania/Force_Urbania_3615WB_13Str.htm",
            "https://www.cardekho.com/overview/Force_Urbania/Force_Urbania_4400WB_13Str.htm",
            "https://www.cardekho.com/overview/Jeep_Meridian/Jeep_Meridian_Longitude_4x2.htm",
            "https://www.cardekho.com/overview/Jeep_Meridian/Jeep_Meridian_Longitude_4x2_AT.htm",
            "https://www.cardekho.com/overview/Jeep_Meridian/Jeep_Meridian_Limited_Opt_4x2_AT.htm",
            "https://www.cardekho.com/overview/BYD_Atto_3/BYD_Atto_3_Dynamic.htm",
            "https://www.cardekho.com/overview/BYD_Atto_3/BYD_Atto_3_Premium.htm",
            "https://www.cardekho.com/overview/Hyundai_Tucson/Hyundai_Tucson_Signature_Diesel_AT_DT.htm",
            "https://www.cardekho.com/overview/Hyundai_Tucson/Hyundai_Tucson_Platinum_AT.htm",
            "https://www.cardekho.com/overview/MG_ZS_EV/MG_ZS_EV_Excite_Pro.htm",
            "https://www.cardekho.com/overview/MG_ZS_EV/MG_ZS_EV_100_Year_Limited_Edition.htm",
            "https://www.cardekho.com/overview/MG_ZS_EV/MG_ZS_EV_Essence.htm",
            "https://www.cardekho.com/overview/BYD_eMAX_7/BYD_eMAX_7_Premium_6Str.htm",
            "https://www.cardekho.com/overview/BYD_eMAX_7/BYD_eMAX_7_Premium_7Str.htm",
            "https://www.cardekho.com/overview/BYD_eMAX_7/BYD_eMAX_7_Superior_7Str.htm",
            "https://www.cardekho.com/overview/Honda_City_Hybrid/Honda_City_Hybrid_ZX_CVT_Reinforced.htm",
            "https://www.cardekho.com/overview/Isuzu_Hi-Lander/Isuzu_Hi-Lander_4x2_MT.htm",
            "https://www.cardekho.com/overview/Force_Urbania/Force_Urbania_4400WB_13Str.htm",
            "https://www.cardekho.com/overview/BYD_Seal/BYD_Seal_Dynamic_Range.htm",
            "https://www.cardekho.com/overview/BYD_Seal/BYD_Seal_Premium_Range.htm",
            "https://www.cardekho.com/overview/BYD_Sealion_7/BYD_Sealion_7_Premium.htm",
            "https://www.cardekho.com/overview/BMW_iX1/BMW_iX1_LWB.htm",
            "https://www.cardekho.com/overview/BMW_2_Series/BMW_2_Series_220i_M_Sport.htm",
            "https://www.cardekho.com/overview/BMW_2_Series/BMW_2_Series_220d_M_Sport.htm",
            "https://www.cardekho.com/overview/BMW_2_Series/BMW_2_Series_220i_M_Sport_Shadow_Edition.htm",
            "https://www.cardekho.com/overview/Mini_Cooper_Countryman/Mini_Cooper_Countryman_S_JCW_Inspired.htm",
            "https://www.cardekho.com/overview/Nissan_X-Trail/Nissan_X-Trail_STD.htm",
            "https://www.cardekho.com/overview/Pravaig_DEFY/Pravaig_DEFY_Hacker_Edition.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_A-Class_Limousine/Mercedes-Benz_A-Class_Limousine_A_200.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_A-Class_Limousine/Mercedes-Benz_A-Class_Limousine_A_200d.htm",
            "https://www.cardekho.com/overview/Hyundai_IONIQ_5/Hyundai_IONIQ_5_Long_Range_RWD.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_GLC/Mercedes-Benz_GLC_300.htm",
            "https://www.cardekho.com/overview/BMW_X5/BMW_X5_xDrive40i_xLine.htm",
            "https://www.cardekho.com/overview/BMW_X5/BMW_X5_xDrive30d_xLine.htm",
            "https://www.cardekho.com/overview/Kia_Carnival/Kia_Carnival_Limousine_Plus.htm",
            "https://www.cardekho.com/overview/BMW_X1/BMW_X1_sDrive18d_M_Sport.htm",
            "https://www.cardekho.com/overview/BMW_X1/BMW_X1_sDrive18i_M_Sport.htm",
            "https://www.cardekho.com/overview/Land_Rover_Range_Rover_Velar/Land_Rover_Range_Rover_Velar_Dynamic_HSE.htm",
            "https://www.cardekho.com/overview/Land_Rover_Range_Rover_Velar/Land_Rover_Range_Rover_Velar_Dynamic_HSE_Diesel.htm",
            "https://www.cardekho.com/overview/Kia_EV6/Kia_EV6_GT_Line.htm",
            "https://www.cardekho.com/overview/Audi_Q3/Audi_Q3_Technology.htm",
            "https://www.cardekho.com/overview/Audi_Q3/Audi_Q3_Bold_Edition.htm",
            "https://www.cardekho.com/overview/Audi_Q3/Audi_Q3_Premium.htm",
            "https://www.cardekho.com/overview/BMW_Z4/BMW_Z4_M40i.htm",
            "https://www.cardekho.com/overview/BMW_Z4/BMW_Z4_M40i_Pure_Impulse_AT.htm",
            "https://www.cardekho.com/overview/BMW_Z4/BMW_Z4_M40i_Pure_Impulse.htm",
            "https://www.cardekho.com/overview/BMW_3_Series/BMW_3_Series_M340i_xDrive.htm",
            "https://www.cardekho.com/overview/BMW_X3/BMW_X3_xDrive_20_M_Sport.htm",
            "https://www.cardekho.com/overview/Audi_A6/Audi_A6_45_TFSI_Technology.htm",
            "https://www.cardekho.com/overview/BYD_Seal/BYD_Seal_Performance.htm",
            "https://www.cardekho.com/overview/Audi_Q7/Audi_Q7_Premium_Plus.htm",
            "https://www.cardekho.com/overview/Audi_Q7/Audi_Q7_Bold_Edition.htm",
            "https://www.cardekho.com/overview/Jeep_Wrangler/Jeep_Wrangler_Unlimited.htm",
            "https://www.cardekho.com/overview/Jeep_Wrangler/Jeep_Wrangler_Rubicon.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_C-Class/Mercedes-Benz_C-Class_C_200.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_C-Class/Mercedes-Benz_C-Class_C_300.htm",
            "https://www.cardekho.com/overview/Audi_Q5/Audi_Q5_Premium_Plus.htm",
            "https://www.cardekho.com/overview/Audi_Q5/Audi_Q5_Bold_Edition.htm",
            "https://www.cardekho.com/overview/BMW_5_Series/BMW_5_Series_530Li.htm",
            "https://www.cardekho.com/overview/Land_Rover_Discovery/Land_Rover_Discovery_2.0_S.htm",
            "https://www.cardekho.com/overview/Land_Rover_Discovery/Land_Rover_Discovery_3.0_Diesel_S.htm",
            "https://www.cardekho.com/overview/Land_Rover_Discovery/Land_Rover_Discovery_3.0_S.htm",
            "https://www.cardekho.com/overview/Land_Rover_Discovery/Land_Rover_Discovery_2.0_Dynamic_HSE.htm",
            "https://www.cardekho.com/overview/Land_Rover_Discovery/Land_Rover_Discovery_3.0_Diesel_Metropolitan_Edition.htm",
            "https://www.cardekho.com/overview/Land_Rover_Discovery/Land_Rover_Discovery_3.0_l_Metropolitan_Edition.htm",
            "https://www.cardekho.com/overview/Land_Rover_Range_Rover_Evoque/Land_Rover_Range_Rover_Evoque_2.0_Dynamic_SE.htm",
            "https://www.cardekho.com/overview/Land_Rover_Range_Rover_Evoque/Land_Rover_Range_Rover_Evoque_2.0_Dynamic_SE_Diesel.htm",
            "https://www.cardekho.com/overview/Volvo_XC60/Volvo_XC60_B5_Ultimate.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_E-Class/Mercedes-Benz_E-Class_E_200.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_E-Class/Mercedes-Benz_E-Class_E_220d.htm",
            "https://www.cardekho.com/overview/Jaguar_F-Pace/Jaguar_F-Pace_2.0_R-Dynamic_S.htm",
            "https://www.cardekho.com/overview/Jaguar_F-Pace/Jaguar_F-Pace_2.0_R-Dynamic_S_Diesel.htm",
            "https://www.cardekho.com/overview/Porsche_Macan/Porsche_Macan_Standard.htm",
            "https://www.cardekho.com/overview/Porsche_Macan/Porsche_Macan_S.htm",
            "https://www.cardekho.com/overview/Porsche_Macan/Porsche_Macan_GTS.htm",
            "https://www.cardekho.com/overview/Lexus_ES/Lexus_ES_300h_Exquisite.htm",
            "https://www.cardekho.com/overview/Lexus_ES/Lexus_ES_300h_Luxury.htm",
            "https://www.cardekho.com/overview/Volvo_S90/Volvo_S90_B5_Ultimate.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_GLA/Mercedes-Benz_GLA_200.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_GLA/Mercedes-Benz_GLA_220d_4MATIC.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_GLE/Mercedes-Benz_GLE_300d_4Matic_AMG_Line.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_GLE/Mercedes-Benz_GLE_450_4Matic.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_GLE/Mercedes-Benz_GLE_450d_4Matic.htm",
            "https://www.cardekho.com/overview/BMW_6_Series/BMW_6_Series_GT_630i_M_Sport.htm",
            "https://www.cardekho.com/overview/BMW_6_Series/BMW_6_Series_GT_630i_M_Sport_Signature.htm",
            "https://www.cardekho.com/overview/BMW_6_Series/BMW_6_Series_GT_620d_M_Sport_Signature.htm",
            "https://www.cardekho.com/overview/Jeep_Grand_Cherokee/Jeep_Grand_Cherokee_Limited_Opt.htm",
            "https://www.cardekho.com/overview/Volvo_C40_Recharge/Volvo_C40_Recharge_E80.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_EQB/Mercedes-Benz_EQB_250_Plus.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_EQB/Mercedes-Benz_EQB_350_4Matic.htm",
            "https://www.cardekho.com/overview/BMW_3_Series_Long_Wheelbase/BMW_3_Series_Long_Wheelbase_330Li_M_Sport.htm",
            "https://www.cardekho.com/overview/Lexus_RX/Lexus_RX_350h_Luxury_Lexus_Premium_System.htm",
            "https://www.cardekho.com/overview/Lexus_RX/Lexus_RX_350h_Luxury_Mark_Levinson_System.htm",
            "https://www.cardekho.com/overview/Lexus_RX/Lexus_RX_500h_F_SPORT_Lexus_Premium_System.htm",
            "https://www.cardekho.com/overview/Volvo_XC40_Recharge/Volvo_XC40_Recharge_E60_Plus.htm",
            "https://www.cardekho.com/overview/Volvo_XC40_Recharge/Volvo_XC40_Recharge_E80_ultimate.htm",
            "https://www.cardekho.com/overview/Lexus_NX/Lexus_NX_350h_Exquisite.htm",
            "https://www.cardekho.com/overview/Lexus_NX/Lexus_NX_350h_Luxury.htm",
            "https://www.cardekho.com/overview/Lexus_NX/Lexus_NX_350h_F-sport.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_AMG_C43/Mercedes-Benz_AMG_C43_4Matic.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_AMG_A_45_S/Mercedes-Benz_AMG_A_45_S_4MATIC_Plus.htm",
            "https://www.cardekho.com/overview/BMW_i4/BMW_i4_eDrive35_M_Sport.htm",
            "https://www.cardekho.com/overview/BMW_i4/BMW_i4_eDrive40_M_Sport.htm",
            "https://www.cardekho.com/overview/Land_Rover_Discovery_Sport/Land_Rover_Discovery_Sport_Dynamic_SE_Diesel.htm",
            "https://www.cardekho.com/overview/Mini_Cooper_SE/Mini_Cooper_SE_Electric.htm",
            "https://www.cardekho.com/overview/Audi_S5_Sportback/Audi_S5_Sportback_3.0L_TFSI.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_AMG_GLA_35/Mercedes-Benz_AMG_GLA_35_4MATIC.htm",
            "https://www.cardekho.com/overview/Audi_Q3_Sportback/Audi_Q3_Sportback_40TFSI_Quattro.htm",
            "https://www.cardekho.com/overview/Land_Rover_Defender/Land_Rover_Defender_2.0_110_X-Dynamic_HSE.htm",
            "https://www.cardekho.com/overview/Land_Rover_Defender/Land_Rover_Defender_3.0_Diesel_90_X-Dynamic_HSE.htm",
            "https://www.cardekho.com/overview/Land_Rover_Defender/Land_Rover_Defender_5.0_l_X-Dynamic_HSE_90.htm",
            "https://www.cardekho.com/overview/Land_Rover_Defender/Land_Rover_Defender_3.0_Diesel_110_Sedona_Edition.htm",
            "https://www.cardekho.com/overview/Land_Rover_Defender/Land_Rover_Defender_3.0_Diesel_110_X.htm",
            "https://www.cardekho.com/overview/Land_Rover_Defender/Land_Rover_Defender_3.0_l_Diesel_130_X.htm",
            "https://www.cardekho.com/overview/Land_Rover_Defender/Land_Rover_Defender_Octa.htm",
            "https://www.cardekho.com/overview/Land_Rover_Defender/Land_Rover_Defender_Octa_Edition_One.htm",
            "https://www.cardekho.com/overview/Land_Rover_Range_Rover/Land_Rover_Range_Rover_3.0_I_Diesel_LWB_HSE.htm",
            "https://www.cardekho.com/overview/Land_Rover_Range_Rover/Land_Rover_Range_Rover_3.0_I_LWB_Autobiography.htm",
            "https://www.cardekho.com/overview/Land_Rover_Range_Rover/Land_Rover_Range_Rover_SV_Ranthambore_Edition.htm",
            "https://www.cardekho.com/overview/Toyota_Land_Cruiser_300/Toyota_Land_Cruiser_300_GR_S.htm",
            "https://www.cardekho.com/overview/Toyota_Land_Cruiser_300/Toyota_Land_Cruiser_300_ZX.htm",
            "https://www.cardekho.com/overview/BMW_X5/BMW_X5_xDrive40i_M_Sport.htm",
            "https://www.cardekho.com/overview/BMW_X5/BMW_X5_xDrive30d_M_Sport.htm",
            "https://www.cardekho.com/overview/Toyota_Vellfire/Toyota_Vellfire_Hi.htm",
            "https://www.cardekho.com/overview/Toyota_Vellfire/Toyota_Vellfire_VIP_Executive_Lounge.htm",
            "https://www.cardekho.com/overview/Toyota_Vellfire/Toyota_Vellfire_VIP_Executive_Lounge.htm",
            "https://www.cardekho.com/overview/Porsche_911/Porsche_911_Carrera.htm",
            "https://www.cardekho.com/overview/Porsche_911/Porsche_911_Turbo_S.htm",
            "https://www.cardekho.com/overview/Porsche_911/Porsche_911_GT3_RS.htm",
            "https://www.cardekho.com/overview/Porsche_911/Porsche_911_Turbo_50_Years.htm",
            "https://www.cardekho.com/overview/Porsche_911/Porsche_911_ST.htm",
            "https://www.cardekho.com/overview/Lamborghini_Urus/Lamborghini_Urus_S.htm",
            "https://www.cardekho.com/overview/Lamborghini_Urus/Lamborghini_Urus_Performante.htm",
            "https://www.cardekho.com/overview/Lamborghini_Urus/Lamborghini_Urus_SE_Plugin_Hybrid.htm",
            "https://www.cardekho.com/overview/Lamborghini_Revuelto/Lamborghini_Revuelto_LB_744.htm",
            "https://www.cardekho.com/overview/Volvo_XC90/Volvo_XC90_B5_AWD.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Cullinan/Rolls-Royce_Cullinan_Series_II.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Cullinan/Rolls-Royce_Cullinan_Black_Badge_Series_II.htm",
            "https://www.cardekho.com/overview/BMW_i7/BMW_i7_eDrive50_M_Sport.htm",
            "https://www.cardekho.com/overview/BMW_i7/BMW_i7_M70_xDrive.htm",
            "https://www.cardekho.com/overview/Land_Rover_Range_Rover_Sport/Land_Rover_Range_Rover_Sport_3.0_Diesel_Dynamic_SE.htm",
            "https://www.cardekho.com/overview/Land_Rover_Range_Rover_Sport/Land_Rover_Range_Rover_Sport_3.0_Dynamic_SE.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Phantom/Rolls-Royce_Phantom_Series_II.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Phantom/Rolls-Royce_Phantom_Extended_Wheelbase.htm",
            "https://www.cardekho.com/overview/Porsche_Cayenne/Porsche_Cayenne_STD.htm",
            "https://www.cardekho.com/overview/Porsche_Cayenne/Porsche_Cayenne_GTS.htm",
            "https://www.cardekho.com/overview/Kia_EV9/Kia_EV9_GT_Line.htm",
            "https://www.cardekho.com/overview/BMW_7_Series/BMW_7_Series_740i_M_Sport.htm",
            "https://www.cardekho.com/overview/BMW_7_Series/BMW_7_Series_740d_M_Sport.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_S-Class/Mercedes-Benz_S-Class_S_350d.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_S-Class/Mercedes-Benz_S-Class_S450_4Matic.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_Maybach_GLS/Mercedes-Benz_Maybach_GLS_600_Night_Series.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_G-Class/Mercedes-Benz_G-Class_400d_AMG_Line.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_G-Class/Mercedes-Benz_G-Class_400d_Adventure_Edition.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_G-Class/Mercedes-Benz_G-Class_AMG_G_63_Grand_Edition.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Spectre/Rolls-Royce_Spectre_Electric.htm",
            "https://www.cardekho.com/overview/BMW_M4_Competition/BMW_M4_Competition_xDrive.htm",
            "https://www.cardekho.com/overview/Porsche_Macan/Porsche_Macan_GTS.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_G-Class_Electric/Mercedes-Benz_G-Class_Electric_G_580.htm",
            "https://www.cardekho.com/overview/Bentley_Flying_Spur/Bentley_Flying_Spur_V6_Hybrid.htm",
            "https://www.cardekho.com/overview/Bentley_Flying_Spur/Bentley_Flying_Spur_V8.htm",
            "https://www.cardekho.com/overview/Bentley_Flying_Spur/Bentley_Flying_Spur_S_Hybrid.htm",
            "https://www.cardekho.com/overview/Bentley_Flying_Spur/Bentley_Flying_Spur_V8_Azure.htm",
            "https://www.cardekho.com/overview/Bentley_Flying_Spur/Bentley_Flying_Spur_Mulliner_V8.htm",
            "https://www.cardekho.com/overview/Audi_RS_Q8/Audi_RS_Q8_Performance.htm",
            "https://www.cardekho.com/overview/BMW_iX/BMW_iX_xDrive50.htm",
            "https://www.cardekho.com/overview/Aston_Martin_Vanquish/Aston_Martin_Vanquish_V12.htm",
            "https://www.cardekho.com/overview/BMW_M4_CS/BMW_M4_CS_xDrive.htm",
            "https://www.cardekho.com/overview/Bentley_Bentayga/Bentley_Bentayga_V8.htm",
            "https://www.cardekho.com/overview/Bentley_Bentayga/Bentley_Bentayga_S.htm",
            "https://www.cardekho.com/overview/Bentley_Bentayga/Bentley_Bentayga_EWB_Azure_FIRST_EDITION.htm",
            "https://www.cardekho.com/overview/Aston_Martin_Vantage/Aston_Martin_Vantage_V8.htm",
            "https://www.cardekho.com/overview/Maserati_Levante/Maserati_Levante_350_GranSport.htm",
            "https://www.cardekho.com/overview/Maserati_Levante/Maserati_Levante_GranSport_Diesel.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_EQS_SUV/Mercedes-Benz_EQS_SUV_450_4Matic.htm",
            "https://www.cardekho.com/overview/Mclaren_GT/Mclaren_GT_V8.htm",
            "https://www.cardekho.com/overview/Porsche_Taycan/Porsche_Taycan_STD.htm",
            "https://www.cardekho.com/overview/Porsche_Taycan/Porsche_Taycan_4S.htm",
            "https://www.cardekho.com/overview/Porsche_Panamera/Porsche_Panamera_STD_Hybrid.htm",
            "https://www.cardekho.com/overview/Porsche_Panamera/Porsche_Panamera_GTS.htm",
            "https://www.cardekho.com/overview/Lexus_LM/Lexus_LM_350h_7_Seater_VIP.htm",
            "https://www.cardekho.com/overview/Maserati_Grecale/Maserati_Grecale_GT.htm",
            "https://www.cardekho.com/overview/Lamborghini_Huracan_EVO/Lamborghini_Huracan_EVO_Spyder.htm",
            "https://www.cardekho.com/overview/Lamborghini_Huracan_EVO/Lamborghini_Huracan_EVO_Sterrato.htm",
            "https://www.cardekho.com/overview/Lamborghini_Huracan_EVO/Lamborghini_Huracan_EVO_Tecnica.htm",
            "https://www.cardekho.com/overview/Mclaren_750S/Mclaren_750S_Coupe.htm",
            "https://www.cardekho.com/overview/Ferrari_296_GTB/Ferrari_296_GTB_V6_hybrid.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_AMG_SL/Mercedes-Benz_AMG_SL_55_4Matic_Plus_Roadster.htm",
            "https://www.cardekho.com/overview/Ferrari_F8_Tributo/Ferrari_F8_Tributo_V8_Turbo.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_Maybach_SL_680/Mercedes-Benz_Maybach_SL_680_Monogram_Series.htm",
            "https://www.cardekho.com/overview/Ferrari_SF90_Stradale/Ferrari_SF90_Stradale_Coupe_V8.htm",
            "https://www.cardekho.com/overview/Lotus_Eletre/Lotus_Eletre_Base.htm",
            "https://www.cardekho.com/overview/Lotus_Eletre/Lotus_Eletre_R.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_EQE_SUV/Mercedes-Benz_EQE_SUV_500_4MATIC.htm",
            "https://www.cardekho.com/overview/Maserati_Gran_Cabrio/Maserati_Gran_Cabrio_4.7_V8.htm",
            "https://www.cardekho.com/overview/Maserati_Gran_Cabrio/Maserati_Gran_Cabrio_Sport_Diesel.htm",
            "https://www.cardekho.com/overview/Maserati_Gran_Cabrio/Maserati_Gran_Cabrio_MC_Diesel.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_Maybach_EQS_SUV/Mercedes-Benz_Maybach_EQS_SUV_680.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_Maybach_EQS_SUV/Mercedes-Benz_Maybach_EQS_SUV_Night_Series.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_EQS/Mercedes-Benz_EQS_580_4Matic.htm",
            "https://www.cardekho.com/overview/Aston_Martin_DBX/Aston_Martin_DBX_V8.htm",
            "https://www.cardekho.com/overview/Aston_Martin_DBX/Aston_Martin_DBX_707.htm",
            "https://www.cardekho.com/overview/Porsche_Macan_EV/Porsche_Macan_EV_Standard.htm",
            "https://www.cardekho.com/overview/Ferrari_Roma/Ferrari_Roma_Coupe_V8.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_Maybach_S-Class/Mercedes-Benz_Maybach_S-Class_S580.htm",
            "https://www.cardekho.com/overview/Ferrari_812/Ferrari_812_GTS.htm",
            "https://www.cardekho.com/overview/Audi_RS_e-tron_GT/Audi_RS_e-tron_GT_Quattro.htm",
            "https://www.cardekho.com/overview/Audi_RS_e-tron_GT/Audi_RS_e-tron_GT_Quattro.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_CLE_Cabriolet/Mercedes-Benz_CLE_Cabriolet_300_4Matic_AMG_Line.htm",
            "https://www.cardekho.com/overview/Lotus_Emeya/Lotus_Emeya_GT.htm",
            "https://www.cardekho.com/overview/Mercedes-Benz_AMG_E_53_Cabriolet/Mercedes-Benz_AMG_E_53_Cabriolet_4MATIC_Plus.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Ghost_Series_II/Rolls-Royce_Ghost_Series_II_Standard.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Ghost_Series_II/Rolls-Royce_Ghost_Series_II_Extended_Wheelbase.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Ghost_Series_II/Rolls-Royce_Ghost_Series_II_Black_Badge.htm",
            "https://www.cardekho.com/overview/Porsche_Cayenne_Coupe/Porsche_Cayenne_Coupe_STD.htm",
            "https://www.cardekho.com/overview/Porsche_Cayenne_Coupe/Porsche_Cayenne_Coupe_GTS.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Ghost_Series_II/Rolls-Royce_Ghost_Series_II_Standard.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Ghost_Series_II/Rolls-Royce_Ghost_Series_II_Extended_Wheelbase.htm",
            "https://www.cardekho.com/overview/Rolls-Royce_Ghost_Series_II/Rolls-Royce_Ghost_Series_II_Black_Badge.htm",
            # ... (ALL OTHER URLs FROM YOUR LIST WITH "#specification" APPENDED)
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        return webdriver.Chrome(options=chrome_options)

    def load_full_page(self, url):
        driver = self.init_driver()
        driver.get(url)
        time.sleep(3)  # Initial load
        no_change_count = 0
        max_no_change = 6
        scroll_pause_time = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        while no_change_count < max_no_change:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                no_change_count += 1
            else:
                no_change_count = 0
            last_height = new_height
        html = driver.page_source
        driver.quit()
        return html

    def get_variant_urls_from_card(self,card):
        """
        From a car card element, extract specs page hrefs from the
        "Variant Matching Your Search Criteria" and "Other Variants" sections.
        Construct the full URL as follows:
          - If href starts with "/overview": base_url + href + "#specification"
          - Otherwise: base_url + href (if it starts with a slash) or as is.
        """
        urls = []
        for cls in ["expandcollapse matching clear", "expandcollapse other clear"]:
            section = card.find("div", class_=cls)
            if section:
                ul = section.find("ul", class_="gsc_thin_scroll")
                if ul:
                    for li in ul.find_all("li"):
                        a_tag = li.find("a")
                        if a_tag:
                            href = a_tag.get("href")
                            if href:
                                if href.startswith("/overview"):
                                    full_url = self.base_url + href + "#specification"
                                else:
                                    full_url = self.base_url + href if href.startswith("/") else href
                                urls.append(full_url)
        return urls

    def scrape_results_page(self,url):
        """
        Load the listing page using Selenium (via load_full_page) and extract specs page URLs.
        """
        full_html = self.load_full_page(url)
        soup = BeautifulSoup(full_html, 'html.parser')
        variant_urls = []
        cards = soup.find_all("div", class_="gsc_col-md-12 gsc_col-sm-12 gsc_col-xs-12 append_list")
        print(f"Found {len(cards)} car cards on endpoint: {url}")
        for card in cards:
            urls = self.get_variant_urls_from_card(card)
            variant_urls.extend(urls)
        return list(set(variant_urls))

    @staticmethod
    def parse_table(table):
        """
        Extract key-value pairs from a table element.
        If the value cell contains an <i> tag:
          - If class contains 'icon-check', set value to "Yes"
          - If class contains 'icon-deletearrow', set value to "No"
        Otherwise, use the text in the cell.
        """
        data = {}
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 2:
                key = cols[0].get_text(strip=True)
                value_cell = cols[1]
                i_tag = value_cell.find("i")
                if i_tag:
                    classes = i_tag.get("class", [])
                    if "icon-check" in classes:
                        value = "Yes"
                    elif "icon-deletearrow" in classes:
                        value = "No"
                    else:
                        value = value_cell.get_text(strip=True)
                else:
                    value = value_cell.get_text(strip=True)
                data[key] = value
        return data

    def parse_spec_page(self,spec_url):
   
        print(f"Fetching spec page: {spec_url}")
        try:
            res = requests.get(spec_url, headers=self.headers)
            if res.status_code != 200:
                print(f"Failed to fetch specs page: {spec_url} (Status: {res.status_code})")
                return {}
            soup = BeautifulSoup(res.text, "html.parser")
            specs = {}

            # Extract image from the standard container if available
            model_img_div = soup.find("div", class_="modelTopImg")
            if model_img_div:
                img_tag = model_img_div.find("img")
                if img_tag and img_tag.get("src"):
                    specs["Image"] = img_tag.get("src")
            
            # New gallery-based image extraction if the standard image is missing
            if "Image" not in specs:
                # Attempt to find gallery section with data-track-section="gallery"
                gallery_section = soup.find("div", attrs={"data-track-section": "gallery"})
                if gallery_section:
                    # First try to find a ul with data-carousel="OverviewTop"
                    overview_ul = gallery_section.find("ul", attrs={"data-carousel": "OverviewTop"})
                    if not overview_ul:
                        # Fallback: look for a ul with data-carousel="gallery"
                        overview_ul = gallery_section.find("ul", attrs={"data-carousel": "gallery"})
                    if overview_ul:
                        # Find the first li with data-track-section="image"
                        first_li = overview_ul.find("li", attrs={"data-track-section": "image"})
                        if first_li:
                            img_tag = first_li.find("img")
                            if img_tag and img_tag.get("src"):
                                specs["Image"] = img_tag.get("src")

            quick_overview = soup.find("section", class_="quickOverviewNew")
            if quick_overview:
                # Sometimes overviewdetail may be missing in quickOverview pages, so try to capture model info from <h2>
                h2 = quick_overview.find("h2")
                if h2 and "overview" in h2.get_text(strip=True).lower():
                    specs["Overview Title"] = h2.get_text(strip=True)
                # Extract Key Specifications
                key_specs_section = quick_overview.find("div", attrs={"data-track-section": "Key Specifications"})
                if key_specs_section:
                    # Look inside qccontent first
                    qc = key_specs_section.find("div", class_="qccontent")
                    if qc:
                        table = qc.find("table")
                    else:
                        table = key_specs_section.find("table")
                    if table:
                        specs["Key Specifications"] = self.parse_table(table)
                # Extract Top Features
                top_features_section = quick_overview.find("div", attrs={"data-track-section": "Top Features"})
                if top_features_section:
                    qc = top_features_section.find("div", class_="qccontent")
                    if qc:
                        ul = qc.find("ul")
                    else:
                        ul = top_features_section.find("ul")
                    if ul:
                        features = [li.get_text(strip=True) for li in ul.find_all("li")]
                        specs["Top Features"] = {"Features": ", ".join(features)}

            # Extract overview detail block data (if available)
            overview_detail = soup.find("div", class_="overviewdetail")
            if overview_detail:
                h1 = overview_detail.find("h1", class_="displayInlineBlock")
                if h1:
                    specs["Model"] = h1.get_text(strip=True)
                start_rating = overview_detail.find("div", class_="startRating")
                if start_rating:
                    rating_span = start_rating.find("span", class_="ratingStarNew")
                    if rating_span:
                        specs["Rating"] = rating_span.get_text(strip=True)
                    reviews_span = start_rating.find("span", class_="reviews")
                    if reviews_span:
                        specs["Reviews"] = reviews_span.get_text(strip=True)
                price_div = soup.find("div", class_="price")
                if price_div:
                    price_text = ' '.join(price_div.get_text().split())
                    match = re.search(r"Rs\.\s*([\d,\.]+\s*\w+)", price_text)
                    if match:
                        specs["Price"] = match.group(1).strip()

            # Extract specs from scrollDiv section if available
            scroll_div = soup.find("div", id="scrollDiv")
            if scroll_div:
                for header in scroll_div.find_all("h3"):
                    section_title = header.get_text(strip=True)
                    table = header.find_next("table")
                    if table:
                        specs[section_title] = self.parse_table(table)

            # Process quickOverviewNew section if available (this captures the missed structure)
            # Fallback: if no overview or scrollDiv found, try any table with class "keyfeature"
            if "Key Specifications" not in specs:
                table = soup.find("table", class_="keyfeature")
                if table:
                    specs["Key Specifications"] = self.parse_table(table)

            # --- Additional extraction: Look for any <div class="qccontent"> blocks not already captured.
            additional_count = 1
            for qc in soup.find_all("div", class_="qccontent"):
                # If this qccontent block contains a table and its parent section is not already handled, add it.
                table = qc.find("table")
                if table:
                    key_name = f"Additional Specs {additional_count}"
                    # Only add if this key is not already present
                    if key_name not in specs:
                        specs[key_name] = self.parse_table(table)
                        additional_count += 1

            return specs
        except Exception as e:
            print("Error in parse_spec_page:", e)
            return {}

    def extract_car_data(self, specs, spec_url):
        if not specs:
            return None
        base_specs = {
            'price': specs.get('Price'),
            'model': specs.get('Model', 'Unknown Model'),
            'transmission': specs.get('Key Specifications_Transmission'),
            'seating': self.extract_seating(specs),
            'safety_rating': self.extract_safety_rating(specs)
        }
        category = 'ev' if self.is_electric(specs) else 'fuel'
        media = {'image': specs.get('Image', '')}
        car_data = {
            'specs': specs,
            'media': media,
            'category': category,
            'base_specs': {k: v for k, v in base_specs.items() if v is not None},
            'spec_url': spec_url
        }
        if category == 'ev':
            car_data['ev_specific'] = {
                'battery': specs.get('Key Specifications_Battery Capacity'),
                'range': specs.get('Key Specifications_Range')
            }
        else:
            car_data['fuel_specific'] = {
                'engine': specs.get('Key Specifications_Engine'),
                'mileage': specs.get('Key Specifications_Mileage')
            }
        return car_data

    def extract_seating(self, specs):
        seating_str = specs.get('Key Specifications_Seating Capacity', '')
        match = re.search(r'\d+', seating_str)
        return int(match.group()) if match else None

    def extract_safety_rating(self, specs):
        for section_name, section in specs.items():
            if isinstance(section, dict):
                for key, value in section.items():
                    if 'Global NCAP' in key:
                        match = re.search(r'\d+\.?\d*', str(value))
                        return float(match.group()) if match else None
        return None

    def is_electric(self, specs):
        fuel_type = specs.get('Key Specifications_Fuel Type', '').lower()
        return 'electric' in fuel_type

    def process_spec_url(self, spec_url):
        print(f"\nProcessing spec URL: {spec_url}")
        specs = self.parse_spec_page(spec_url)
        if not specs:
            return
        car_data = self.extract_car_data(specs, spec_url)
        if not car_data:
            return
        # Prepare document
        document = {
            'spec_url': spec_url,
            'specs': car_data['specs'],
            'media': car_data['media'],
            'category': car_data['category'],
            'base_specs': car_data['base_specs'],
            'ev_specific': car_data.get('ev_specific'),
            'fuel_specific': car_data.get('fuel_specific'),
            'last_updated': datetime.datetime.now()
        }
        # Upsert into MongoDB
        self.db.collection.update_one(
            {"spec_url": spec_url},
            {"$set": document},
            upsert=True
        )
        time.sleep(1)  #  # Polite delay# Polite delay

    def run(self):
        for spec_url in self.spec_urls:
            try:
                self.process_spec_url(spec_url)
            except Exception as e:
                print(f"Error processing {spec_url}: {str(e)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.client.close()

if __name__ == "__main__":
    with CarScraper() as scraper:
        scraper.run()