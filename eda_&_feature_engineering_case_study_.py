# -*- coding: utf-8 -*-
"""EDA & feature-engineering case study .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f0pWcV-r3C-AFozkD7wxpzN1LW4R_Nha

# Feature Engineering Assignments

**Today's Case focal points:**
- Feature Scaling & Transformation
- Feature Encoding (Categorical Data)
- Feature Cleaning & Imputation

### Importing Libraries & Datasets
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msn
# %matplotlib inline
sns.set()

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/Machine learning/Datasets/stackoverflow.csv')

df.head(2)

"""# Data Exploration

"""

df.info()

df.describe()

"""## let's define numaric and catgorical variables """

df_num = df[['ConvertedSalary', 'StackOverflowJobsRecommend', 'Age',
       'Years Experience']]
df_cat = df[['FormalEducation' , 'Country' ,'VersionControl' ,'Gender'  ]]

numric_col = df.describe().columns
numric_col

"""##  plot distruptoion  for numiric values """

df_num = df[['ConvertedSalary', 'StackOverflowJobsRecommend', 'Age',
       'Years Experience']]
for i in df_num:
  sns.displot(df_num[i] , kind='kde')

  plt.show()

"""## Explore some corlaetion between Numric variables"""

df_num.corr()

sns.heatmap(df_num.corr() , cmap='Blues');

df['Gender'].value_counts()

# mapping gender column
df['Gender_Numeric'] = df['Gender'].apply(lambda x: 0if x == "Male" else(1 if x=='Female' else '-1'))
df['Gender_Numeric'].value_counts()

np.round(pd.pivot_table(df,index = 'Gender_Numeric',values=[ 'Years Experience' , 'ConvertedSalary' ]) , decimals=0)

"""## Explore catgorical variables

"""

df['Gender'] = df['Gender'].apply(lambda x: 'Male' if x == "Male" else("Female" if x=='Female' else 'Other'))

for i in df_cat:
  sns.barplot(df_cat[i].value_counts().index,df_cat[i].value_counts())
  plt.show()

"""==========

## Feature Cleaning & Imputation Exercises

#### Check for any missing data
"""

df.isnull().sum()

msn.bar(df , figsize=(10,5));

"""### Caluclting precntage of missing values"""

df["StackOverflowJobsRecommend"].isnull().sum()/df.shape[0]*100

df['ConvertedSalary'].isnull().sum()/df.shape[0]*100

df['RawSalary'].isnull().sum()/df.shape[0]*100

#check raw salary data types
df['RawSalary'].dtype

df['RawSalary'].value_counts()

"""## Imputing Missing values """

df['RawSalary'] = df['RawSalary'].replace({'\$':'', ',':'','£':'' ,'$':''} ,regex=True)

df['RawSalary'].value_counts()

df['RawSalary'].isnull().sum()

"""#using ittrative imputer """

from sklearn.ensemble import ExtraTreesRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
Regrssor = IterativeImputer(estimator=ExtraTreesRegressor(),random_state=42 , max_iter=10)
Ittimputer= Regrssor.fit_transform(df[['RawSalary' ,'ConvertedSalary']])
Ittimputer

df['ImputedRawSalary']= Ittimputer[:, 0]
df['ImputedRawSalary']

"""Using KNN Imputer"""

from sklearn.impute import KNNImputer
model = KNNImputer(n_neighbors=3)
imputed_Array = model.fit_transform(df_num)
imputed_Array

imputed_num_df = pd.DataFrame(imputed_Array , columns=['ConvertedSalary','StackOverflowJobsRecommend',	'Age',	'Years Experience'])
np.round(imputed_num_df ,decimals=2)

imputed_num_df['imputed_RawSalary'] = Ittimputer[:, 0]
np.round(imputed_num_df ,decimals=2)

msn.bar(imputed_num_df , figsize=(5,5));

"""#Detcting outliers Visualy

## Univariate
"""

plt.figure(figsize=(15,10))
imputed_num_df.boxplot();
plt.show()

for i in imputed_num_df:
  plt.boxplot(imputed_num_df[i])
  plt.title(i)
  plt.show()

"""#Multivruate exploration"""

g = sns.FacetGrid(tips, col="sex", hue="smoker")
g.map(sns.scatterplot, "total_bill", "tip", alpha=.7)
g.add_legend()

g = sns.FacetGrid(df , col ='Gender' , hue= 'Gender')
g.map(plt.scatter,'Years Experience' ,'ConvertedSalary' )
g.set_xticklabels(rotation=45)
g.add_legend();

#df['Gender'].value_counts().index

#g= sns.catplot(x="index", y="vals", hue='cols', data=df, kind='point')

plt.scatter(df['RawSalary'] ,df['ConvertedSalary'])

"""# Now let's apply Isoaltion forest to detect the indexs of outliers"""

from sklearn.ensemble import IsolationForest
clf = IsolationForest(contamination = .12)
predections = clf.fit_predict(imputed_num_df[['imputed_RawSalary' ,'ConvertedSalary']])





anom = np.where(predections<0)
anom

imputed_num_df.drop([ 7,   9,  14,  19,  20,  68,  71,  72,  76,  90,  93, 116, 127,
        136, 138, 147, 167, 169, 170, 175, 178, 189, 192, 199, 202, 205,
        214, 227, 234, 241, 245, 251, 261, 280, 285, 305, 313, 319, 321,
        333, 351, 352, 358, 363, 374, 380, 385, 388, 393, 399, 401, 402,
        404, 407, 408, 412, 413, 420, 424, 425, 431, 439, 450, 458, 468,
        482, 484, 485, 486, 488, 495, 500, 505, 524, 541, 558, 559, 563,
        578, 581, 583, 584, 607, 612, 613, 615, 623, 624, 625, 632, 633,
        641, 657, 658, 664, 667, 670, 680, 683, 685, 686, 701, 714, 715,
        725, 727, 732, 738, 748, 752, 769, 773, 780, 782, 783, 805, 822,
        828, 833, 834, 835, 836, 837, 840, 843, 844, 857, 873, 888, 894,
        897, 901, 906, 908, 915, 920, 928, 931, 933, 938, 939, 941, 951,
        953, 964, 966, 980, 987, 990, 998] , axis=0 , inplace =True )

imputed_num_df[['imputed_RawSalary' ,'ConvertedSalary']].boxplot()

plt.scatter(imputed_num_df['imputed_RawSalary'] ,imputed_num_df['ConvertedSalary'])

imputed_num_df[['ConvertedSalary', 'StackOverflowJobsRecommend', 'Age',
       'Years Experience', 'imputed_RawSalary']]
for i in imputed_num_df:
  sns.displot(imputed_num_df[i] , kind='hist')

  plt.show()

sns.displot(imputed_num_df['imputed_RawSalary'] , kind='hist')

"""==========

## Let's scale / normalize the data in the 'Age' column
"""

sns.displot(df['Age'] ,kind='kde');

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
scaled_age = sc.fit_transform(imputed_num_df[['Age']])

imputed_num_df['ScaledAge']= scaled_age

sns.displot(imputed_num_df['ScaledAge'] ,kind='kde');

imputed_num_df.head(2)

"""==========

## Feature Encoding Exercises

##### Encoding the data in the 'Hobby' / 'Gender' column
"""

df['Hobby'].value_counts()

# Transfer cloumn datatype fot the perpous of encoding
df['Hobby'].astype('category')

from sklearn.preprocessing import OneHotEncoder
model = OneHotEncoder(handle_unknown='ignore')
#enc_df = pd.DataFrame(enc.fit_transform(bridge_df[['Bridge_Types_Cat']]).toarray())

enc = pd.DataFrame(model.fit_transform(df[['Hobby']]).toarray())

df["encodedHobby"] = enc

"""### **And** also, we need to encode the 'Country' column"""

df['Country'].value_counts()

from sklearn.preprocessing import LabelEncoder
model = LabelEncoder()
encoded = model.fit_transform(df[['Country']])

df['EncodedCuntry'] = encoded
df.head()

"""===========

# THANK YOU!
"""