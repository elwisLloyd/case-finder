# Image detection as a service

Источник: https://medium.com/bumble-tech/image-detection-as-a-service-9bd463f74f43

Across our two apps Badoo and Bumble, we have over millions registered users worldwide uploading millions of photos a day to our platform. These images provide us with a rich data set from which we derive a wealth of insights.
Within our Data Science team, we created a service where images are input, and output is the image content information. We use this service during our prototyping phase, during our exploratory analysis and for delivering ad-hoc insights to the business about image content.
For example, we have observed that if someone is wearing sunglasses in all of their pictures they tend to receive fewer likes than users who clearly show their faces. This enables us to provide tips to users on how to enhance their profiles.
In this blog, I explain how we combined Deep Neural Networks and Flask APIs to offer this service.
Computer Vision Tasks
Our API serves a variety of models, providing different types of information on image content.
Image Classification
One model type that our service supports is that of an image classification problem. The models we have trained classify the images with a variety of targets. For example, the service can predict if the person in the image is smiling or wearing sunglasses.
Textual Descriptions
In addition to image classification models, our service can also provide a textual description of images.
This model uses a combination of a CNN and an LSTM in order to output the sentence.
Object Detection
Finally, the service can also detect objects present in an image using YOLO. For this, we are using an off-the-shelf GitHub repository.
Having built the initial prototype of our models, we then needed to further assess the value and possible impact these could have on business.
Impact & Workflow
During the execution of projects, we carry out a number of potential impact analyses. These give an estimate of the value we expect the project to deliver as we learn more and progress throughout the process. The purpose of this is to ensure that resources get allocated effectively and that what we produced delivers maximum impact on the business. The visual below outlines the workflow we aim for.
During the prototyping phase of our computer vision models, we need to be able to assess what the possible impact might be on the business if we were to allocate resources and productionise them. In order to assess this fully, we needed to be able to scale the number of images we could score. To this end, we built a Flask framework to enable us to serve the models on a greater scale compared to using a local machine.
Web API
Once we had trained our models using Jupyter notebooks and .py scripts we wanted other members of the team and people across the business to be able to use them to support their prototyping efforts and potential impact reviews. To achieve this, we decided to encapsulate the models in REST APIs. An API essentially allows you to interact over HTTP, making requests to specific URLs and getting relevant data back in the response.
Why APIs?
The reason we decided to use APIs is that it makes it easy for cross-language applications to work well. For example, when it’s necessary for a front-end developer to use these models, they simply need to get the endpoint of the API and have no need to be familiar with Python or have domain-specific knowledge.
Get Laura Mitchell’s stories in your inbox
Join Medium for free to get updates from this writer.
There are a host of third-party solutions offering machine vision APIs including Google Cloud Vision and AWS Rekognition. We decided against going down this route in the interests both of minimising costs and keeping our data in-house. We used Python Flask to build and serve our API in-house. Flask is a microframework for Python and offers a powerful way of annotating Python functions with REST endpoints.
Why Flask?
Flask and Django are relatively comparable to Python web frameworks. We decided to use Flask over Django because it is very simple and easy to get started with whereas Django is quite heavy for building web applications. Simplicity and flexibility being two key requirements for our service also influenced our decision.
The Basics
The following code represents a minimal Flask-RESTful API and forms the basis of our service.
from flask import Flask
from flask_restful import Resource, Apiapp = Flask(__name__)
api = Api(app)class MagicLab(Resource):
def get(self):
return {Magic: Lab}api.add_resource(MagicLab, '/')if __name__ == '__main__':
app.run(debug=True)
This API can be enabled by saving it as a server.py file and using the Python interpreter.
$ python server.py
* Running on http://127.0.0.1:5000/
* Restarting with reloader
From here use cURL, an open-source command-line tool that allows the easy transfer of data. Using cURL makes it easy to compose and send HTTP requests to the service and check the responses.
$ curl http://127.0.0.1:5000/
{"Magic": "Lab"}
Serving Models
By including them in our server .py file the pre-trained models are loaded to the service at the point when it starts.
smiling_model = load_model('models/smiling.h5')
sunglasses_model = load_model('models/sunglasses.h5')
Uploading Images
Our service accepts images sent to it and saves them in a specified location, as shown below.
app = Flask(__name__)basedir = os.path.abspath(os.path.dirname(__file__))app.config.update(
UPLOAD_FOLDER=os.path.join(basedir, 'magiclab_images')
)
Making Predictions
Once our image has been uploaded to the service from the request, we are able to make predictions using the models on the service.
We define a function to make the predictions as follows:
def make_predictions(model):
def make_predictions(model):
img = load_img(image_file_path, target_size=(img_width, img_height))
img_tensor = image.img_to_array(img)
img_tensor = np.expand_dims(img_tensor, axis=0)
img_tensor /= 255.
p = model.predict(img_tensor).tolist()
p = p[0:1][0][1]  
return p
The code extract gives an example as to how we can make predictions about whether or not the user in the image is smiling and wearing sunglasses.
@app.route("/", methods=['POST', 'PUT'])
def features():
f = request.files['file']
save_image(f)
pred = {}
p = make_predictions(sunglasses_model)
pred.update({'probability_{}'.format('sunglasses'): p})
p = make_predictions(smiling_model)
pred.update({'probability_{}'.format('smiling'): p})
return jsonify(pred)
Sending Requests & Serving Predictions
Now that our server is up and running, requests and images can be sent to it and a response received in the following way. The response gives the probability of certain features being present in the image.
Request
curl -X POST -F file=@'/Users/lauramitchell/Desktop/image_1_example.jpg' http://127.0.0.1:5000/
Response
{‘prob_smiling’: 0.11, ‘prob_sunglasses’: 0.20}
The illustration below demonstrates the overall process of our service in simple terms.
Hosting the Service
GPUs
Once our Flask API was up and running on a local machine, we then packaged up the service as an application on one of our servers for easy access by other people in the business. On these servers, we have GPUs which help to accelerate the computational time.
Responses
We can make requests to the server via a Jupyter notebook and review the response times.
Docker
In order to containerise the service on our server, we created a Docker container from an image. If you are not familiar with Docker I would recommend taking a look at their documentation online as it is very thorough and digestible.
To start the service, we run a Docker container on one of our images and then enter the container. From here we can start the service as shown below.
lmitchell@bi19.mlan:~> docker exec -it a92ca5029500 bash
root@bi19:/# python server.py
At last, our service is ready to go!
Summary
The infrastructure we have developed is primarily used by the Data Science team when carrying out exploratory pieces of work, performing ad-hoc analysis and during our model prototyping phase. We also use the service to help to determine whether we should be investing resources into putting the models onto production. We have found that the framework allows our team to work in a more unified yet flexible way.
If you have any suggestions/feedback feel free to comment below.
If contributing to projects such as this are of interest to you, we are hiring so feel free to get in touch and find out more about joining the MagicLab family! 🙂
