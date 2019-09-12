# DataHack2019

![alt text][logo]

[logo]: https://github.com/YG15/DataHack2019/raw/master/media/logo.png "Logo"


Datahack 2019 project on Armis challenge
[The challange ](https://github.com/armis-security/DataHack2019).


## What are the things in this repo

### Overview
There are three parts to the code.
* Getting the featues - get_final_features.py
* Running the model - submit_final.py
* Explainability code - ``shap_values.py``
 
 
 ## Quick reproduce of the results
 As long as the leaderboard is working you can run this code and it will actually submit the result
 
 ### I just want to run it with pre-created featues file:
```
wget http://unofficialpi.org/share/datahack/only_session_Features_no_log.csv
wget https://raw.githubusercontent.com/YG15/DataHack2019/master/src/requirements.txt
wget https://raw.githubusercontent.com/YG15/DataHack2019/master/src/final/submit_final.py
sudo pip3 install -r requirements.txt
python3 ./submit_final.py
```

The printout should be:

```
{'member': 'The Whale and the Petunias', 'rank': 4, 'score': 0.8753833638145928}
```

 ### I want to create only_session_Features_no_log.csv on my own
 
 Note: Make sure you have ~32GB of free ram for this, and it should run for about 10 mintues on our servers.

```
wget http://unofficialpi.org/share/datahack/only_session_Features_no_log.csv
wget https://raw.githubusercontent.com/YG15/DataHack2019/master/src/requirements.txt
wget https://raw.githubusercontent.com/YG15/DataHack2019/master/src/final/get_final_features.py
sudo pip3 install -r requirements.txt
python3 ./get_final_features.py
```


### Explainability code

The way we used to understand what features are effecting the ones signalling the anomaly is with [SHAP (SHapley Additive exPlanations)](https://github.com/slundberg/shap). The example code pics a single machine and returns the fraction of how much each of the 7 features in ``selected_col`` effected the descision.

to run it use:

```
wget http://unofficialpi.org/share/datahack/only_session_Features_no_log.csv
wget https://raw.githubusercontent.com/YG15/DataHack2019/master/src/requirements.txt
wget https://raw.githubusercontent.com/YG15/DataHack2019/master/src/final/submit_final.py
wget https://raw.githubusercontent.com/YG15/DataHack2019/master/src/final/shap_values.py
sudo pip3 install -r requirements.txt
python3 ./submit_final.py
```

Output is:

```
[[ 0.         -0.00414068 -0.00794539 -0.00891363  0.00211455  0.00373532
   0.01469779 -0.03151073]]
```

Which corresponds to:

```
selected_col = ['network_id',
                'device_id',
                'host_ipnunique',
                'outbound_bytes_countnanmax',
                'timestampcount',
                'timestampnunique',
                'timestamprange',
                'transport_protocolnunique',
                'port_dstnunique']
```
respectively.
 
 ### Running the model - the method we used in the hackathon
 
In order to run the model in the hackathon on sevral machines, we didn't have all access to a 30GB ram server, so we used google collab instead, that code is a litte messy, but you can still take a look at it. 

The upload to collab takes about 30 mintues. Here is the notebook for that:

[Open this notebook](https://github.com/YG15/DataHack2019/blob/master/src/notebook/The_whale_and_the_petunias_pipeline.ipynb) and connect github to google collab. You can also use this button: [Deploy to google Collab](https://colab.research.google.com/github/YG15/DataHack2019/blob/master/The_whale_and_the_petunias_pipeline.ipynb)
 

You can use that notebook to see the thought process that went it to finally getting the cleaned up script above.


## Resources (Hebrew)

<div dir="rtl">

זוהי סקירה די מקיפה ובסיסית של חומר שנראה רלוונטי ברשת, וריכזתי למטה את הכל כדי שתהי גישה מהירה לנושא מסויים אם נחפש אותו, במקום לחפש כל פעם מחדש. לא עשיתי פילטור רציני, אז יש די הרבה חומר - לא הכל בהכרח רלוונטי.

**חומרים:**

  

קודם כל יש  [ריפוסטורי מדהים](https://github.com/yzhao062/anomaly-detection-resources)  שמקבץ מלא מקורות ללימוד בתחום

  

מאמרים קצרים (בעיקר מדיום):

1. מדריכים בסיסיים:

- [מבוא קצרצר על קצה המזלג](https://towardsdatascience.com/5-ways-to-detect-outliers-that-every-data-scientist-should-know-python-code-70a54335a623)

- עוד מבוא אחד  [למתחילים](https://medium.com/@swethalakshmanan14/outlier-detection-and-treatment-a-beginners-guide-c44af0699754)

-  [מבוא קצת יותר מפורט](https://blog.floydhub.com/introduction-to-anomaly-detection-in-python/)

-  [מדריך לבניית מודל זיהוי אנומליות](https://towardsdatascience.com/wondering-how-to-build-an-anomaly-detection-model-87d28e50309) + אחד נוסף

- [Anomaly Detection for Dummies](https://towardsdatascience.com/anomaly-detection-for-dummies-15f148e559c1)

- [שיטות anomaly detection בסיסיות עם קוד בפייתון](https://machinelearningmedium.com/2018/05/02/anomaly-detection/)

- [detecting the onset of machine failure using anomaly detection techniques](https://towardsdatascience.com/detecting-the-onset-of-machine-failure-using-anomaly-detection-techniques-d2f7a11eb809)

-  [Anomaly detection -key features](https://towardsdatascience.com/anomaly-detection-def662294a4e)

(קיצר, מדיום מפוצץ במיני מאמרים - תמצאו את זה שהכי זורם לכן)

2.  [מבוא קצת יותר מפורט עם דוגמאות ל-anomaly detection בפייתון.](https://medium.com/learningdatascience/anomaly-detection-techniques-in-python-50f650c75aaf)

3.  [מבוא עם דוגמא לסדרות עיתיות (פייתון)](https://www.datascience.com/blog/python-anomaly-detection)

4. **[אסטרטגיות anomaly detection for IoT - עושה רושם שרלוונטי עבורנו במיוחד](https://medium.com/analytics-vidhya/anomaly-detection-strategies-for-iot-sensors-6281e84263df)**

5.  [תיאור של כלי בשם RAD שנטפליקס פיתחו על מנת לזהות אנומליות בביג דאטא (בעיקר על סדרות עתיות)](https://medium.com/netflix-techblog/rad-outlier-detection-on-big-data-d6b0494371cc)

6.  [שימוש בסדרות עיתיות כדי לזהות אנומליות ב-IoT](https://www.infoworld.com/article/3386398/how-to-model-time-series-anomaly-detection-for-iot.html)

7. [סקירה קצרצרה על נקודות חשובות לזיהוי אנומליות באופן אפקטיבי](https://www.sans.org/reading-room/whitepapers/hackers/keys-effective-anomaly-detection-37362)  

8.  [זיהוי אנומליות באמצעות ספריית PyOD](https://www.analyticsvidhya.com/blog/2019/02/outlier-detection-python-pyod/)

9.  [מבוא עם דגש על שיטות unsuprvised](https://towardsdatascience.com/unsupervised-machine-learning-approaches-for-outlier-detection-in-time-series-using-python-5759c6394e19)

10.  [מבוא עם דגש על סדרות עיתיות](https://towardsdatascience.com/anomaly-detection-with-time-series-forecasting-c34c6d04b24a)

11. דוגמא לשימוש ב-LSTM עם KERAS

12. [דוגמא לפייפליין שלם בפייתון](https://towardsdatascience.com/machine-learning-for-anomaly-detection-and-condition-monitoring-d4614e7de770)

13.  [דוגמא נוספת לשיטה מסויימת (isolation forest) עם קוד פייתון מלא](https://towardsdatascience.com/anomaly-detection-with-isolation-forest-visualization-23cd75c281e2)

14.  [דוגמא לשימוש בחבילת Prophet](https://towardsdatascience.com/anomaly-detection-time-series-4c661f6f165f)

  

מאמרים יותר מקיפים:

[[1]](https://reader.elsevier.com/reader/sd/pii/S1084804518303886?token=E487F890EF35669B972D34D625B259C0E2EBA55F5222C884E67920E114003B19432090EDAB5D0FBD87556E3D3B555760)  -  **מאמר סקירה על זיהוי אנומליות ברשתות (2019)**

[[2]](https://reader.elsevier.com/reader/sd/pii/S2542660519300241?token=186DBEB26DE44F232978FCE689E29BFCD1CD47A0D6F9A07E14350BC9CDA9B52061B0F87916D2C8A237DD3466840F72B9)  - מאמר על השוואה של אלגורתמים שונים של ML לזיהוי אנומליות במכשירי IoT -עושה רושם רלוונטי

[[3]](https://arxiv.org/ftp/arxiv/papers/1812/1812.00890.pdf)  - מאמר על זיהוי אנומליות בסדרות עיתות של IoT

[[4]](https://arxiv.org/pdf/1901.00402.pdf)  - מאמר על זיהוי אנומליות ברשתות

**[[5]](https://www.researchgate.net/publication/328512658_Anomaly_Detection_in_Networks_Using_Machine_Learning) - סקירה מקיפה מאוד, מהבסיס - על זיהוי אנומליות ברשתות באמצועות ML - נראה מאוד רלוונטי**

**[[6]](http://www.nr2.ufpr.br/~jefferson/pdf/Network_Anomaly_Detection-Methods,_Systems_and_Tools.pdf) -** Network Anomaly Detection: Methods, Systems and Tools (2014

[[7]](https://www.net.in.tum.de/fileadmin/TUM/NET/NET-2017-09-1/NET-2017-09-1_08.pdf)  -  **מאמר קצר על זיהוי אנומליות ברשתות (2017)**

**[[8]](https://link.springer.com/epdf/10.1007/s11235-018-0475-8?author_access_token=-Mo8L2_IB69bLeCC5izR0Pe4RwlQNchNByi7wbcMAY6MQgG9ACzpwohgZsgeuKIPkNcWAwxuBZhoCM9P0hO4R9it1IoP18q09E0jr4QQBTqRE1F1USUDmlxWhtVZuZ6NzgEAY2XRpq8XXPCxZJi_zg%3D%3D) - מאמר סקירה של זיהוי אנומליות ברשתות (2019)**

**[[9]](https://reader.elsevier.com/reader/sd/pii/S1084804515002891?token=E8293736D6FE7BC1DB6BD31192E196A4D13AC840BAD547A672908AA14D90BBA3BCCD8A1ECA74C01F3B581F640D4B9F26)  - ואחד נוסף (2016)**

**[[10]](https://pdfs.semanticscholar.org/f2a9/44c139038253e5a637bba6df2a1cc8985490.pdf?_ga=2.141194418.1019956858.1566806595-1250107886.1566806595)  - מאמר רוויו על הנושא מ-2014**

  

repositories/ חבילות פייתון:

1. lsanomaly -[חבילה שמאפשרת זיהוי אנומליות וקבלת ההסתברות עבורן (לא בינארי)](https://pypi.org/project/lsanomaly/)

2. PyOD - [חבילה די מבוססת (ראו כתבה עליה מפורטת לעיל)](https://pypi.org/project/pyod/)

3. Stumpy -  [חבילה שעושה גם anomaly detection](https://pypi.org/project/stumpy/)

4.  [loglizer](https://github.com/logpai/loglizer)

5. Telemanon -  [משתמשים ב-LSTM בסדרות עיתיות](https://github.com/khundman/telemanom)

6. [keras-anomaly-detection](https://github.com/chen0040/keras-anomaly-detection)

7. [PyNomaly](https://github.com/vc1492a/PyNomaly)

8.  [קוד דוגמא לanomally detection](https://github.com/shubhomoydas/ad_examples)

9.  [אחת נוספת](https://github.com/bozbil/Anomaly-Detection-in-Networks-Using-Machine-Learning)

10. [ואחרונה (שמדגימה שימוש ב-PCA)](https://github.com/andrewenoble/net-detect)

11.  [Prophet](https://github.com/facebook/prophet) גם  [פה](https://facebook.github.io/prophet/)

<div>
  For time-series: Distribution ChangePoint Detection:
  
  1. Review paper + implementation of several models in python:
  https://arxiv.org/pdf/1801.00718.pdf
  https://github.com/deepcharles/ruptures
  
  2. changepoint detectioin - python package that wraps and R package for changepoint detection + explanations
  http://members.cbio.mines-paristech.fr/~thocking/change-tutorial/RK-CptWorkshop.html
  https://pypi.org/project/changepoint/
  
  3. Online changepoint detection - paper + implementation in python
  https://www.icms.org.uk/downloads/CompStratTalks/KNOBLAUCH.pdf
  https://github.com/alan-turing-institute/rbocpdms
