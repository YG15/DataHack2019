Kaggle credit card fraud detection dataset
Download from https://www.kaggle.com/mlg-ulb/creditcardfraud/downloads/creditcardfraud.zip/3 
(not on repo).

Dataset		          points		dim		outliers
____________________________________________________________
Kaggele credit card	284807		31		492 (0.17%)



Outlier detection data sets taken from: http://odds.cs.stonybrook.edu/

Converted from .mat to .csv. 
data (X) and outlier labels (y) concatenated with y as last column. http and smtp datasets were combined. 
Read http/smtp csv data with header, others with no header. 


Dataset		points		dim		outliers
____________________________________________________________
Http (KDDCUP99)	567479		3		2211 (0.4%)
Smtp (KDDCUP99)	95156		3		30 (0.03%)
ForestCover	286048		10		2747 (0.9%)
Musk		3062		166		97 (3.2%)


*** Some conclusions: http/smtp work very well with an isolated forest approach (aUC=0.996). However the forest cover data set is not suitable for unsupervised anomaly detection because its "outlier" class is a pretty dense cluster of points in one part of the feature space (i.e. works as a supervised classification problem). ***


http (KDDCUP99) dataset
Dataset Information
The original KDD Cup 1999 dataset from UCI machine learning repository contains 41 attributes (34 continuous, and 7 categorical), however, they are reduced to 4 attributes (service, duration, src_bytes, dst_bytes) as these attributes are regarded as the most basic attributes (see kddcup.names), where only ‘service’ is categorical. Using the ‘service’ attribute, the data is divided into {http, smtp, ftp, ftp_data, others} subsets. Here, only ‘http’ service data is used. Since the continuous attribute values are concentrated around ‘0’, we transformed each value into a value far from ‘0’, by y = log(x + 0.1). The original data set has 3,925,651 attacks (80.1%) out of 4,898,431 records. A smaller set is forged by having only 3,377 attacks (0.35%) of 976,157 records, where attribute ‘logged_in’ is positive. From this forged dataset 567,497 ‘http’ service data is used to construct the http (KDDCUP99) dataset. 

Source (citation)
Kenji Yamanishi, Jun-Ichi Takeuchi, Graham Williams, and Peter Milne. On-line unsupervised outlier detection using finite mixtures with discounting learning algorithms. In Proceedings of the sixth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pages 320–324, New York, NY, USA, 2000. ACM Press.

Graham Williams, Rohan Baxter, Hongxing He, Simon Hawkins, and Lifang Gu. A comparative study of rnn for outlier detection in data mining. In Proceedings of the 2002 IEEE International Conference on Data Mining, page 709, Washington, DC, USA, 2002. IEEE Computer Society.

Liu, Fei Tony, Kai Ming Ting, and Zhi-Hua Zhou. “Isolation forest.” 2008 Eighth IEEE International Conference on Data Mining. IEEE, 2008.

K. M. Ting, J. T. S. Chuan, and F. T. Liu. “Mass: A New Ranking Measure for Anomaly Detection.“, IEEE Transactions on Knowledge and Data Engineering, 2009.

Kai Ming Ting, Guang-Tong Zhou, Fei Tony Liu and Swee Chuan Tan, Mass Estimation and Its Applications. In Proceedings of the 16th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD), 989-998, Washington, DC, 2010.

Swee Chuan Tan, Kai Ming Ting & Fei Tony Liu. (2011). Fast Anomaly Detection for Streaming Data. Proceedings of the International Joint Conference on Artificial Intelligence 2011. pp.1151-1156.

Download
File: http.mat

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




Musk dataset
Dataset information
The original musk dataset from UCI machine learning repository contains several musk and non-musk classes. The non-musk classes j146, j147, and 252 are combined to form the inliers, while the musk classes 213 and 211 are added as outliers without downsampling. Other classes are discarded. 

Source (citation)
C. C. Aggarwal and S. Sathe, “Theoretical foundations and algorithms for outlier ensembles.” ACM SIGKDD Explorations Newsletter, vol. 17, no. 1, pp. 24–47, 2015.

Downloads
File: musk.mat

Description: X = Multi-dimensional point data, y = labels (1 = outliers, 0 = inliers)

