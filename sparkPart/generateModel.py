#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-17 10:39:25
# @Author  : guanglinzhou (xdzgl812@163.com)
# @Link    : https://github.com/GuanglinZhou
# @Version : $Id$


'''

使用RF训练hdfs://master:9000//trainDataDir/trainData_xxx.csv文件

'''

# from __future__ import print_function

from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors
import random
import time

if __name__ == '__main__':
    start = time.time()
    spark = SparkSession.builder.appName("generateCompleteTrainModel").getOrCreate()
    sc = spark.sparkContext
    # gridIDHaveData = sc.textFile('hdfs://master:9000//sparkExperiment/gridIDHaveData.txt')
    # gridIDHaveData = gridIDHaveData.map(lambda line: line.split(','))
    # gridIDHaveDataList = gridIDHaveData.first()

    gridIDHaveDataList = [37826, 38116, 39276, 40663, 40664, 40954, 41245, 41246, 42427, 42428, 42439, 42440, 42730,
                          42733, 42990, 43603, 43608, 43680, 43893, 43907, 43910, 43911, 43914, 43917, 43918, 43919,
                          44155, 44189, 44207, 44447, 44479, 44484, 44490, 44497, 44737, 44747, 44770, 44772, 44780,
                          44781, 44782, 44784, 44785, 44786, 44787, 44788, 44789, 45031, 45032, 45036, 45061, 45062,
                          45063, 45070, 45071, 45074, 45075, 45076, 45077, 45078, 45079, 45083, 45140, 45320, 45321,
                          45322, 45326, 45352, 45353, 45363, 45364, 45366, 45367, 45368, 45373, 45374, 45610, 45611,
                          45612, 45613, 45616, 45617, 45619, 45620, 45635, 45637, 45638, 45641, 45642, 45643, 45644,
                          45654, 45656, 45657, 45658, 45663, 45664, 45901, 45902, 45903, 45904, 45905, 45906, 45907,
                          45909, 45910, 45914, 45928, 45929, 45930, 45932, 45933, 45935, 45936, 45937, 45941, 45942,
                          45943, 45944, 45945, 45946, 45947, 45948, 45949, 45952, 45953, 45954, 45956, 45957, 46192,
                          46193, 46194, 46195, 46196, 46197, 46198, 46199, 46200, 46201, 46213, 46219, 46220, 46222,
                          46223, 46224, 46225, 46226, 46227, 46228, 46229, 46230, 46231, 46232, 46234, 46235, 46236,
                          46237, 46238, 46243, 46244, 46247, 46480, 46483, 46484, 46485, 46486, 46487, 46489, 46490,
                          46491, 46503, 46509, 46510, 46513, 46519, 46520, 46521, 46522, 46523, 46524, 46525, 46526,
                          46527, 46528, 46534, 46772, 46773, 46774, 46775, 46776, 46777, 46779, 46780, 46789, 46790,
                          46791, 46792, 46793, 46796, 46797, 46798, 46799, 46800, 46809, 46812, 46814, 46815, 46816,
                          46817, 46818, 46819, 46820, 46821, 46822, 46823, 46824, 47061, 47062, 47063, 47064, 47065,
                          47066, 47067, 47070, 47071, 47072, 47073, 47078, 47081, 47083, 47089, 47090, 47093, 47099,
                          47100, 47101, 47102, 47103, 47104, 47105, 47106, 47107, 47351, 47355, 47356, 47357, 47358,
                          47360, 47361, 47368, 47371, 47373, 47376, 47377, 47378, 47379, 47380, 47381, 47382, 47383,
                          47384, 47386, 47387, 47388, 47389, 47390, 47391, 47392, 47393, 47394, 47396, 47410, 47411,
                          47645, 47647, 47648, 47649, 47650, 47651, 47653, 47658, 47659, 47660, 47661, 47663, 47669,
                          47670, 47671, 47673, 47674, 47675, 47676, 47677, 47680, 47681, 47682, 47683, 47684, 47685,
                          47686, 47700, 47938, 47939, 47940, 47947, 47948, 47949, 47950, 47951, 47952, 47953, 47956,
                          47957, 47958, 47959, 47960, 47962, 47963, 47964, 47970, 47971, 47972, 47973, 47974, 47979,
                          47984, 48229, 48230, 48231, 48239, 48240, 48243, 48251, 48253, 48254, 48260, 48261, 48263,
                          48264, 48265, 48267, 48268, 48269, 48270, 48272, 48274, 48278, 48519, 48520, 48521, 48529,
                          48530, 48531, 48532, 48533, 48536, 48537, 48538, 48540, 48542, 48543, 48551, 48553, 48554,
                          48555, 48556, 48557, 48558, 48559, 48560, 48562, 48564, 48566, 48567, 48568, 48569, 48804,
                          48808, 48809, 48810, 48811, 48813, 48814, 48815, 48819, 48820, 48821, 48823, 48829, 48830,
                          48831, 48833, 48841, 48843, 48844, 48845, 48846, 48847, 48848, 48849, 48850, 48851, 48852,
                          48854, 48857, 48859, 49050, 49095, 49096, 49097, 49098, 49099, 49100, 49101, 49102, 49104,
                          49105, 49108, 49109, 49110, 49111, 49113, 49119, 49120, 49121, 49123, 49128, 49131, 49132,
                          49134, 49135, 49136, 49137, 49138, 49139, 49140, 49141, 49142, 49143, 49144, 49145, 49149,
                          49385, 49387, 49388, 49389, 49390, 49391, 49392, 49395, 49396, 49397, 49398, 49399, 49401,
                          49408, 49409, 49410, 49412, 49413, 49418, 49419, 49422, 49423, 49424, 49425, 49426, 49427,
                          49428, 49429, 49430, 49431, 49432, 49433, 49434, 49440, 49455, 49631, 49632, 49672, 49676,
                          49677, 49678, 49679, 49680, 49683, 49684, 49686, 49687, 49689, 49690, 49691, 49692, 49693,
                          49694, 49696, 49705, 49708, 49709, 49710, 49712, 49713, 49714, 49715, 49716, 49717, 49718,
                          49719, 49720, 49721, 49722, 49723, 49724, 49922, 49955, 49962, 49967, 49968, 49970, 49971,
                          49974, 49976, 49977, 49978, 49979, 49980, 49982, 49983, 49984, 49985, 49986, 49987, 49988,
                          49989, 49992, 49993, 49995, 49997, 49998, 49999, 50000, 50003, 50004, 50005, 50006, 50007,
                          50008, 50009, 50010, 50011, 50012, 50013, 50014, 50033, 50062, 50212, 50213, 50245, 50247,
                          50249, 50260, 50268, 50269, 50271, 50272, 50273, 50278, 50279, 50282, 50283, 50286, 50287,
                          50293, 50294, 50295, 50296, 50297, 50298, 50299, 50300, 50301, 50302, 50303, 50323, 50501,
                          50502, 50503, 50504, 50540, 50541, 50560, 50561, 50563, 50568, 50569, 50570, 50571, 50572,
                          50573, 50574, 50575, 50576, 50590, 50592, 50791, 50794, 50836, 50850, 50851, 50854, 50858,
                          50859, 50860, 50862, 50863, 50864, 50865, 50866, 51085, 51118, 51119, 51122, 51125, 51126,
                          51136, 51137, 51138, 51141, 51142, 51143, 51144, 51145, 51146, 51147, 51148, 51149, 51150,
                          51151, 51152, 51153, 51155, 51383, 51386, 51387, 51413, 51419, 51424, 51425, 51427, 51430,
                          51431, 51432, 51433, 51434, 51435, 51436, 51437, 51438, 51440, 51442, 51443, 51463, 51464,
                          51465, 51496, 51519, 51678, 51681, 51703, 51709, 51710, 51713, 51714, 51717, 51720, 51722,
                          51723, 51752, 51753, 51754, 51756, 51765, 51766, 51776, 51809, 51969, 51970, 51971, 51989,
                          51990, 52000, 52003, 52006, 52012, 52013, 52017, 52018, 52020, 52022, 52023, 52024, 52027,
                          52028, 52044, 52045, 52046, 52047, 52048, 52050, 52051, 52052, 52054, 52055, 52056, 52093,
                          52103, 52105, 52261, 52271, 52277, 52278, 52279, 52280, 52281, 52282, 52283, 52284, 52285,
                          52288, 52293, 52296, 52302, 52303, 52304, 52305, 52306, 52307, 52308, 52309, 52310, 52313,
                          52314, 52318, 52319, 52320, 52334, 52335, 52336, 52337, 52345, 52357, 52366, 52382, 52389,
                          52566, 52567, 52568, 52569, 52570, 52571, 52577, 52583, 52586, 52590, 52591, 52592, 52594,
                          52595, 52596, 52599, 52600, 52602, 52603, 52604, 52605, 52609, 52610, 52611, 52624, 52625,
                          52627, 52628, 52629, 52630, 52631, 52632, 52633, 52634, 52635, 52636, 52637, 52638, 52639,
                          52640, 52641, 52642, 52643, 52644, 52647, 52846, 52847, 52848, 52852, 52853, 52857, 52860,
                          52862, 52873, 52874, 52875, 52876, 52877, 52878, 52879, 52880, 52881, 52883, 52884, 52885,
                          52889, 52890, 52895, 52896, 52899, 52914, 52915, 52917, 52918, 52919, 52920, 52921, 52922,
                          52923, 52924, 52933, 52937, 53136, 53137, 53138, 53143, 53147, 53152, 53164, 53166, 53167,
                          53168, 53169, 53170, 53171, 53172, 53173, 53174, 53176, 53177, 53178, 53179, 53180, 53187,
                          53188, 53189, 53203, 53204, 53205, 53206, 53207, 53209, 53210, 53211, 53212, 53214, 53227,
                          53228, 53429, 53433, 53437, 53442, 53452, 53453, 53454, 53455, 53456, 53457, 53458, 53459,
                          53460, 53461, 53462, 53465, 53466, 53467, 53468, 53469, 53470, 53471, 53472, 53473, 53477,
                          53478, 53494, 53496, 53497, 53498, 53499, 53500, 53503, 53504, 53516, 53720, 53727, 53730,
                          53732, 53742, 53743, 53744, 53746, 53747, 53748, 53749, 53750, 53751, 53754, 53755, 53756,
                          53757, 53758, 53759, 53760, 53761, 53763, 53764, 53765, 53766, 53767, 53788, 53789, 53791,
                          53794, 53797, 53798, 53806, 53815, 54016, 54017, 54020, 54023, 54032, 54033, 54034, 54035,
                          54036, 54037, 54038, 54039, 54040, 54041, 54042, 54044, 54045, 54046, 54047, 54048, 54049,
                          54050, 54051, 54055, 54056, 54073, 54074, 54076, 54077, 54078, 54079, 54080, 54081, 54083,
                          54084, 54085, 54086, 54087, 54088, 54096, 54300, 54301, 54302, 54305, 54306, 54307, 54309,
                          54310, 54311, 54312, 54313, 54314, 54315, 54316, 54317, 54318, 54322, 54323, 54324, 54325,
                          54326, 54327, 54328, 54329, 54330, 54331, 54332, 54333, 54334, 54335, 54337, 54339, 54340,
                          54353, 54358, 54362, 54363, 54364, 54368, 54369, 54374, 54378, 54385, 54386, 54387, 54601,
                          54602, 54605, 54606, 54607, 54608, 54609, 54613, 54614, 54615, 54616, 54617, 54618, 54619,
                          54620, 54621, 54627, 54628, 54643, 54644, 54645, 54647, 54648, 54649, 54650, 54652, 54653,
                          54654, 54659, 54660, 54664, 54704, 54880, 54881, 54882, 54883, 54885, 54886, 54887, 54891,
                          54895, 54896, 54897, 54898, 54899, 54901, 54903, 54904, 54905, 54906, 54907, 54908, 54909,
                          54910, 54911, 54917, 54918, 54919, 54920, 54921, 54922, 54923, 54924, 54927, 54933, 54934,
                          54935, 54936, 54937, 54938, 54939, 54940, 54941, 54942, 54943, 54944, 54949, 54951, 54952,
                          54953, 54954, 54955, 54956, 54957, 54964, 54965, 54966, 54967, 55166, 55170, 55171, 55177,
                          55185, 55186, 55187, 55188, 55191, 55193, 55194, 55195, 55196, 55197, 55198, 55199, 55200,
                          55201, 55202, 55203, 55204, 55205, 55206, 55207, 55208, 55209, 55212, 55213, 55214, 55217,
                          55218, 55219, 55223, 55224, 55231, 55232, 55233, 55234, 55235, 55236, 55237, 55238, 55239,
                          55240, 55241, 55242, 55243, 55244, 55246, 55259, 55460, 55466, 55467, 55475, 55476, 55477,
                          55478, 55481, 55482, 55483, 55485, 55486, 55487, 55488, 55489, 55490, 55491, 55493, 55494,
                          55495, 55497, 55499, 55509, 55510, 55511, 55512, 55513, 55514, 55515, 55521, 55522, 55525,
                          55526, 55527, 55528, 55529, 55530, 55531, 55532, 55536, 55548, 55575, 55747, 55750, 55751,
                          55752, 55755, 55756, 55759, 55760, 55763, 55764, 55765, 55766, 55767, 55768, 55769, 55770,
                          55771, 55772, 55773, 55774, 55775, 55776, 55777, 55778, 55779, 55780, 55786, 55787, 55788,
                          55789, 55797, 55798, 55799, 55800, 55802, 55803, 55804, 55813, 55819, 55820, 55821, 55822,
                          55823, 55825, 56040, 56042, 56055, 56056, 56057, 56058, 56060, 56061, 56062, 56063, 56064,
                          56065, 56066, 56067, 56068, 56069, 56076, 56077, 56078, 56084, 56085, 56086, 56087, 56088,
                          56089, 56090, 56091, 56092, 56093, 56094, 56103, 56115, 56330, 56347, 56348, 56352, 56353,
                          56354, 56355, 56357, 56358, 56359, 56363, 56364, 56365, 56366, 56367, 56368, 56369, 56370,
                          56371, 56372, 56373, 56374, 56375, 56376, 56377, 56378, 56379, 56380, 56381, 56382, 56383,
                          56384, 56385, 56386, 56387, 56392, 56393, 56404, 56620, 56636, 56637, 56638, 56639, 56640,
                          56641, 56642, 56643, 56644, 56645, 56646, 56647, 56648, 56649, 56650, 56651, 56653, 56654,
                          56655, 56656, 56657, 56658, 56659, 56660, 56661, 56662, 56663, 56664, 56666, 56668, 56672,
                          56673, 56674, 56675, 56676, 56910, 56919, 56926, 56930, 56931, 56932, 56933, 56934, 56935,
                          56936, 56937, 56938, 56939, 56940, 56941, 56944, 56946, 56947, 56948, 56949, 56950, 56951,
                          56952, 56953, 56956, 56958, 56959, 56961, 56962, 56963, 56964, 56965, 56966, 56967, 56983,
                          57200, 57201, 57206, 57207, 57208, 57209, 57218, 57219, 57223, 57224, 57225, 57226, 57227,
                          57228, 57230, 57233, 57234, 57235, 57237, 57238, 57239, 57240, 57241, 57242, 57243, 57244,
                          57246, 57248, 57249, 57250, 57251, 57252, 57253, 57254, 57255, 57256, 57257, 57258, 57263,
                          57264, 57273, 57284, 57490, 57491, 57492, 57493, 57496, 57497, 57498, 57502, 57506, 57507,
                          57508, 57509, 57510, 57512, 57513, 57514, 57515, 57516, 57517, 57518, 57519, 57520, 57521,
                          57522, 57523, 57524, 57525, 57526, 57527, 57528, 57529, 57530, 57531, 57532, 57533, 57534,
                          57535, 57538, 57539, 57540, 57541, 57542, 57543, 57544, 57545, 57546, 57548, 57549, 57553,
                          57554, 57562, 57573, 57574, 57776, 57777, 57778, 57779, 57780, 57781, 57782, 57783, 57784,
                          57785, 57786, 57787, 57788, 57789, 57790, 57791, 57792, 57795, 57796, 57798, 57799, 57800,
                          57801, 57802, 57803, 57805, 57806, 57807, 57808, 57809, 57810, 57811, 57814, 57816, 57817,
                          57818, 57819, 57822, 57823, 57824, 57825, 57826, 57827, 57828, 57829, 57830, 57831, 57832,
                          57833, 57834, 57837, 57838, 57839, 57843, 57844, 57852, 57864, 58066, 58067, 58068, 58070,
                          58076, 58077, 58078, 58079, 58080, 58081, 58082, 58083, 58088, 58090, 58094, 58095, 58096,
                          58097, 58098, 58099, 58100, 58101, 58106, 58107, 58108, 58109, 58112, 58113, 58114, 58115,
                          58116, 58117, 58118, 58119, 58121, 58122, 58125, 58126, 58127, 58128, 58129, 58130, 58133,
                          58134, 58139, 58141, 58142, 58154, 58155, 58183, 58360, 58363, 58364, 58366, 58367, 58369,
                          58371, 58384, 58385, 58386, 58387, 58388, 58389, 58390, 58391, 58392, 58394, 58397, 58399,
                          58405, 58406, 58407, 58409, 58411, 58412, 58415, 58416, 58417, 58418, 58419, 58420, 58421,
                          58422, 58423, 58424, 58428, 58429, 58431, 58444, 58445, 58446, 58447, 58475, 58646, 58647,
                          58650, 58653, 58654, 58655, 58656, 58657, 58658, 58659, 58660, 58661, 58662, 58664, 58665,
                          58666, 58667, 58670, 58675, 58677, 58678, 58679, 58680, 58681, 58682, 58683, 58684, 58685,
                          58686, 58687, 58688, 58689, 58690, 58691, 58695, 58696, 58697, 58698, 58699, 58700, 58701,
                          58702, 58703, 58704, 58705, 58706, 58707, 58708, 58709, 58710, 58711, 58712, 58718, 58734,
                          58735, 58736, 58737, 58937, 58946, 58947, 58949, 58951, 58952, 58953, 58954, 58955, 58956,
                          58957, 58958, 58959, 58960, 58961, 58962, 58965, 58967, 58968, 58969, 58970, 58971, 58972,
                          58973, 58974, 58975, 58977, 58978, 58979, 58980, 58981, 58982, 58985, 58986, 58987, 58988,
                          58989, 58990, 58991, 58992, 58993, 58994, 58995, 58996, 58997, 58998, 58999, 59000, 59008,
                          59009, 59024, 59025, 59026, 59027, 59239, 59241, 59244, 59248, 59254, 59255, 59256, 59257,
                          59258, 59259, 59260, 59261, 59262, 59264, 59265, 59266, 59267, 59268, 59269, 59270, 59271,
                          59275, 59279, 59280, 59281, 59282, 59283, 59284, 59285, 59286, 59287, 59288, 59289, 59290,
                          59294, 59295, 59298, 59299, 59315, 59316, 59317, 59520, 59527, 59529, 59530, 59531, 59533,
                          59543, 59545, 59546, 59547, 59548, 59549, 59550, 59552, 59553, 59554, 59555, 59556, 59557,
                          59558, 59559, 59561, 59565, 59566, 59570, 59572, 59573, 59574, 59575, 59576, 59577, 59578,
                          59579, 59580, 59583, 59584, 59586, 59587, 59591, 59592, 59593, 59607, 59790, 59810, 59814,
                          59815, 59816, 59817, 59818, 59819, 59820, 59823, 59832, 59833, 59835, 59836, 59837, 59838,
                          59840, 59841, 59842, 59843, 59844, 59845, 59848, 59849, 59851, 59852, 59855, 59856, 59859,
                          59860, 59861, 59862, 59863, 59864, 59865, 59866, 59867, 59868, 59869, 59870, 59871, 59872,
                          59873, 59876, 59877, 59882, 59883, 59889, 59891, 59897, 60080, 60081, 60099, 60100, 60108,
                          60110, 60113, 60123, 60125, 60126, 60127, 60128, 60130, 60131, 60132, 60133, 60134, 60135,
                          60141, 60145, 60146, 60148, 60149, 60150, 60152, 60153, 60158, 60159, 60160, 60161, 60162,
                          60166, 60167, 60170, 60171, 60172, 60173, 60174, 60175, 60180, 60181, 60182, 60185, 60186,
                          60372, 60388, 60389, 60390, 60391, 60392, 60393, 60394, 60395, 60396, 60397, 60398, 60399,
                          60413, 60415, 60416, 60417, 60418, 60420, 60423, 60424, 60425, 60430, 60431, 60432, 60433,
                          60435, 60436, 60438, 60439, 60440, 60441, 60442, 60444, 60446, 60448, 60449, 60450, 60451,
                          60452, 60453, 60454, 60455, 60459, 60460, 60461, 60462, 60463, 60464, 60465, 60470, 60471,
                          60472, 60651, 60676, 60677, 60680, 60681, 60683, 60684, 60687, 60688, 60689, 60694, 60703,
                          60704, 60705, 60706, 60707, 60708, 60710, 60711, 60712, 60713, 60714, 60715, 60719, 60720,
                          60721, 60722, 60724, 60725, 60726, 60728, 60729, 60730, 60731, 60732, 60733, 60735, 60736,
                          60738, 60739, 60740, 60741, 60742, 60743, 60744, 60745, 60746, 60747, 60748, 60749, 60750,
                          60751, 60752, 60753, 60754, 60755, 60760, 60964, 60966, 60968, 60970, 60973, 60981, 60984,
                          60986, 60987, 60992, 60993, 60995, 60996, 60997, 60998, 60999, 61000, 61001, 61002, 61003,
                          61004, 61005, 61006, 61007, 61009, 61010, 61011, 61012, 61013, 61015, 61016, 61017, 61018,
                          61019, 61020, 61021, 61022, 61023, 61024, 61025, 61026, 61028, 61029, 61030, 61031, 61032,
                          61033, 61034, 61035, 61036, 61037, 61038, 61039, 61040, 61042, 61048, 61049, 61050, 61051,
                          61253, 61254, 61256, 61258, 61259, 61260, 61263, 61264, 61270, 61271, 61272, 61273, 61274,
                          61276, 61277, 61278, 61280, 61281, 61282, 61285, 61287, 61288, 61289, 61290, 61291, 61292,
                          61293, 61294, 61295, 61296, 61297, 61299, 61300, 61301, 61302, 61303, 61304, 61305, 61306,
                          61307, 61309, 61310, 61311, 61312, 61313, 61314, 61315, 61316, 61317, 61319, 61320, 61321,
                          61322, 61325, 61326, 61328, 61329, 61330, 61332, 61333, 61334, 61335, 61336, 61337, 61338,
                          61339, 61340, 61544, 61548, 61549, 61550, 61553, 61554, 61555, 61556, 61561, 61562, 61566,
                          61567, 61568, 61569, 61570, 61571, 61572, 61573, 61574, 61579, 61581, 61582, 61584, 61585,
                          61586, 61587, 61588, 61589, 61590, 61591, 61592, 61593, 61594, 61595, 61596, 61597, 61598,
                          61599, 61600, 61601, 61602, 61603, 61604, 61605, 61606, 61607, 61608, 61609, 61610, 61611,
                          61612, 61614, 61616, 61618, 61619, 61620, 61621, 61622, 61623, 61624, 61625, 61626, 61627,
                          61628, 61629, 61829, 61834, 61838, 61840, 61845, 61846, 61847, 61848, 61849, 61850, 61851,
                          61852, 61853, 61855, 61856, 61857, 61858, 61859, 61860, 61861, 61864, 61869, 61871, 61872,
                          61873, 61874, 61875, 61876, 61877, 61878, 61879, 61880, 61881, 61882, 61884, 61886, 61887,
                          61888, 61889, 61890, 61891, 61892, 61893, 61894, 61895, 61896, 61898, 61899, 61900, 61901,
                          61902, 61903, 61904, 61905, 61906, 61907, 61908, 61909, 61911, 61912, 61913, 61914, 61915,
                          61916, 61917, 61918, 61919, 61920, 61922, 61939, 61940, 61944, 61945, 61946, 61947, 62122,
                          62130, 62135, 62136, 62139, 62141, 62142, 62143, 62145, 62146, 62147, 62148, 62149, 62153,
                          62159, 62161, 62164, 62165, 62166, 62167, 62169, 62170, 62173, 62174, 62176, 62177, 62178,
                          62179, 62180, 62181, 62182, 62183, 62184, 62185, 62186, 62188, 62189, 62190, 62191, 62192,
                          62193, 62194, 62195, 62196, 62197, 62198, 62199, 62200, 62201, 62202, 62203, 62207, 62208,
                          62209, 62210, 62212, 62229, 62231, 62233, 62234, 62235, 62237, 62238, 62240, 62241, 62420,
                          62425, 62426, 62427, 62428, 62429, 62430, 62431, 62432, 62433, 62434, 62435, 62436, 62437,
                          62438, 62439, 62440, 62442, 62443, 62449, 62450, 62451, 62452, 62453, 62454, 62455, 62456,
                          62457, 62460, 62464, 62465, 62466, 62469, 62470, 62471, 62472, 62473, 62474, 62475, 62476,
                          62477, 62478, 62479, 62480, 62481, 62483, 62484, 62485, 62486, 62487, 62488, 62489, 62490,
                          62491, 62492, 62493, 62499, 62500, 62501, 62502, 62503, 62519, 62520, 62521, 62523, 62524,
                          62531, 62709, 62710, 62715, 62716, 62718, 62719, 62720, 62721, 62722, 62723, 62739, 62740,
                          62741, 62742, 62743, 62744, 62747, 62748, 62749, 62750, 62753, 62754, 62755, 62756, 62759,
                          62760, 62761, 62762, 62763, 62764, 62765, 62766, 62767, 62768, 62769, 62770, 62771, 62775,
                          62776, 62777, 62778, 62779, 62780, 62781, 62783, 62789, 62790, 62791, 62792, 62793, 62808,
                          62809, 62810, 62811, 62812, 62813, 62814, 62815, 62820, 62821, 63008, 63009, 63010, 63011,
                          63012, 63029, 63030, 63031, 63032, 63033, 63034, 63038, 63040, 63041, 63042, 63043, 63044,
                          63045, 63046, 63047, 63048, 63049, 63050, 63051, 63052, 63053, 63054, 63055, 63059, 63060,
                          63063, 63065, 63066, 63067, 63068, 63069, 63070, 63071, 63072, 63073, 63080, 63081, 63082,
                          63089, 63098, 63099, 63100, 63101, 63102, 63103, 63104, 63107, 63301, 63310, 63319, 63320,
                          63321, 63322, 63323, 63324, 63325, 63326, 63327, 63328, 63329, 63330, 63331, 63332, 63333,
                          63334, 63335, 63336, 63337, 63338, 63339, 63340, 63341, 63342, 63343, 63344, 63345, 63346,
                          63349, 63352, 63353, 63354, 63355, 63356, 63357, 63358, 63359, 63360, 63361, 63362, 63363,
                          63370, 63371, 63379, 63380, 63397, 63400, 63401, 63600, 63601, 63611, 63612, 63613, 63614,
                          63615, 63616, 63617, 63618, 63620, 63621, 63622, 63623, 63624, 63625, 63626, 63627, 63628,
                          63629, 63630, 63631, 63632, 63633, 63634, 63635, 63636, 63642, 63643, 63644, 63645, 63646,
                          63647, 63648, 63649, 63651, 63652, 63660, 63662, 63663, 63664, 63669, 63682, 63683, 63686,
                          63687, 63688, 63690, 63691, 63692, 63697, 63901, 63905, 63911, 63912, 63916, 63917, 63918,
                          63921, 63922, 63923, 63924, 63925, 63926, 63933, 63934, 63935, 63936, 63937, 63938, 63942,
                          63943, 63946, 63948, 63949, 63950, 63951, 63958, 63959, 63971, 63972, 63973, 63975, 63976,
                          63977, 63978, 63979, 63980, 63981, 63982, 63985, 63986, 63987, 64191, 64192, 64194, 64195,
                          64201, 64202, 64204, 64205, 64206, 64207, 64209, 64210, 64212, 64214, 64215, 64220, 64223,
                          64224, 64225, 64232, 64233, 64236, 64237, 64238, 64239, 64240, 64241, 64242, 64243, 64244,
                          64245, 64246, 64261, 64262, 64263, 64264, 64265, 64266, 64267, 64268, 64269, 64270, 64271,
                          64272, 64273, 64274, 64275, 64276, 64277, 64486, 64488, 64489, 64491, 64492, 64494, 64495,
                          64496, 64499, 64500, 64504, 64505, 64509, 64510, 64511, 64512, 64513, 64514, 64515, 64526,
                          64527, 64528, 64529, 64530, 64531, 64532, 64533, 64534, 64535, 64536, 64543, 64544, 64545,
                          64546, 64549, 64551, 64552, 64553, 64554, 64555, 64556, 64558, 64559, 64560, 64561, 64562,
                          64563, 64564, 64565, 64776, 64777, 64779, 64780, 64781, 64782, 64783, 64784, 64785, 64786,
                          64787, 64788, 64789, 64790, 64791, 64794, 64795, 64798, 64799, 64800, 64801, 64802, 64803,
                          64804, 64809, 64814, 64815, 64816, 64817, 64818, 64819, 64820, 64822, 64823, 64833, 64834,
                          64835, 64836, 64837, 64838, 64839, 64840, 64841, 64842, 64843, 64844, 64845, 64846, 64848,
                          64849, 64850, 64851, 64852, 65070, 65073, 65074, 65076, 65077, 65078, 65079, 65080, 65081,
                          65082, 65083, 65085, 65088, 65090, 65091, 65092, 65094, 65095, 65096, 65098, 65099, 65101,
                          65102, 65104, 65105, 65107, 65124, 65128, 65129, 65130, 65131, 65132, 65133, 65134, 65135,
                          65136, 65137, 65139, 65140, 65141, 65142, 65143, 65144, 65145, 65146, 65357, 65358, 65366,
                          65367, 65368, 65369, 65370, 65371, 65372, 65374, 65380, 65381, 65382, 65383, 65384, 65385,
                          65386, 65387, 65388, 65389, 65390, 65391, 65392, 65393, 65394, 65395, 65397, 65419, 65421,
                          65422, 65424, 65426, 65429, 65430, 65431, 65432, 65433, 65434, 65435, 65436, 65437, 65640,
                          65647, 65648, 65651, 65658, 65660, 65661, 65662, 65664, 65665, 65666, 65667, 65670, 65671,
                          65672, 65673, 65674, 65675, 65676, 65677, 65678, 65679, 65680, 65681, 65682, 65685, 65687,
                          65709, 65710, 65712, 65719, 65720, 65721, 65722, 65723, 65724, 65726, 65917, 65930, 65931,
                          65932, 65937, 65938, 65940, 65941, 65942, 65943, 65945, 65951, 65952, 65953, 65954, 65955,
                          65956, 65957, 65961, 65962, 65963, 65964, 65965, 65966, 65967, 65968, 65969, 65970, 65971,
                          65972, 65974, 65975, 65977, 65998, 65999, 66000, 66002, 66010, 66011, 66014, 66219, 66220,
                          66221, 66222, 66226, 66227, 66228, 66229, 66230, 66231, 66232, 66233, 66234, 66235, 66236,
                          66240, 66241, 66242, 66243, 66245, 66246, 66248, 66249, 66251, 66252, 66253, 66254, 66255,
                          66256, 66261, 66262, 66263, 66264, 66265, 66267, 66288, 66289, 66290, 66292, 66293, 66299,
                          66300, 66303, 66304, 66305, 66306, 66496, 66497, 66498, 66510, 66512, 66515, 66516, 66519,
                          66520, 66521, 66522, 66523, 66524, 66525, 66526, 66527, 66531, 66532, 66533, 66535, 66536,
                          66538, 66539, 66540, 66542, 66544, 66545, 66546, 66547, 66549, 66550, 66551, 66552, 66553,
                          66555, 66556, 66560, 66589, 66590, 66596, 66785, 66786, 66800, 66802, 66805, 66809, 66810,
                          66811, 66812, 66814, 66815, 66816, 66819, 66820, 66821, 66822, 66823, 66829, 66830, 66832,
                          66833, 66834, 66835, 66836, 66843, 66848, 66849, 66850, 67073, 67074, 67075, 67090, 67091,
                          67092, 67094, 67108, 67109, 67110, 67111, 67112, 67113, 67120, 67121, 67123, 67125, 67126,
                          67130, 67133, 67134, 67142, 67143, 67147, 67148, 67149, 67363, 67382, 67383, 67384, 67398,
                          67399, 67400, 67401, 67402, 67403, 67411, 67413, 67414, 67416, 67417, 67419, 67420, 67427,
                          67428, 67430, 67431, 67432, 67436, 67671, 67672, 67673, 67688, 67689, 67690, 67691, 67692,
                          67700, 67701, 67707, 67708, 67709, 67710, 67718, 67719, 67721, 67728, 67961, 67962, 67977,
                          67978, 67980, 67981, 67984, 67989, 67990, 67995, 67996, 67997, 67998, 67999, 68005, 68007,
                          68008, 68009, 68010, 68011, 68017, 68018, 68019, 68251, 68267, 68268, 68269, 68270, 68271,
                          68273, 68274, 68279, 68284, 68285, 68286, 68287, 68288, 68289, 68299, 68301, 68307, 68308,
                          68556, 68557, 68558, 68559, 68560, 68562, 68563, 68565, 68569, 68573, 68574, 68575, 68576,
                          68578, 68581, 68591, 68597, 68598, 68845, 68846, 68847, 68848, 68849, 68850, 68852, 68853,
                          68854, 68858, 68859, 68861, 68862, 68866, 68869, 68870, 68871, 68880, 68881, 68883, 68885,
                          68886, 68887, 68888, 68889, 69136, 69137, 69138, 69139, 69140, 69141, 69142, 69144, 69148,
                          69150, 69151, 69153, 69154, 69156, 69157, 69158, 69168, 69169, 69170, 69171, 69172, 69173,
                          69177, 69179, 69209, 69425, 69426, 69427, 69428, 69429, 69432, 69433, 69434, 69438, 69439,
                          69440, 69442, 69443, 69446, 69447, 69449, 69450, 69455, 69456, 69462, 69467, 69468, 69715,
                          69716, 69718, 69722, 69723, 69724, 69728, 69729, 69731, 69732, 69736, 69740, 69742, 69743,
                          69744, 69745, 69751, 69752, 69753, 69755, 69756, 69757, 69758, 69759, 70005, 70006, 70008,
                          70012, 70013, 70014, 70016, 70017, 70018, 70019, 70020, 70030, 70031, 70032, 70033, 70034,
                          70035, 70042, 70043, 70044, 70045, 70046, 70047, 70048, 70049, 70295, 70296, 70297, 70298,
                          70299, 70300, 70301, 70302, 70303, 70304, 70306, 70308, 70309, 70317, 70318, 70319, 70320,
                          70323, 70324, 70333, 70334, 70336, 70566, 70585, 70586, 70587, 70588, 70589, 70590, 70591,
                          70592, 70593, 70598, 70606, 70607, 70609, 70610, 70611, 70614, 70623, 70624, 70625, 70626,
                          70855, 70856, 70875, 70876, 70877, 70878, 70879, 70880, 70881, 70882, 70883, 70887, 70888,
                          70899, 70901, 70904, 70910, 70913, 70915, 70916, 71144, 71145, 71146, 71165, 71166, 71167,
                          71168, 71169, 71170, 71171, 71172, 71173, 71177, 71200, 71202, 71206, 71435, 71436, 71455,
                          71456, 71460, 71461, 71462, 71467, 71485, 71489, 71724, 71725, 71726, 71744, 71745, 71746,
                          71747, 71757, 71758, 71771, 71772, 71774, 71775, 72012, 72013, 72014, 72015, 72035, 72036,
                          72037, 72038, 72039, 72060, 72061, 72062, 72063, 72299, 72302, 72325, 72326, 72327, 72328,
                          72329, 72334, 72337, 72338, 72342, 72343, 72345, 72346, 72347, 72348, 72349, 72350, 72545,
                          72590, 72591, 72592, 72593, 72616, 72617, 72618, 72619, 72624, 72625, 72626, 72635, 72636,
                          72882, 72883, 72884, 72885, 72889, 72905, 72907, 72908, 72909, 72913, 72914, 72916, 72917,
                          72918, 72933, 73173, 73179, 73181, 73182, 73194, 73195, 73197, 73199, 73200, 73203, 73205,
                          73207, 73220, 73472, 73485, 73486, 73487, 73488, 73489, 73491, 73492, 73494, 73505, 73775,
                          73776, 73777, 73778, 73780, 73781, 73782, 73783, 73784, 73800, 74061, 74062, 74063, 74065,
                          74066, 74068, 74069, 74070, 74071, 74072, 74073, 74091, 74349, 74351, 74352, 74353, 74354,
                          74355, 74356, 74357, 74358, 74359, 74360, 74361, 74362, 74375, 74381, 74382, 74634, 74637,
                          74638, 74639, 74641, 74642, 74643, 74644, 74645, 74646, 74647, 74649, 74650, 74651, 74652,
                          74665, 74912, 74922, 74923, 74926, 74928, 74934, 74936, 74939, 74940, 74941, 74955, 75226,
                          75229, 75230, 75519, 75520, 75521, 75527, 75809, 75811, 75816, 75817, 76095, 76101, 76384,
                          76385, 76386, 76388, 76389, 76390, 76391, 76392, 76397, 76402, 76413, 76680, 76686, 76687,
                          76690, 76691, 76692, 76962, 77250, 77251, 77252, 77254, 77255, 77256, 77538, 77540, 77541,
                          77542, 77828, 77829, 77830, 77831, 77832, 78118, 78119, 78122, 78408, 78409, 78410, 78411,
                          78412, 78701, 78735, 78993, 79572, 79862, 80152, 80442, 81059, 81307, 81350, 81597, 81891,
                          82221, 83963, 85125, 87751]
    # indexRange = range(64832, 64838)
    # gridIDHaveDataList = random.sample(gridIDHaveDataList, 3)
    num = 0
    gridIDHaveDataList = [38116]
    for index in gridIDHaveDataList:
        num += 1
        print('num={}'.format(num))
        trainData = sc.textFile('hdfs://master:9000//fcd/397-290_trainDataSet/trainData_{}.csv'.format(index))
        trainData = trainData.map(lambda line: line.split(','))
        columnName = trainData.first()
        trainData = trainData.filter(lambda row: row != columnName).toDF(columnName)
        trainData = trainData.rdd.map(lambda x: (Vectors.dense(x[0:-1]), x[-1])).toDF(["features", "label"])
        labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(trainData)
        trainData = labelIndexer.transform(trainData)
        label = labelIndexer.labels
        labelDict = {}
        for i in range(len(label)):
            labelDict[label[i]] = i
        labelValIndex = list(labelDict.items())
        labelRdd = sc.parallelize(labelValIndex)
        labelDF = spark.createDataFrame(labelRdd, ['secID', 'index'])
        labelDF.write.save('hdfs://master:9000//fcd/completeLabelIndexer/labelIndexer_{}'.format(index),
                           format='parquet', mode='append')

        # df = spark.read.format('parquet').load('hdfs://master:9000//sparkExperiment/labelIndexer/labelIndexer_60438')

        rf = RandomForestClassifier(numTrees=3, maxDepth=2, labelCol='indexedLabel', featuresCol='features', seed=42)
        model1 = rf.fit(trainData)
        model1.save('hdfs://master:9000//fcd/completeModel/model_{}'.format(index))
    end = time.time()
    print('训练花费时间: {}s'.format(end - start))
    sc.stop()
