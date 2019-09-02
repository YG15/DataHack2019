Outlier detection data taken from: http://odds.cs.stonybrook.edu/

Converted from .mat to .csv. 
data (X) and outlier labels (y) concatenated with y as last column. 
Read with no headers. 

** EDIT: After playing with the ForestCover dataset and getting very poor results with both DBScan and isolated forest, I think this is a bad dataset for an unsupervised oulier detection task (as opposed to supervised classification). This is because the data points labeled as outliers are easily separable from the others, but are too clustered together in one part of the feature space to qualify as outliers as they are defined by these algorithms - i.e., being sufficiently far from other data points. In other words, the algorithms found outliers all around the sparse outskirts of the feature space while the labeled outliers were all found in one side of it. 
** 

Dataset		points		dim		outliers
____________________________________________________________
Musk		3062		166		97 (3.2%)
ForestCover	286048		10		2747 (0.9%)


Musk dataset
Dataset information
The original musk dataset from UCI machine learning repository contains several musk and non-musk classes. The non-musk classes j146, j147, and 252 are combined to form the inliers, while the musk classes 213 and 211 are added as outliers without downsampling. Other classes are discarded. 

Source (citation)
C. C. Aggarwal and S. Sathe, “Theoretical foundations and algorithms for outlier ensembles.” ACM SIGKDD Explorations Newsletter, vol. 17, no. 1, pp. 24–47, 2015.

Downloads
File: musk.mat

Description: X = Multi-dimensional point data, y = labels (1 = outliers, 0 = inliers)




ForestCover/Covertype dataset
Dataset Information
The original ForestCover/Covertype dataset from UCI machine learning repository is a multiclass classification dataset. It is used in predicting forest cover type from cartographic variables only (no remotely sensed data). This study area includes four wilderness areas located in the Roosevelt National Forest of northern Colorado. These areas represent forests with minimal human-caused disturbances, so that existing forest cover types are more a result of ecological processes rather than forest management practices. This dataset has 54 attributes (10 quantitative variables, 4 binary wilderness areas and 40 binary soil type variables). Here, outlier detection dataset is created using only 10 quantitative attributes. Instances from class 2 are considered as normal points and instances from class 4 are anomalies. The anomalies ratio is 0.9%. Instances from the other classes are omitted.

Source (citation)
Liu, Fei Tony, Kai Ming Ting, and Zhi-Hua Zhou. “Isolation forest.” 2008 Eighth IEEE International Conference on Data Mining. IEEE, 2008.

K. M. Ting, J. T. S. Chuan, and F. T. Liu. “Mass: A New Ranking Measure for Anomaly Detection.“, IEEE Transactions on Knowledge and Data Engineering, 2009.

Kai Ming Ting, Guang-Tong Zhou, Fei Tony Liu & Tan Swee Chuan. (2010). Mass Estimation and Its Applications. Proceedings of The 16th ACM SIGKDD Conference on Knowledge Discovery and Data Mining 2010. pp. 989-998.

Swee Chuan Tan, Kai Ming Ting & Fei Tony Liu. (2011). Fast Anomaly Detection for Streaming Data. Proceedings of the International Joint Conference on Artificial Intelligence 2011. pp.1151-1156.

Download
File: cover.mat

Description: X = Multi-dimensional point data, y = labels (1 = outliers, 0 = inliers)
