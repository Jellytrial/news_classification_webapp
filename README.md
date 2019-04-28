# news_classification_webapp
- Function：Input the news article URL of Gunosy and return the category classified by Naive Bayes Model.

## Environment
- Docker 18.09.2
- Python 3.6.8
- Django 1.11

## Code Style Convention
Automaticlly PEP8 check by travi-ci

## Training data
3200 news articles from 8 categories (エンタメ,スポーツ,おもしろ,国内,海外,コラム,IT・科学,グルメ) of Gunosy news web site `https://gunosy.com/`.

## Web app usage
#### 1. Clone news_classification_webapp from Github
`$git clone https://github.com/Jellytrial/news_classification_webapp.git`

#### 2. Move to news_classification_webapp folder
`$cd news_classification_webapp`

#### 3. Build up docker container
In oder to build contianer, make sure you have installed docker.  
`$docker-compose build`

#### 4. Run web app
`$docker-compose up`  

#### 5. Enter into web app
After launching, please input following URL in browser:  
`http://127.0.0.1:8000/`  
Then input news article URL of Gunosy, it will return the category. 

#### 6. Evaluate model and save model
`$docker-compose run app python evaluation.py`

## Model evaluation
All classifiers are evaluated with cross validation score.  
#### 1. Comparison of different classifiers
Following models are evaluated with 3200 data size.  

|Model|Accuracy|
|:----:|:-----:|
|My Naive Bayes Model|0.9434|
|Logistic Regression|0.9272|
|SGD|0.9303|
|Random Forest|0.8970|
|K-Neighbors|0.8469|
|Linear SVC|0.9335|

#### 2. Works on improving accuracy
a. Increase data size from 800 to 3200，and accuracy grows from 0.7989 to 0.9434.  
b. Increase training data from words of article title to words both in title and article content.  
c. Transform news contents to category-word frequency form by words count.   
