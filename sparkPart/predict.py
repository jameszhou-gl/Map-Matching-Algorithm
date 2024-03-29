#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-20 10:39:25
# @Author  : guanglinzhou (xdzgl812@163.com)
# @Link    : https://github.com/GuanglinZhou
# @Version : $Id$
# from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors
# import random
# import time
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.sql.functions import udf

if __name__ == '__main__':
    spark = SparkSession.builder.appName("generateCompletePred").getOrCreate()
    sc = spark.sparkContext
    # start = time.time()
    gridIDHaveDataList = [
                          63033, 63034, 63038, 63040, 63041, 63042, 63043, 63044, 63045, 63046, 63047, 63048, 63049,
                          63050, 63051, 63052, 63053, 63054, 63055, 63059, 63060, 63063, 63065, 63066, 63067, 63068,
                          63069, 63070, 63071, 63072, 63073, 63080, 63081, 63082, 63089, 63099, 63100, 63101, 63102,
                          63103, 63104, 63107, 63301, 63310, 63319, 63320, 63321, 63323, 63324, 63325, 63326, 63327,
                          63328, 63329, 63330, 63331, 63332, 63333, 63334, 63335, 63336, 63337, 63338, 63339, 63340,
                          63341, 63342, 63343, 63344, 63345, 63346, 63349, 63352, 63353, 63354, 63355, 63356, 63357,
                          63358, 63359, 63360, 63361, 63362, 63370, 63379, 63397, 63400, 63401, 63600, 63601, 63611,
                          63612, 63613, 63614, 63615, 63616, 63617, 63618, 63620, 63621, 63622, 63623, 63624, 63625,
                          63626, 63627, 63628, 63629, 63630, 63631, 63632, 63633, 63634, 63635, 63636, 63642, 63643,
                          63644, 63645, 63646, 63647, 63648, 63649, 63651, 63652, 63660, 63662, 63663, 63664, 63669,
                          63682, 63683, 63687, 63688, 63690, 63691, 63692, 63697, 63901, 63905, 63911, 63912, 63916,
                          63917, 63918, 63921, 63922, 63923, 63924, 63925, 63926, 63933, 63934, 63935, 63936, 63937,
                          63938, 63942, 63943, 63946, 63948, 63949, 63950, 63951, 63958, 63959, 63971, 63972, 63973,
                          63975, 63976, 63977, 63978, 63979, 63980, 63981, 63982, 63985, 63986, 63987, 64191, 64194,
                          64195, 64201, 64202, 64204, 64205, 64206, 64207, 64209, 64210, 64212, 64214, 64215, 64220,
                          64223, 64224, 64225, 64232, 64233, 64236, 64237, 64238, 64239, 64240, 64241, 64242, 64243,
                          64245, 64246, 64261, 64262, 64263, 64264, 64266, 64267, 64268, 64269, 64270, 64272, 64273,
                          64274, 64275, 64276, 64488, 64489, 64491, 64492, 64494, 64495, 64496, 64499, 64500, 64504,
                          64505, 64509, 64510, 64511, 64512, 64513, 64514, 64526, 64527, 64528, 64529, 64530, 64531,
                          64532, 64533, 64534, 64535, 64536, 64545, 64549, 64551, 64552, 64553, 64554, 64555, 64556,
                          64558, 64559, 64560, 64561, 64562, 64563, 64564, 64565, 64776, 64777, 64779, 64780, 64781,
                          64782, 64783, 64784, 64785, 64786, 64787, 64788, 64789, 64790, 64791, 64794, 64795, 64798,
                          64799, 64800, 64801, 64802, 64803, 64804, 64809, 64814, 64815, 64816, 64817, 64818, 64819,
                          64820, 64834, 64835, 64837, 64838, 64839, 64840, 64841, 64842, 64843, 64844, 64845, 64846,
                          64848, 64849, 64850, 64851, 64852, 65070, 65073, 65074, 65076, 65077, 65078, 65079, 65080,
                          65081, 65082, 65083, 65085, 65088, 65090, 65091, 65092, 65094, 65095, 65096, 65098, 65099,
                          65101, 65102, 65104, 65105, 65107, 65124, 65128, 65129, 65130, 65131, 65132, 65134, 65135,
                          65136, 65137, 65140, 65141, 65142, 65143, 65144, 65146, 65357, 65358, 65366, 65367, 65368,
                          65369, 65370, 65371, 65372, 65374, 65380, 65381, 65382, 65383, 65384, 65385, 65386, 65387,
                          65388, 65389, 65390, 65391, 65392, 65395, 65397, 65419, 65421, 65422, 65424, 65426, 65429,
                          65430, 65431, 65432, 65433, 65434, 65435, 65436, 65437, 65640, 65647, 65648, 65658, 65660,
                          65661, 65662, 65664, 65665, 65666, 65667, 65670, 65671, 65672, 65673, 65674, 65675, 65676,
                          65677, 65678, 65679, 65680, 65681, 65682, 65685, 65687, 65709, 65723, 65724, 65726, 65917,
                          65930, 65931, 65937, 65938, 65940, 65941, 65942, 65943, 65945, 65951, 65952, 65953, 65954,
                          65955, 65956, 65957, 65961, 65962, 65963, 65964, 65965, 65966, 65967, 65968, 65969, 65970,
                          65971, 65972, 65974, 65975, 65977, 65999, 66014, 66220, 66221, 66222, 66226, 66227, 66228,
                          66229, 66230, 66231, 66232, 66233, 66234, 66235, 66236, 66240, 66241, 66242, 66243, 66245,
                          66246, 66248, 66249, 66251, 66252, 66253, 66254, 66255, 66256, 66261, 66262, 66263, 66264,
                          66265, 66267, 66289, 66290, 66304, 66305, 66306, 66496, 66497, 66498, 66510, 66512, 66515,
                          66516, 66519, 66520, 66521, 66522, 66523, 66524, 66525, 66526, 66527, 66531, 66532, 66533,
                          66535, 66538, 66539, 66540, 66542, 66544, 66545, 66546, 66547, 66549, 66550, 66551, 66552,
                          66553, 66555, 66556, 66560, 66596, 66785, 66786, 66800, 66802, 66805, 66812, 66814, 66815,
                          66816, 66819, 66820, 66821, 66822, 66823, 66829, 66830, 66832, 66833, 66834, 66835, 66836,
                          66843, 66849, 66850, 67073, 67074, 67075, 67090, 67091, 67092, 67094, 67109, 67112, 67113,
                          67120, 67121, 67123, 67125, 67126, 67142, 67143, 67147, 67148, 67363, 67382, 67383, 67384,
                          67398, 67399, 67400, 67401, 67402, 67403, 67411, 67413, 67414, 67416, 67417, 67419, 67420,
                          67427, 67428, 67430, 67431, 67432, 67436, 67671, 67672, 67673, 67688, 67689, 67690, 67691,
                          67700, 67701, 67707, 67708, 67709, 67721, 67728, 67961, 67962, 67977, 67978, 67980, 67981,
                          67984, 67990, 67995, 67996, 67997, 67998, 67999, 68005, 68008, 68009, 68010, 68011, 68017,
                          68018, 68251, 68267, 68268, 68269, 68270, 68273, 68279, 68285, 68286, 68287, 68288, 68289,
                          68301, 68307, 68308, 68556, 68557, 68558, 68559, 68560, 68562, 68563, 68569, 68575, 68576,
                          68578, 68581, 68591, 68597, 68598, 68845, 68846, 68847, 68848, 68849, 68850, 68852, 68853,
                          68854, 68858, 68859, 68861, 68862, 68866, 68869, 68870, 68871, 68881, 68883, 68885, 68886,
                          68887, 68888, 68889, 69136, 69137, 69138, 69139, 69140, 69141, 69142, 69144, 69148, 69150,
                          69151, 69153, 69154, 69156, 69157, 69158, 69168, 69169, 69170, 69171, 69172, 69173, 69177,
                          69425, 69426, 69427, 69428, 69429, 69432, 69433, 69434, 69438, 69439, 69440, 69442, 69443,
                          69446, 69447, 69449, 69450, 69455, 69456, 69462, 69467, 69468, 69715, 69716, 69718, 69722,
                          69723, 69724, 69728, 69729, 69731, 69732, 69736, 69740, 69742, 69743, 69744, 69745, 69751,
                          69752, 69753, 69755, 69756, 69757, 69758, 69759, 70005, 70006, 70008, 70012, 70013, 70014,
                          70016, 70017, 70018, 70030, 70031, 70032, 70033, 70034, 70042, 70043, 70044, 70045, 70046,
                          70047, 70048, 70049, 70295, 70296, 70297, 70298, 70299, 70300, 70301, 70302, 70303, 70304,
                          70308, 70317, 70318, 70319, 70320, 70323, 70324, 70333, 70334, 70336, 70566, 70585, 70586,
                          70587, 70588, 70589, 70590, 70591, 70592, 70593, 70598, 70606, 70607, 70609, 70610, 70611,
                          70614, 70623, 70624, 70625, 70626, 70855, 70856, 70875, 70877, 70878, 70879, 70880, 70881,
                          70882, 70883, 70887, 70888, 70899, 70901, 70904, 70910, 70913, 70915, 70916, 71144, 71145,
                          71146, 71165, 71166, 71167, 71168, 71169, 71170, 71171, 71172, 71173, 71177, 71200, 71202,
                          71206, 71435, 71436, 71455, 71456, 71462, 71467, 71485, 71489, 71724, 71725, 71726, 71744,
                          71745, 71746, 71747, 71757, 71758, 71772, 71774, 71775, 72012, 72013, 72014, 72015, 72035,
                          72036, 72037, 72038, 72039, 72060, 72061, 72062, 72063, 72302, 72325, 72326, 72327, 72328,
                          72329, 72337, 72338, 72342, 72343, 72345, 72346, 72347, 72348, 72349, 72350, 72545, 72590,
                          72591, 72592, 72593, 72616, 72617, 72618, 72619, 72624, 72625, 72626, 72636, 72882, 72883,
                          72884, 72889, 72905, 72907, 72908, 72909, 72913, 72914, 72916, 72917, 73173, 73179, 73181,
                          73182, 73194, 73195, 73197, 73199, 73200, 73203, 73205, 73207, 73220, 73485, 73486, 73487,
                          73488, 73491, 73492, 73494, 73775, 73776, 73780, 73781, 73782, 73783, 73784, 73800, 74062,
                          74065, 74066, 74069, 74070, 74071, 74072, 74073, 74091, 74349, 74351, 74352, 74353, 74354,
                          74355, 74356, 74357, 74359, 74360, 74361, 74362, 74381, 74634, 74637, 74638, 74639, 74643,
                          74644, 74645, 74646, 74647, 74649, 74650, 74651, 74652, 74665, 74912, 74922, 74923, 74928,
                          74934, 74936, 74939, 74940, 74941, 74955, 75229, 75230, 75519, 75520, 75521, 75527, 75809,
                          75811, 75817, 76095, 76101, 76384, 76385, 76386, 76388, 76389, 76390, 76391, 76392, 76397,
                          76413, 76686, 76687, 76690, 76691, 76962, 77250, 77251, 77252, 77255, 77256, 77538, 77540,
                          77541, 77542, 77828, 77829, 77830, 77831, 77832, 78118, 78119, 78122, 78408, 78409, 78410,
                          78411, 78412, 78735, 78993, 79572, 79862, 80152, 80442, 81059, 81307, 81350, 81597, 81891,
                          82221, 83963, 87751]
    # gridIDHaveDataList = random.sample(gridIDHaveDataList, 10)
    for index in gridIDHaveDataList:
        model = RandomForestClassificationModel.load(
            'hdfs://master:9000//fcd/completeModel/model_{}'.format(index))
        test = sc.textFile('hdfs://master:9000//fcd/397-290_testDataSetMatchTrainDataSet/testData_{}.csv'.format(index))
        test = test.map(lambda line: line.split(','))
        columnName = test.first()
        test = test.filter(lambda row: row != columnName).toDF(columnName)
        test = test.rdd.map(lambda x: (Vectors.dense(x[0:-1]), x[-1])).toDF(["features", "label"])

        labelIndexer = spark.read.format('parquet').load(
            'hdfs://master:9000//fcd/completeLabelIndexer/labelIndexer_{}'.format(index))
        labelIndexer_pandas = labelIndexer.toPandas()
        indexRange = range(labelIndexer_pandas.shape[0])
        index_secID_dict = {}
        for i in indexRange:
            index_secID_dict[str(labelIndexer_pandas.iloc[i, 1])] = labelIndexer_pandas.iloc[i, 0]
        pred = model.transform(test)


        def func(s):
            return index_secID_dict[str(int(s))]


        func_udf = udf(func)
        pred = pred.withColumn('pred', func_udf('prediction')).select('pred')
        pred.write.csv('hdfs://master:9000//fcd/completePred/node8/pred_{}.csv'.format(index))
    # end = time.time()
    # print('预测花费时间：{}'.format(end - start))
    sc.stop()
