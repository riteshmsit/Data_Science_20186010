# -*- coding: utf-8 -*-
"""Spark.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B5SMwvE1WRME3tDco9n7gLteH1zJz2y9
"""

import matplotlib as mpl
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %matplotlib inline

pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 100)

!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q https://www-us.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz
!tar xf spark-2.4.3-bin-hadoop2.7.tgz
!pip install -q findspark

import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-2.4.3-bin-hadoop2.7"

import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()

sc

sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).map(lambda x : x**2).sum()

"""# CREATE A RDD"""

wordsList = ['cat', 'elephant', 'rat', 'rat', 'cat']
wordsRDD = sc.parallelize(wordsList, 4)
print(type(wordsRDD))

?sc.parallelize()

sc.parallelize([0, 2, 3, 4, 6], 5).glom().collect()

sc.parallelize(range(0, 6, 2), 5).glom().collect()

wordsRDD.collect()

"""# OPERATIONS ON RDD

**RDDs support two types of operations: transformations, which create a new dataset from an existing one, and actions, which return a value to the driver program after running a computation on the dataset. For example, map is a transformation that passes each dataset element through a function and returns a new RDD representing the results. On the other hand, reduce is an action that aggregates all the elements of the RDD using some function and returns the final result to the driver program (although there is also a parallel reduceByKey that returns a distributed dataset).**

**Word Examples**
"""

def makePlural(word):
  return word + 's'

print(makePlural('cat'))

"""Transform one RDD into another"""

pluralRDD = wordsRDD.map(makePlural)
print(pluralRDD.first())
print(pluralRDD.take(2))

pluralRDD.take(1)

pluralRDD.collect()

"""**Key Value Pairs**"""

wordPairs = wordsRDD.map(lambda w : (w, 1))
print(wordPairs.collect())

"""# WORD COUNT"""

wordsList = ['cat', 'elephant', 'rat', 'rat', 'cat']
wordsRDD = sc.parallelize(wordsList, 4)
wordCountsCollected = (wordsRDD.map(lambda w : (w, 1)).reduceByKey(lambda x,y : x+y).collect())
print(wordCountsCollected)

print(wordsRDD.map(lambda w : (w, 1)).reduceByKey(lambda x,y : x+y).toDebugString())

"""# Using Cache"""

wordsList = ['cat', 'elephant', 'rat', 'rat', 'cat']
wordsRDD = sc.parallelize(wordsList, 4)
print(wordsRDD)
wordsRDD.count()

wordsRDD.count()

wordsRDD.cache()

wordsRDD.count()

wordsRDD.count()

"""**Where is this useful: it is when you have branching parts or loops, so that you dont do things again and again. Spark, being "lazy" will rerun the chain again. So cache or persist serves as a checkpoint, breaking the RDD chain or the lineage.**"""

birdsList = ['heron', 'owl']
animList = wordsList + birdsList

animaldict = {}
for e in wordsList:
  animaldict[e] = 'mammal'
for e in birdsList:
  animaldict[e] = 'bird'
  
animaldict

animsrdd = sc.parallelize(animList, 4)
animsrdd.cache()

mammalcount = animsrdd.filter(lambda w : animaldict[w] == 'mammal').count()
birdcount = animsrdd.filter(lambda w : animaldict[w] == 'bird').count()

print(mammalcount, birdcount)

from google.colab import files
upload = files.upload()

stopwords = [e.strip() for e in open('english.stop.txt').readlines()]

juliusrdd = sc.textFile('juliuscaeser.txt')

juliusrdd.flatMap(lambda line : line.split()).count()

(juliusrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).collect())

(juliusrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).take(20))

(juliusrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).filter(lambda word : word not in stopwords).collect())

(juliusrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).filter(lambda word : word not in stopwords).take(20))

(juliusrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).filter(lambda word : word not in stopwords).map(lambda word : (word, 1)).collect())

(juliusrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).filter(lambda word : word not in stopwords).map(lambda word : (word, 1)).take(20))

(juliusrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).filter(lambda word : word not in stopwords).map(lambda word : (word, 1)).reduceByKey(lambda a,b : a + b).collect())

(juliusrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).filter(lambda word : word not in stopwords).map(lambda word : (word, 1)).reduceByKey(lambda a,b : a + b).take(20))

(juliusrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).filter(lambda word : word not in stopwords).map(lambda word : (word, 1)).reduceByKey(lambda a,b : a + b).takeOrdered(20, lambda x : -x[1]))

captions, counts = zip(*juliusrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).filter(lambda word : word not in stopwords).map(lambda word : (word, 1)).reduceByKey(lambda a,b : a + b).takeOrdered(20, lambda x : -x[1]))

pos = np.arange(len(counts))
plt.bar(pos, counts)
plt.xticks(pos+0.4, captions, rotation=90)

from google.colab import files
upload = files.upload()

novelrdd = sc.textFile('*.txt', minPartitions = 4)

novelrdd.collect()

novelrdd.take(10)

(novelrdd.flatMap(lambda line : line.split()).map(lambda word : word.strip().lower()).filter(lambda word : word not in stopwords).map(lambda word : (word, 1)).reduceByKey(lambda a,b : a+b).sortByKey(0,1).take(30))

from google.colab import files
upload = files.upload()

df = pd.read_csv('01_heights_weights_genders.csv')
df.head()

from pyspark.sql import SQLContext
sqlsc = SQLContext(sc)
sparkdf = sqlsc.createDataFrame(df)

sparkdf

sparkdf.show(10)

type(sparkdf.Gender)

temp = sparkdf.rdd.map(lambda r : r.Gender)
print(type(temp))
temp.take(10)

"""# Machine Learning"""

from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.regression import LabeledPoint

data = sparkdf.rdd.map(lambda row : LabeledPoint(row.Gender == 'Male', [row.Height, row.Weight]))
data.take(5)

data2 = sparkdf.rdd.map(lambda row : LabeledPoint(row[0] == 'Male', row[1:]))
data2.take(5)[0].label, data2.take(5)[1].features

train, test = data.randomSplit([0.7, 0.3])
train.cache()
test.cache()

type(train)

type(test)

model = LogisticRegressionWithLBFGS.train(train)

model.weights

results = test.map(lambda lp : (lp.label, float(model.predict(lp.features))))

results.take(10)

type(results)

from pyspark.mllib.evaluation import BinaryClassificationMetrics
metrics = BinaryClassificationMetrics(results)

print(type(metrics))
metrics.areaUnderROC

type(model)

!rm -rf mylogistic.model

sc.stop()