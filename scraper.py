import telethon
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty
import json
from PIL import Image
import re
import asyncio

api_id = 12904801  # Your API ID
api_hash = 'b704615d6fd3a2e606a22deb2f1bcb44'  # Your API HASH
movies = {}
series = {}

# media > document > attribute > file_name
dic_list_all_series_movies = {
    "Ms. Marvel": ["Ms.Marvel.S01E02", "Ms.Marvel.S01E02", "Ms_Marvel_S01E01", "Ms_Marvel_S01E01"],
    "Marvel Studios: Assembled (2021)": ["Marvel.Studios.Assembld.S01E09", "Marvel_Studios_Assembled_S01E08",
                                         "Marvel_Studios_Assembled_S01E07", "Marvel.Studios.Assembled.S01E06",
                                         "Marvel.Studios.Assembled.S01E05", "Marvel.Studios.Assembled.S01E04",
                                         "ASSEMBLED.S01E03", "Marvel_Studios_Assembled_S01E02",
                                         "Marvel_Studios:_Assembled_S01E01"],
    "Fury Files (2012)": ["F.F.S01E16", "F.F.S01E15", "F.F.S01E14", "F.F.S01E13", "F.F.S01E12", "F.F.S01E11",
                          "F.F.S01E10", "F.F.S01E09", "F.F.S01E08", "F.F.S01E07", "F.F.S01E06", "F.F.S01E05",
                          "F.F.S01E04", "F.F.S01E03", "F.F.S01E02", "F.F.S01E01"],
    "Morbius": ["Morbius.2022.1080p", "Morbius.2022.1080p"],
    "Moon Knight": ["Moon.Knight.S01E06", "Moon.Knight.S01E06", "Moon.Knight.S01E05", "Moon.Knight.S01E05",
                    "Moon.Knight.S01E04", "Moon.Knight.S01E04", "Moon.Knight.S01E03", "Moon.Knight.S01E03",
                    "Moon.Knight.S01E02", "Moon.Knight.S01E02", "Moon.Knight.S01E01", "Moon.Knight.S01E01"],
    "Marvel Studios: Legends (2021)": ["Marvel_Studios_Legends_S01E17", "Marvel.Studios.Legends.S01E16",
                                       "Marvel.Studios.Legends.S01E15", "Marvel Studios Legends S01E14",
                                       "Marvel.Studios.Legends.S01E13", "Marvel.Studios.LEGENDS.S01E12",
                                       "Marvel.Studios.LEGENDS.S01E11", "Marvel.Studios.LEGENDS.S01E10",
                                       "Marvel.Studios.Legends.S01E09", "Marvel.Stds.Legends.S01E08",
                                       "Marvel.Stds.Legends.S01E07", "Marvel.Studios.Legends.S01E06",
                                       "Marvel.Studios.Legends.S01E05", "Marvel.Studios.Legends.S01E04",
                                       "Marvel.Studios.Legends.S01E03", "Marvel.Studios.Legends.S01E02",
                                       "Marvel.Studios.Legends.S01E01"],
    "Spider-Man: No Way Home": ["Spider-Man.No.Way.Home.2021.1080p", "ספיידרמן: אין דרך הביתה 1080p"],
    "Eternals (2021)": ["Eternals.2021.UHD.1080p", "Eternals.2021.IMAX.1080p", "Eternals.2021.IMAX.1080p"],
    "Hawkeye (2021)": ["Hawkeye.S01E06", "Hawkeye.S01E06", "Hawkeye.S01E05", "Hawkeye.S01E05", "Hawkeye.S01E04",
                       "Hawkeye.S01E04", "Hawkeye.S01E03", "Hawkeye.S01E03", "Hawkeye.S01E02", "Hawkeye.S01E02",
                       "Hawkeye.2021.S01E01", "Hawkeye.2021.S01E01"],
    "Marvel's Hit-Monkey (2021)": ["Hit-Monkey.S01E10", "Hit-Monkey.S01E10", "Hit-Monkey.S01E09", "Hit-Monkey.S01E09",
                                   "Hit-Monkey.S01E08", "Hit-Monkey.S01E08", "Hit-Monkey.S01E07", "Hit-Monkey.S01E07",
                                   "Hit-Monkey.S01E06", "Hit-Monkey.S01E06", "Marvels.Hit-Monkey.S01E05",
                                   "Marvels_Hit_Monkey_S01E05", "Marvels_Hit_Monkey_S01E04",
                                   "Marvels_Hit_Monkey_S01E04",
                                   "Hit-Monkey.S01E03", "Hit-Monkey.S01E03", "Hit-Monkey.S01E02", "Hit-Monkey.S01E02",
                                   "Hit-Monkey.S01E01", "Hit-Monkey.S01E01"],
    "Venom: Let There Be Carnage (2021)": ["Venom.Let.There.Be.Carnage.2021.1080p",
                                           "Venom.Let.There.Be.Carnage.2021.1080p"],
    "Shang-Chi and the Legend of the Ten Rings (2021)": ["_Shang_Chi_And_The_Legend_Of_The_Ten_Rings_2021_1080p",
                                                         "Shang-Chi.2021.720p",
                                                         "Shang_Chi_And_The_Legend_Of_The_Ten_Rings_2021_1080p",
                                                         "Shang-Chi.2021.720p"],
    "What If...? (2021)": ["What.If.S01E09", "What.If.S01E09", "What.If.2021.S01E08", "What.If.2021.S01E08",
                           "What.If.2021.S01E07", "What.If.2021.S01E07", "What.If.2021.S01E06", "What.If.2021.S01E06",
                           "What.If.2021.S01E05", "What.If.2021.S01E05", "What.If.2021.S01E04", "What.If.2021.S01E04",
                           "What.If.2021.S01E03", "What.If.2021.S01E03", "What.If.2021.S01E02", "What.If.2021.S01E02",
                           "What.If.2021.S01E01", "What.If.2021.S01E01"],
    "Black Widow (2021)": ["Black.Widow.2021 WEBRip 1080p", "Black.Widow.2021 WEBRip 720p",
                           "Black.Widow.2021 WEBRip 1080p", "Black.Widow.2021 WEBRip 720p"],
    "Loki (2021)": ["Loki.S01E06", "Loki.S01E06", "Loki.S01E06", "Loki.S01E05", "Loki.S01E05", "Loki.S01E05",
                    "Loki.S01E04", "Loki.S01E04", "Loki.S01E04", "Loki.S01E03", "Loki.S01E03", "Loki.S01E03",
                    "Loki.S01E02", "Loki.S01E02", "Loki.S01E02", "Loki.S01E01", "Loki.S01E01", "Loki.S01E01"],
    "Marvel's M.O.D.O.K. (2021)": ["marvels.m.o.d.o.k.s01e10", "marvels.m.o.d.o.k.s01e09", "marvels.m.o.d.o.k.s01e08",
                                   "marvels.m.o.d.o.k.s01e07", "marvels.m.o.d.o.k.s01e06", "marvels.m.o.d.o.k.s01e05",
                                   "marvels.m.o.d.o.k.s01e04", "marvels.m.o.d.o.k.s01e03", "marvels.m.o.d.o.k.s01e02",
                                   "marvels.m.o.d.o.k.s01e01"],
    "The Falcon and the Winter Soldier (2020)": ["The.Falcon.and.The.Winter.Sol_r.S01E06",
                                                 "The.Falcon.and.The.Winter.Sol_r.S01E05",
                                                 "Falcon.and.The.Winter.Sol_r.S01E04",
                                                 "The.Falcon.and.The.Winter.Sol_r.S01E03",
                                                 "The.Falcon.and.the.Winter.So_r.S01E02",
                                                 "Falcon_&_Winter_Soldier_S01E01"],
    "WandaVision (2021)": ["WandaVision (2021)"]
}

dic_web_name_to_download_name = {
    "Ms.Marvel.S01E02": "Ms.Marvel.S01E02.1080p.DSNP.WEB-DL.DDP5.1.H.264-NTb.mp4",
    "Ms.Marvel.S01E02": "Ms.Marvel.S01E02.1080p.DSNP.WEB-DL.DDP5.1.H.264-NTb.mkv",
    "Ms_Marvel_S01E01": "Ms_Marvel_S01E01_Generation_Why_1080p_DSNP_WEB_DL_DDPA5_1_H_264.mp4",
    "Ms_Marvel_S01E01": "Ms_Marvel_S01E01_Generation_Why_1080p_DSNP_WEB_DL_DDPA5_1_H_264.mp4",
    "Marvel.Studios.Assembld.S01E09": "Marvel.Studios.Assembld.S01E09.The.Making.of.Moon.Knight.202.mkv",
    "Marvel_Studios_Assembled_S01E08": "Marvel_Studios_Assembled_S01E08_The_Making_of_Eternals_720p_10bit.mkv",
    "Marvel_Studios_Assembled_S01E07": "Marvel_Studios_Assembled_S01E07_The_Making_of_Hawkeye_720p_10bit.mkv",
    "Marvel.Studios.Assembled.S01E06": "Marvel.Studios.Assembled.S01E06.1080p.WEB.H264-KOGi.mp4",
    "Marvel.Studios.Assembled.S01E05": "Marvel.Studios.Assembled.S01E05.The.Making.of.What.If.720p.W.mp4",
    "Marvel.Studios.Assembled.S01E04": "Marvel.Studios.Assembled.S01E04.The.Making.of.Black.Widow.10.mkv",
    "ASSEMBLED.S01E03": "ASSEMBLED.S01E03.The_Making.of.Loki.720p.DSNP.WEB.mkv",
    "Marvel_Studios_Assembled_S01E02": "Marvel_Studios_Assembled_S01E02The_Falcon_and_The_Winter_Sol_r_720p.mp4",
    "Marvel_Studios:_Assembled_S01E01": "Marvel_Studios:_Assembled_S01E01_making_WandaVision_720p_@Disney.mkv",
    "F.F.S01E16": "F.F.S01E16.Leader.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E15": "F.F.S01E15.She-Hulk.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E14": "F.F.S01E14.Skaar.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E13": "F.F.S01E13.A-Bomb.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E12": "F.F.S01E12.Red.Hulk.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E11": "F.F.S01E11.Sinister.Six.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E10": "F.F.S01E10.Goblin.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E09": "F.F.S01E09.Coulson.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E08": "F.F.S01E08.Doctor.Octopus.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZ.mkv",
    "F.F.S01E07": "F.F.S01E07.The.Skrulls.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E06": "F.F.S01E06.Black.Panther.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E05": "F.F.S01E05.White.Tiger.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E04": "F.F.S01E04.Hawkeye.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E03": "F.F.S01E03.Nova.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E02": "F.F.S01E02.Power-Man.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "F.F.S01E01": "F.F.S01E01.Iron.Fist.1080p.DSNP.WEB-DL.DDP5.1.H.264-LAZY.mkv",
    "Morbius.2022.1080p": "Morbius.2022.1080p.WEB-DL.mp4",
    "Morbius.2022.1080p": "Morbius.2022.1080p.WEB-DL.mp4",
    "Moon.Knight.S01E06": "Moon.Knight.S01E06.1080p.mkv",
    "Moon.Knight.S01E06": "Moon.Knight.S01E06.1080p.mkv",
    "Moon.Knight.S01E05": "Moon.Knight.S01E05.1080p.mkv",
    "Moon.Knight.S01E05": "Moon.Knight.S01E05.1080p.mkv",
    "Moon.Knight.S01E04": "Moon.Knight.S01E04.1080p.WEB.DL.mkv",
    "Moon.Knight.S01E04": "Moon.Knight.S01E04.1080p.WEB.DL.mkv",
    "Moon.Knight.S01E03": "Moon.Knight.S01E03.1080p.WEB.h264-KOGi.mkv",
    "Moon.Knight.S01E03": "Moon.Knight.S01E03.1080p.WEB.h264-KOGi.mkv",
    "Moon.Knight.S01E02": "Moon.Knight.S01E02.1080p.DSNP.WEB-DL.DDP5.1.Atmos.H.264-TBD.mkv",
    "Moon.Knight.S01E02": "Moon.Knight.S01E02.1080p.DSNP.WEB-DL.DDP5.1.Atmos.H.264-TBD.mp4",
    "Moon.Knight.S01E01": "Moon.Knight.S01E01.1080p.DSNP.WEB.DL.DDP.5.1.mkv",
    "Moon.Knight.S01E01": "Moon.Knight.S01E01.1080p.DSNP.WEB.DL.DDP.5.1.mp4",
    "Marvel_Studios_Legends_S01E17": "Marvel_Studios_Legends_S01E17_Scarlet_Witch_720p_DSNP_WEB_DL_1.mp4",
    "Marvel.Studios.Legends.S01E16": "Marvel.Studios.Legends.S01E16.Wong.720p.DSNP.WEB-DL.DDP5.1.A.mp4",
    "Marvel.Studios.Legends.S01E15": "Marvel.Studios.Legends.S01E15.Doctor.Strange.720p.DSNP.WEB-D.mp4",
    "Marvel Studios Legends S01E14": "Marvel Studios Legends S01E14 1080p.mkv",
    "Marvel.Studios.Legends.S01E13": "Marvel.Studios.Legends.S01E13.HSUBS.1080p.WEB-DL.H264-LAZY.mp4",
    "Marvel.Studios.LEGENDS.S01E12": "Marvel.Studios.LEGENDS.S01E12.The.Ravagers.1080p.DSNP.WEB-DL.mp4",
    "Marvel.Studios.LEGENDS.S01E11": "Marvel.Studios.LEGENDS.S01E11.The.Avengers.Initiative.1080p.mp4",
    "Marvel.Studios.LEGENDS.S01E10": "Marvel.Studios.LEGENDS.S01E10.Peggy.Carter.1080p.DSNP.WEB-DL.mp4",
    "Marvel.Studios.Legends.S01E09": "Marvel.Studios.Legends.S01E09.HEBSUBBED.1080p.WEB.H264-KOGi.mp4",
    "Marvel.Stds.Legends.S01E08": "Marvel.Stds.Legends.S01E08.1080p.WEB-DL.heb.subs.H264-LAZY.mp4",
    "Marvel.Stds.Legends.S01E07": "Marvel.Stds.Legends.S01E07.1080p.WEB-DL.heb.subs.H264-LAZY.mp4",
    "Marvel.Studios.Legends.S01E06": "Marvel.Studios.Legends.S01E06.720p.@Disney_Plus_il.mp4",
    "Marvel.Studios.Legends.S01E05": "Marvel.Studios.Legends.S01E05.720p.@Disney_Plus_il.mp4",
    "Marvel.Studios.Legends.S01E04": "Marvel.Studios.Legends.S01E04.720p.WEB.@Disney_Plus_il.mkv",
    "Marvel.Studios.Legends.S01E03": "Marvel.Studios.Legends.S01E03.720p.WEB.@Disney_Plus_il.mkv",
    "Marvel.Studios.Legends.S01E02": "Marvel.Studios.Legends.S01E02.1080p.ל.ת.@Disney_plus_il.mp4",
    "Marvel.Studios.Legends.S01E01": "Marvel.Studios.Legends.S01E01.1080p.@Disney_plus_il.mp4",
    "Spider-Man.No.Way.Home.2021.1080p": "Spider-Man.No.Way.Home.2021.1080p.BluRay.H264.AAC-RARBG.mp4",
    "ספיידרמן: אין דרך הביתה 1080p": "ספיידרמן: אין דרך הביתה 1080p BluRay.mp4",
    "Eternals.2021.UHD.1080p": "Eternals.2021.UHD.1080p.BluRay.DV.HDR.DDP.7.1.X265-SPHD.mkv",
    "Eternals.2021.IMAX.1080p": "Eternals.2021.IMAX.1080p.DSNP.WEB-DL.HebSub.H.264-TEPES.mp4",
    "Eternals.2021.IMAX.1080p": "Eternals.2021.IMAX.1080p.DSNP.WEB-DL.HebSub.H.264-TEPES.mp4",
    "Hawkeye.S01E06": "Hawkeye.S01E06.1080p.DSNP.WEB-DL.HSUBS.DDP5.1.x264-TEPES.mp4",
    "Hawkeye.S01E06": "Hawkeye.S01E06.1080p.DSNP.WEB-DL.HSUBS.DDP5.1.x264-TEPES.mp4",
    "Hawkeye.S01E05": "Hawkeye.S01E05.1080p.DSNP.WEB-DL.HSUBS.DDP5.1.x264-TEPES.mp4",
    "Hawkeye.S01E05": "Hawkeye.S01E05.1080p.DSNP.WEB-DL.HSUBS.DDP5.1.x264-TEPES.mp4",
    "Hawkeye.S01E04": "Hawkeye.S01E04.1080p.DSNP.WEB-DL.HSUBS.DDP5.1.x264-TEPES.mp4",
    "Hawkeye.S01E04": "Hawkeye.S01E04.1080p.DSNP.WEB-DL.HSUBS.DDP5.1.x264-TEPES.mp4",
    "Hawkeye.S01E03": "Hawkeye.S01E03.1080p.DSNP.WEB-DL.HSUBS.DDP5.1.x264-TEPES.mp4",
    "Hawkeye.S01E03": "Hawkeye.S01E03.1080p.DSNP.WEB-DL.HSUBS.DDP5.1.x264-TEPES.mp4",
    "Hawkeye.S01E02": "Hawkeye.S01E02.1080p.DSNP.WEB-DL.HSUBS.DDP5.1.x264-TEPES.mp4",
    "Hawkeye.S01E02": "Hawkeye.S01E02.1080p.DSNP.WEB-DL.HSUBS.DDP5.1.x264-TEPES.mp4",
    "Hawkeye.2021.S01E01": "Hawkeye.2021.S01E01.1080p.mkv",
    "Hawkeye.2021.S01E01": "Hawkeye.2021.S01E01.1080p.mkv",
    "Hit-Monkey.S01E10": "Hit-Monkey.S01E10.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E10": "Hit-Monkey.S01E10.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E09": "Hit-Monkey.S01E09.1080p.HULU.WEB-DL.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E09": "Hit-Monkey.S01E09.1080p.HULU.WEB-DL.DDP5.1.H.264-TEPES.mkv",
    "Hit-Monkey.S01E08": "Hit-Monkey.S01E08.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E08": "Hit-Monkey.S01E08.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E07": "Hit-Monkey.S01E07.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E07": "Hit-Monkey.S01E07.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E06": "Hit-Monkey.S01E06.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E06": "Hit-Monkey.S01E06.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Marvels.Hit-Monkey.S01E05": "Marvels.Hit-Monkey.S01E05.1080p.WEB-DL.H.264-TEPES.mp4",
    "Marvels_Hit_Monkey_S01E05": "Marvels_Hit_Monkey_S01E05_Run_Monkey_Run_1080p_HULU_WEB_DL_DDP5.mp4",
    "Marvels_Hit_Monkey_S01E04": "Marvels_Hit_Monkey_S01E04_The_Code_1080p_HULU_WEB_DL_DDP5_1_H_264.mp4",
    "Marvels_Hit_Monkey_S01E04": "Marvels_Hit_Monkey_S01E04_The_Code_1080p_HULU_WEB_DL_DDP5_1_H_264.mp4",
    "Hit-Monkey.S01E03": "Hit-Monkey.S01E03.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E03": "Hit-Monkey.S01E03.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E02": "Hit-Monkey.S01E02.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E02": "Hit-Monkey.S01E02.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E01": "Hit-Monkey.S01E01.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Hit-Monkey.S01E01": "Hit-Monkey.S01E01.1080p.HULU.WEB-DL.HSUBS.DDP5.1.H.264-TEPES.mp4",
    "Venom.Let.There.Be.Carnage.2021.1080p": "Venom.Let.There.Be.Carnage.2021.1080p.BluRay.mkv",
    "Venom.Let.There.Be.Carnage.2021.1080p": "Venom.Let.There.Be.Carnage.2021.1080p.BluRay.mkv",
    "Marvel_Studios_2021_Disney_Plus_Day_Special_2021_1080p": "Marvel_Studios_2021_Disney_Plus_Day_Special_2021_1080p_WEB_h264.mp4",
    "The.Simpsons.in.Plusaversary.2021.1080p": "The.Simpsons.in.Plusaversary.2021.1080p.WEB.h264-KOGi.mp4",
    "_Shang_Chi_And_The_Legend_Of_The_Ten_Rings_2021_1080p": "_Shang_Chi_And_The_Legend_Of_The_Ten_Rings_2021_1080p_BluRay_x264.mp4",
    "Shang-Chi.2021.720p": "Shang-Chi.2021.720p.BluRay.x264-VETO.mp4",
    "Shang_Chi_And_The_Legend_Of_The_Ten_Rings_2021_1080p": "Shang_Chi_And_The_Legend_Of_The_Ten_Rings_2021_1080p_BluRay_x264.mp4",
    "Shang-Chi.2021.720p": "Shang-Chi.2021.720p.BluRay.x264-VETO.mp4",
    "Spider-Man.2017.S03E08": "Spider-Man.2017.S03E08 1080p .HebDub.@Disney_plus_il.mp4",
    "What.If.S01E09": "What.If.S01E09.1080p.mp4",
    "What.If.S01E09": "What.If.S01E09.1080p.mp4",
    "What.If.2021.S01E08": "What.If.2021.S01E08.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E08": "What.If.2021.S01E08.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E07": "What.If.2021.S01E07.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E07": "What.If.2021.S01E07.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E06": "What.If.2021.S01E06.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E06": "What.If.2021.S01E06.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E05": "What.If.2021.S01E05.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E05": "What.If.2021.S01E05.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E04": "What.If.2021.S01E04.720p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E04": "What.If.2021.S01E04.720p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E03": "What.If.2021.S01E03.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E03": "What.If.2021.S01E03.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E02": "What.If.2021.S01E02.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E02": "What.If.2021.S01E02.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E01": "What.If.2021.S01E01.1080p.HEVC.x265 @Disney_Plus_il.mp4",
    "What.If.2021.S01E01": "What.If.2021.S01E01.1080p.HEVC.x265 Disney_Plus_il.mp4",
    "Black.Widow.2021 WEBRip 1080p": "Black.Widow.2021 WEBRip 1080p @Disney_Plus_il.mp4",
    "Black.Widow.2021 WEBRip 720p": "Black.Widow.2021 WEBRip 720p @Disney_Plus_il.mp4",
    "Black.Widow.2021 WEBRip 1080p": "Black.Widow.2021 WEBRip 1080p @Disney_Plus_il.mp4",
    "Black.Widow.2021 WEBRip 720p": "Black.Widow.2021 WEBRip 720p @Disney_Plus_il.mp4",
    "The.Good.The.Bart.and.The.Loki.2021.1080p": "The.Good.The.Bart.and.The.Loki.2021.1080p.@Disney_Plus_il.mp4",
    "The.Good.The.Bart.and.The.Loki.2021.1080p": "The.Good.The.Bart.and.The.Loki.2021.1080p.@Disney_Plus_il.mp4",
    "Loki.S01E06": "Loki.S01E06.1080p.@Disney_plus_il.mp4",
    "Loki.S01E06": "Loki.S01E06.1080p.@Disney_plus_il.mp4",
    "Loki.S01E05": "Loki.S01E05.1080p.x265.@Disney_plus_il.mp4",
    "Loki.S01E05": "Loki.S01E05.1080p.x265.@Disney_plus_il.mp4",
    "Loki.S01E04": "Loki.S01E04.1080p.HEVC.x265-Me.@Disney_plus_il.mp4",
    "Loki.S01E04": "Loki.S01E04.1080p.HEVC.x265-Me.@Disney_plus_il.mp4",
    "Loki.S01E03": "Loki.S01E03.1080p.x265.@Disney_Plus_il.mp4",
    "Loki.S01E03": "Loki.S01E03.1080p.x265.@Disney_Plus_il.mp4",
    "Loki.S01E02": "Loki.S01E02.1080p.@Disney_plus_il.mp4",
    "Loki.S01E02": "Loki.S01E02.1080p.@Disney_plus_il.mp4",
    "Loki.S01E01": "Loki.S01E01.1080p.@Disney_plus_il.mp4",
    "Loki.S01E01": "Loki.S01E01.1080p.@Disney_plus_il.mp4",
    "marvels.m.o.d.o.k.s01e10": "marvels.m.o.d.o.k.s01e10.readnfo.1080p.web.h264-ggez.mkv",
    "marvels.m.o.d.o.k.s01e09": "marvels.m.o.d.o.k.s01e09.readnfo.1080p.web.h264-ggez.mkv",
    "marvels.m.o.d.o.k.s01e08": "marvels.m.o.d.o.k.s01e08.readnfo.1080p.web.h264-ggez.mkv",
    "marvels.m.o.d.o.k.s01e07": "marvels.m.o.d.o.k.s01e07.readnfo.1080p.web.h264-ggez.mkv",
    "marvels.m.o.d.o.k.s01e06": "marvels.m.o.d.o.k.s01e06.readnfo.1080p.web.h264-ggez.mkv",
    "marvels.m.o.d.o.k.s01e05": "marvels.m.o.d.o.k.s01e05.1080p.web.h264-ggez.mkv",
    "marvels.m.o.d.o.k.s01e04": "marvels.m.o.d.o.k.s01e04.readnfo.1080p.web.h264-ggez.mkv",
    "marvels.m.o.d.o.k.s01e03": "marvels.m.o.d.o.k.s01e03.1080p.web.h264-ggwp.mkv",
    "marvels.m.o.d.o.k.s01e02": "marvels.m.o.d.o.k.s01e02.1080p.web.h264-glhf.mkv",
    "marvels.m.o.d.o.k.s01e01": "marvels.m.o.d.o.k.s01e01.1080p.web.h264-ggwp.mkv",
    "The.Falcon.and.The.Winter.Sol_r.S01E06": "The.Falcon.and.The.Winter.Sol_r.S01E06.1080p.@Disney_plus_il.mp4",
    "The.Falcon.and.The.Winter.Sol_r.S01E05": "The.Falcon.and.The.Winter.Sol_r.S01E05.1080p.@Disney_plus_il.mp4",
    "Falcon.and.The.Winter.Sol_r.S01E04": "Falcon.and.The.Winter.Sol_r.S01E04.1080p.mp4",
    "The.Falcon.and.The.Winter.Sol_r.S01E03": "The.Falcon.and.The.Winter.Sol_r.S01E03.1080p.@Disney_plus_il.mp4",
    "The.Falcon.and.the.Winter.So_r.S01E02": "The.Falcon.and.the.Winter.So_r.S01E02.1080p.WEBRip.H264.mp4",
    "Falcon_&_Winter_Soldier_S01E01": "Falcon_&_Winter_Soldier_S01E01_1080p_WEBRip_heb.mp4",
    "WandaVision (2021)": "WandaVision (2021)"
}

dic_vids_id = {"Ms.Marvel.S01E02": "4897",
               "Ms.Marvel.S01E02": "4896",
               "Ms_Marvel_S01E01": "4891",
               "Ms_Marvel_S01E01": "4889",
               "Marvel.Studios.Assembld.S01E09": "4879",
               "Marvel_Studios_Assembled_S01E08": "4878",
               "Marvel_Studios_Assembled_S01E07": "4877",
               "Marvel.Studios.Assembled.S01E06": "4876",
               "Marvel.Studios.Assembled.S01E05": "4875",
               "Marvel.Studios.Assembled.S01E04": "4874",
               "ASSEMBLED.S01E03": "4873",
               "Marvel_Studios_Assembled_S01E02": "4872",
               "Marvel_Studios:_Assembled_S01E01": "4871",
               "F.F.S01E16": "4867",
               "F.F.S01E15": "4866",
               "F.F.S01E14": "4865",
               "F.F.S01E13": "4864",
               "F.F.S01E12": "4863",
               "F.F.S01E11": "4862",
               "F.F.S01E10": "4861",
               "F.F.S01E09": "4860",
               "F.F.S01E08": "4859",
               "F.F.S01E07": "4858",
               "F.F.S01E06": "4857",
               "F.F.S01E05": "4856",
               "F.F.S01E04": "4855",
               "F.F.S01E03": "4854",
               "F.F.S01E02": "4853",
               "F.F.S01E01": "4852",
               "Morbius.2022.1080p": "4848",
               "Morbius.2022.1080p": "4846",
               "Moon.Knight.S01E06": "4829",
               "Moon.Knight.S01E06": "4828",
               "Moon.Knight.S01E05": "4814",
               "Moon.Knight.S01E05": "4813",
               "Moon.Knight.S01E04": "4812",
               "Moon.Knight.S01E04": "4811",
               "Moon.Knight.S01E03": "4810",
               "Moon.Knight.S01E03": "4809",
               "Moon.Knight.S01E02": "4808",
               "Moon.Knight.S01E02": "4807",
               "Moon.Knight.S01E01": "4806",
               "Moon.Knight.S01E01": "4805",
               "Marvel_Studios_Legends_S01E17": "4802",
               "Marvel.Studios.Legends.S01E16": "4801",
               "Marvel.Studios.Legends.S01E15": "4800",
               "Marvel Studios Legends S01E14": "4792",
               "Marvel.Studios.Legends.S01E13": "4791",
               "Marvel.Studios.LEGENDS.S01E12": "4790",
               "Marvel.Studios.LEGENDS.S01E11": "4789",
               "Marvel.Studios.LEGENDS.S01E10": "4788",
               "Marvel.Studios.Legends.S01E09": "4787",
               "Marvel.Stds.Legends.S01E08": "4786",
               "Marvel.Stds.Legends.S01E07": "4785",
               "Marvel.Studios.Legends.S01E06": "4784",
               "Marvel.Studios.Legends.S01E05": "4783",
               "Marvel.Studios.Legends.S01E04": "4782",
               "Marvel.Studios.Legends.S01E03": "4781",
               "Marvel.Studios.Legends.S01E02": "4780",
               "Marvel.Studios.Legends.S01E01": "4779",
               "Spider-Man.No.Way.Home.2021.1080p": "4710",
               "ספיידרמן: אין דרך הביתה 1080p": "4709",
               "Eternals.2021.UHD.1080p": "4631",
               "Eternals.2021.IMAX.1080p": "4627",
               "Eternals.2021.IMAX.1080p": "4626",
               "Hawkeye.S01E06": "4599",
               "Hawkeye.S01E06": "4598",
               "Hawkeye.S01E05": "4597",
               "Hawkeye.S01E05": "4596",
               "Hawkeye.S01E04": "4563",
               "Hawkeye.S01E04": "4562",
               "Hawkeye.S01E03": "4561",
               "Hawkeye.S01E03": "4560",
               "Hawkeye.S01E02": "4559",
               "Hawkeye.S01E02": "4558",
               "Hawkeye.2021.S01E01": "4557",
               "Hawkeye.2021.S01E01": "4556",
               "Hit-Monkey.S01E10": "4537",
               "Hit-Monkey.S01E10": "4536",
               "Hit-Monkey.S01E09": "4525",
               "Hit-Monkey.S01E09": "4524",
               "Hit-Monkey.S01E08": "4523",
               "Hit-Monkey.S01E08": "4522",
               "Hit-Monkey.S01E07": "4507",
               "Hit-Monkey.S01E07": "4506",
               "Hit-Monkey.S01E06": "4505",
               "Hit-Monkey.S01E06": "4504",
               "Marvels.Hit-Monkey.S01E05": "4498",
               "Marvels_Hit_Monkey_S01E05": "4497",
               "Marvels_Hit_Monkey_S01E04": "4496",
               "Marvels_Hit_Monkey_S01E04": "4495",
               "Hit-Monkey.S01E03": "4494",
               "Hit-Monkey.S01E03": "4493",
               "Hit-Monkey.S01E02": "4492",
               "Hit-Monkey.S01E02": "4491",
               "Hit-Monkey.S01E01": "4490",
               "Hit-Monkey.S01E01": "4489",
               "Venom.Let.There.Be.Carnage.2021.1080p": "4472",
               "Venom.Let.There.Be.Carnage.2021.1080p": "4471",
               "Marvel_Studios_2021_Disney_Plus_Day_Special_2021_1080p": "4434",
               "The.Simpsons.in.Plusaversary.2021.1080p": "4432",
               "_Shang_Chi_And_The_Legend_Of_The_Ten_Rings_2021_1080p": "4429",
               "Shang-Chi.2021.720p": "4428",
               "Shang_Chi_And_The_Legend_Of_The_Ten_Rings_2021_1080p": "4427",
               "Shang-Chi.2021.720p": "4426",
               "Spider-Man.2017.S03E08": "4370",
               "What.If.S01E09": "4352",
               "What.If.S01E09": "4351",
               "What.If.2021.S01E08": "4342",
               "What.If.2021.S01E08": "4341",
               "What.If.2021.S01E07": "4334",
               "What.If.2021.S01E07": "4333",
               "What.If.2021.S01E06": "4325",
               "What.If.2021.S01E06": "4324",
               "What.If.2021.S01E05": "4323",
               "What.If.2021.S01E05": "4322",
               "What.If.2021.S01E04": "4321",
               "What.If.2021.S01E04": "4320",
               "What.If.2021.S01E03": "4319",
               "What.If.2021.S01E03": "4318",
               "What.If.2021.S01E02": "4317",
               "What.If.2021.S01E02": "4316",
               "What.If.2021.S01E01": "4315",
               "What.If.2021.S01E01": "4314",
               "Black.Widow.2021 WEBRip 1080p": "4190",
               "Black.Widow.2021 WEBRip 720p": "4189",
               "Black.Widow.2021 WEBRip 1080p": "4188",
               "Black.Widow.2021 WEBRip 720p": "4187",
               "The.Good.The.Bart.and.The.Loki.2021.1080p": "4184",
               "The.Good.The.Bart.and.The.Loki.2021.1080p": "4183",
               "Loki.S01E06": "4155",
               "Loki.S01E06": "4154",
               "Loki.S01E05": "4102",
               "Loki.S01E05": "4101",
               "Loki.S01E04": "4062",
               "Loki.S01E04": "4061",
               "Loki.S01E03": "4044",
               "Loki.S01E03": "4043",
               "Loki.S01E02": "4032",
               "Loki.S01E02": "4030",
               "Loki.S01E01": "4023",
               "Loki.S01E01": "4020",
               "marvels.m.o.d.o.k.s01e10": "3974",
               "marvels.m.o.d.o.k.s01e09": "3973",
               "marvels.m.o.d.o.k.s01e08": "3972",
               "marvels.m.o.d.o.k.s01e07": "3971",
               "marvels.m.o.d.o.k.s01e06": "3970",
               "marvels.m.o.d.o.k.s01e05": "3969",
               "marvels.m.o.d.o.k.s01e04": "3968",
               "marvels.m.o.d.o.k.s01e03": "3967",
               "marvels.m.o.d.o.k.s01e02": "3966",
               "marvels.m.o.d.o.k.s01e01": "3965",
               "The.Falcon.and.The.Winter.Sol_r.S01E06": "3931",
               "The.Falcon.and.The.Winter.Sol_r.S01E05": "3923",
               "Falcon.and.The.Winter.Sol_r.S01E04": "3922",
               "The.Falcon.and.The.Winter.Sol_r.S01E03": "3920",
               "The.Falcon.and.the.Winter.So_r.S01E02": "3919",
               "Falcon_&_Winter_Soldier_S01E01": "3917",
               "WandaVision (2021)": "3653"}


# authentication must be before calling this function.
def get_photos():
    with TelegramClient('name', api_id, api_hash) as client:
        result = client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=500,
            hash=0,
        ))
        for iter in range(1):

            # Title for group chat
            for chat in result.chats:
                # print(chat)
                if chat.id == 1443445743:
                    messages = client.get_messages(chat, limit=1200)

                    # dowload_media(file/id)
                    # messages[10].download_media('')
                    counter = 0
                    print("loading..")
                    num_of_des = 0
                    num_of_img = 0

                    for message in messages:

                        # Media:
                        #
                        # POLL:
                        # if type(message.poll) == telethon.tl.types.MessageMediaPoll:
                        #     polls.append(message.poll)
                        # elif message.button_count > 0:
                        #     navigation.append(message)
                        #
                        # PHOTO
                        if type(message.media) == telethon.tl.types.MessageMediaPhoto:
                            name = message.message.split('\n')[1]
                            if name == "":
                                continue
                            all = message.message.split('\n')
                            for i in range(len(all)):
                                if 'תקציר:' in all[i]:
                                    with open('static/texts/' + name + '.txt', 'w') as f:
                                        f.write(all[i + 1])
                                        num_of_des += 1
                                    try:
                                        message.download_media('static/themeImages/' + name + '.jpeg')
                                        num_of_img += 1
                                    except:
                                        # if there is a problem in telegram, img could be not downloaded
                                        # make a black background img instead
                                        img = Image.new("RGB", (800, 800), (0, 0, 0))
                                        img.save('static/themeImages/' + name + '.jpeg', "JPEG")
                                        num_of_img += 1

                                    # print('"' + name + '"')
                                    break

                        # VIDEO or and gifs and somthing else(?)
                        # look by the next message after image object
                        if type(message.media) == telethon.tl.types.MessageMediaDocument:
                            text = message.message.split('\n')
                            if len(text) == 1:
                                continue
                            size = len(message.media.document.attributes)
                            try:
                                name = message.media.document.attributes[size - 1].file_name
                            except:
                                #     not a movie/series
                                x = 3
                            try:
                                splited_name = re.split(r"(?<=s[0-9][0-9]e[0-9][0-9])([\s\S]*)$", name)
                                splited_name_doublecheck_series = re.split(r"(?<=S[0-9][0-9]E[0-9][0-9])([\s\S]*)$",
                                                                           splited_name[0])
                                # 720p
                                splited_movie = re.split(r"(?<=[0-9][0-9][0]p)([\s\S]*)$",
                                                         splited_name_doublecheck_series[0])
                                # 1080
                                splited_movie_doublecheck = re.split(r"(?<=[0-9][0][0-9][0]p)([\s\S]*)$",
                                                                     splited_movie[0])

                            except:
                                # it's not a movie, nor a series
                                z = 3
                            print('"' + splited_movie_doublecheck[0] + '"' + ' : ' + '"' + name + '"')

                            counter += 1

                        # print()
                        # print("_____________________")
                        # print(message.raw_text)
                        # print("_____________________")
                        # print()
                    if num_of_des == num_of_img:
                        print("done.")
                    else:
                        print("some img of des was not loaded properly.")


# get_photos()


def download_media(unique_name):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with TelegramClient('name', api_id, api_hash, loop=loop) as client:
        result = client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=500,
            hash=0,
        ))
        # Title for group chat
        for chat in result.chats:
            # print(chat)
            if chat.id == 1443445743:
                messages = client.get_messages(chat, limit=1000)

                # dowload_media(file/id)
                # messages[10].download_media('')
                counter = 0
                print("loading..")
                num_of_des = 0
                num_of_img = 0

                for message in messages:
                    # get id from dic
                    id = dic_vids_id.get(unique_name)
                    # turn to int
                    id = int(id)
                    if message.id == id:
                        # download_media
                        message.download_media('static/videos/')
                        print("done.")

# download_media("What.If.2021.S01E04")



# authentication must be before calling this function.
def get_photos2():
    with TelegramClient('name', api_id, api_hash) as client:
        result = client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=500,
            hash=0,
        ))
        for iter in range(1):

            # Title for group chat
            for chat in result.chats:
                # print(chat)
                if chat.id == 1443445743:
                    messages = client.get_messages(chat, limit=None)

                    # dowload_media(file/id)
                    # messages[10].download_media('')
                    counter = 0
                    print("loading..")
                    num_of_des = 0
                    num_of_img = 0


                    names_and_episods = {}
                    # key_name will be used for making a new key for dic
                    key_name = ""
                    dic_flag = False

                    mes = messages[::-1]
                    for message in messages[::-1]:

                        # Media:
                        #
                        # POLL:
                        # if type(message.poll) == telethon.tl.types.MessageMediaPoll:
                        #     polls.append(message.poll)
                        # elif message.button_count > 0:
                        #     navigation.append(message)
                        #
                        # PHOTO
                        if type(message.media) == telethon.tl.types.MessageMediaPhoto:
                            name = message.message.split('\n')[1]
                            if name == "":
                                # flag false
                                dic_flag = False
                                continue
                            all = message.message.split('\n')
                            for i in range(len(all)):
                                if 'תקציר:' in all[i]:  # because there is no takzir iron manis not going in. need to rethink it.
                                    with open('static/texts/' + name + '.txt', 'w') as f:
                                        f.write(all[i + 1])
                                        num_of_des += 1
                                    try:
                                        message.download_media('static/themeImages/' + name + '.jpeg')
                                        num_of_img += 1
                                    except:
                                        # if there is a problem in telegram, img could be not downloaded
                                        # make a black background img instead
                                        img = Image.new("RGB", (800, 800), (0, 0, 0))
                                        img.save('static/themeImages/' + name + '.jpeg', "JPEG")

                                        num_of_img += 1

                                    # make key and value would be a list
                                    key_name = name
                                    names_and_episods[key_name] = []

                                    # flag true
                                    dic_flag = True

                                    # print('"' + name + '"')
                                    break
                                else:
                                    # no Description
                                    dic_flag = False

                        # VIDEO or and gifs and somthing else(?)
                        # look by the next message after image object
                        if type(message.media) == telethon.tl.types.MessageMediaDocument and dic_flag:
                            add_flag = True
                            text = message.message.split('\n')
                            for i in range(len(text)):
                                if 'תקציר:' in text[i]:
                                    add_flag = False
                            if add_flag:
                                if len(text) == 1:
                                    continue
                                size = len(message.media.document.attributes)
                                try:
                                    file_name = message.media.document.attributes[size - 1].file_name
                                except:
                                    #     not a movie/series
                                    x = 3
                                try:
                                    splited_name = re.split(r"(?<=s[0-9][0-9]e[0-9][0-9])([\s\S]*)$", file_name)
                                    splited_name_doublecheck_series = re.split(r"(?<=S[0-9][0-9]E[0-9][0-9])([\s\S]*)$",
                                                                               splited_name[0])
                                    # 720p
                                    splited_movie = re.split(r"(?<=[0-9][0-9][0]p)([\s\S]*)$",
                                                             splited_name_doublecheck_series[0])
                                    # 1080
                                    splited_movie_doublecheck = re.split(r"(?<=[0-9][0][0-9][0]p)([\s\S]*)$",
                                                                         splited_movie[0])

                                    if key_name != "":
                                        names_and_episods[key_name].append(splited_movie_doublecheck[0])
                                    z=2

                                except:
                                    # it's not a movie, nor a series
                                    z = 3
                                # print('"' + splited_movie_doublecheck[0] + '"' + ' : ' + '"' + file_name + '"')

                                counter += 1

                        # print()
                        # print("_____________________")
                        # print(message.raw_text)
                        # print("_____________________")
                        # print()
                    if num_of_des == num_of_img:
                        print("done.")
                    else:
                        print("some img of des was not loaded properly.")

get_photos2()
