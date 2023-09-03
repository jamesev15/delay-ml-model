### Part 0 - Selecting the right model

The goal is to have a model that predicts if there are delays. For that reason, the recall variable needs to be higher
for the class "1" - Delay Class. Following that sentence, there are two models that achieve the goal.

    6.b.i. XGBoost with Feature Importance and with Balance
    6.b.iii. Logistic Regression with Feature Importante and with Balance

Those models have the same recall value for the class "1", 0.69. That way the models reduce the False Negatives cases.  
To choose between those models we can check the F1-score that combines the precision and recall into one metric. Following that sentence
the model will be the "XGBoost with Feature Importance and with Balance" since the model has 0.66 of f1-score, 0.01 more than the other model.

The right model will be "XGBoost with Feature Importance and with Balance"

### Part I - Model development

#### Preprocess
The preprocess step takes a dataframe that needs to be preprocessed before passing it to the fit or predict step.
An iteration over the dataframe is performed to extract the features if those are into the dataframe. If the features are there,
then a new row with True values for the features are added to the final dataframe.  

If the target colum is specified then the target dataframe is returned by computing the difference between estimated arrival and real arrival
with a threshold of 15 min to indicate if there is a delay.

#### Fit
The fit step takes de features already processed and the target in order to train the selected model defined in the previous section.  
This step is validated by testing modules checking the following parameters.  

    recall for no-delay < 0.60
    f1-score for no-delay < 0.70
    recall for delay > 0.60
    f1-score for delay > 0.30


#### Predict
The predict step takes the features already processed in order to predict by loading and executing the pre-saved model.  
This predict step is the core of the realtime execution.


### Part II - API development
The DelayModel is the core of the API powered by FastAPI, an async framework with great performance such as nodejs and golang, 
the new fastapi'versions are based on pydantic v2 which is faster than pydantic v1 since the v2 is made using Rust.  

#### Predict step
The predict step takes a dictionary which is validated using pydantic. For that, pydantic models were created, those models validate 
the month(which needs to be between 0 and 12), the flight type(which needs to be National or International) and the operator(which needs
to be part of the following list)

    available_operators = [
            "Grupo LATAM",
            "Sky Airline",
            "Aerolineas Argentinas",
            "Copa Air",
            "Latin American Wings",
            "Avianca",
            "JetSmart SPA",
            "Gol Trans",
            "American Airlines",
            "Air Canada",
            "Iberia",
            "Delta Air",
            "Air France",
            "Aeromexico",
            "United Airlines",
            "Oceanair Linhas Aereas",
            "Alitalia",
            "K.L.M.",
            "British Airways",
            "Qantas Airways",
            "Lacsa",
            "Austral",
            "Plus Ultra Lineas Aereas",
        ]
If the validations fail then an HTTP Custom Exception will raise as following:

    "MonthException" if the month is not between 0-12
    "FlightTypeException" if the flight type is not national or international
    "OperatorException" if the operator is not in the above list.


### Part III - IV - Test review - CI/CD Pipelines
The testing is an important step that is part of the Continuous Integration Pipeline.  
The app deployment using a cloud provider is part of the Continuous Deployment Pipeline.

In this case, AWS is selected to deploy the app, the service used is App Runner since it's easier to put in production a 
container.  
Note: App Runner is configured to change the docker image every time a new image is pushed into the ECR(Docker Repository for AWS).

#### CI Pipeline
The pipeline tests the model and api only for the develop and main branches, for other branches there is no validation.

#### CD Pipeline
The pipeline builds a docker image that contains the app and pushes it to AWS ECR only for the main branch. It will be a good idea to
deploy in other environments such as DEV, QA.   
To perform this step, github secrets were used to keep the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY safe 
since AWS App Runner will update the service using the latest image, there is nothing else to do.  
The last step is to run the stress test to check the quality of the API.

The following image shows the aws secrets definition into github  
<img width="879" alt="image" src="https://github.com/jamesev15/delay-ml-model/assets/84110446/150e3215-85ff-4d56-9c42-853449368874">

The following image shows the app configured and deployed in AWS  
<img width="1424" alt="image" src="https://github.com/jamesev15/delay-ml-model/assets/84110446/3c4769f6-21e7-4cda-a13d-114398bbf591">

The following image shows the CI/CD actions performed by github actions  

<img width="1434" alt="image" src="https://github.com/jamesev15/delay-ml-model/assets/84110446/06ff82a6-6e6b-4ca8-93eb-dc5a067f2841">
Note: The CD pipeline only runs in the main branch, since there is no other environments suchs as DEV or QA for deployment.

### Testing
Check the status of the app doing a GET request to this URL. 
    
    https://9pgzepmvm3.us-east-2.awsapprunner.com/health

Get a prediction of the app doing a POST request to this URL.

    https://9pgzepmvm3.us-east-2.awsapprunner.com/predict

    json payload: {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas", 
                    "TIPOVUELO": "N", 
                    "MES": 3
                }
            ]
        }

