# Blur Classifier: Image Quality Detector

Источник: https://medium.com/cars24-data-science-blog/blur-classifier-image-quality-detector-7c1de5ff8e59

With over a million cars inspected and unloaded in recent years, we at CARS24 have a significant amount of knowledge and expertise with vehicle defects that result in unpleasant aspects for the next owner. Irrespective of how much efforts humans put in car evaluation it will always have subjectivity of evaluator built into it. We in DS@cars24 are standardizing this experience.
Finding appropriate photos to feed to models for learning is one of the most difficult difficulties in images. The photos in the pipeline can contain several image quality artefacts such as reflections, blur etc. as shown in figure 1. In our scenario, a fault miss or, for that matter, over reporting might cost us a lot of money and provide a poor customer experience, which is not desirable. So, first and foremost, we must ensure that the pictures used for learning or detection are devoid of artefacts. One such major image quality artefact is blur detection. Let’s Dive deep in our Blur Detection algorithm.
Blur detection
The most crucial aspect for any computer vision algorithm is the data. If the data fed to the machine is inappropriate, it can give a wrong predictions.
When an image contains blur artefact, the change in the intensity of pixel value along the edges of the object and background decreases.
Example:
Consider a simple image, with four colors as shown in figure 2.
The code to generate such an image is:
import numpy as np
import cv2img = np.zeros((256, 256, 3), dtype = 'uint8')
img[:,:128,0] = 255
img[:,128:,2] = 255img[:128,:,0] = 255
img[128:,:,1] = 255cv2.imshow("Input Image", img)
cv2.waitKey(0)
Using implementation of blur by open-cv , the effect observed in such a low dimensional image is:
# Please Note: The parameters used for kernel size and anchor point # are used as an example. You can vary these and see the variation  # in results.
blur = cv2.GaussianBlur(img,(5,55),0)
cv2.imshow("Blurred Image", blur)
cv2.waitKey(0)
This difference is also evident in the pixel values at the same location of the image at the location of the edges as shown in fig4A and fig4B for blurred image and sharp image respectively.
These intensity changes along the edges are extremely critical to detect any anomaly in the image. These artefacts result in an increase in false positives and false negatives.
There has been a lot of academic research in detecting blur and correcting it using generative algorithms. However, the scope of our problem is different. We are only interested in blur detection. If an image with blur artefact is detected, we would prefer to not predict on the particular image, rather than give a false prediction. Since, this algorithm/model is a prerequisite for every image, it needs to be lightweight as well as accurate.
To combat this, we developed our own in-house algorithm.
What is a Blurry image?
If we had to explain the “Blur” from a visual standpoint, we could say that a hazy image that lacks definite borders. The main causes of blurry photographs are Camera movement, subject movement, dirty lens, missing focus, inadequate depth of field, and lens softness. The contrast between clear and fuzzy photos may be seen in the example figures 5 and 6.
How did we counter this?
Get Archit Jain’s stories in your inbox
Join Medium for free to get updates from this writer.
We employed the discrete cosine transform (DCT) for this, which turns data points into the form of a sum of cosine functions oscillating at different frequencies.
Why DCT?
The discrete cosine transform (DCT) renders a picture as a sum of sinusoids with different magnitudes and frequencies. The majority of the visually important information is contained in just a few DCT coefficients. For example, the DCT is frequently employed in picture compression applications. For example, the DCT lies at the heart of the JPEG lossy image compression method, which is an international standard. As a result, DCT is both effective and lightweight.
Using image processing techniques like DCT, help in making our algorithm lightweight as well as accurate for many applications involving image quality. The use of deep learning for this particular problem statement is an overkill.
What did we do?
We used the Discrete cosine transform on each 8x8 non-overlapping block in the image. As shown in the diagram, each block is then divided into three areas, R1, R2, and R3, which represent the low frequency (LF), medium frequency (MF), and high frequency (HF) regions, respectively.
B = 8
im = cv2.imread(img_path)
im_yuv = cv2.cvtColor(im, cv2.COLOR_BGR2YUV)
im_y, im_u, im_v = cv2.split(im_yuv)strides = np.float32(
np.lib.stride_tricks.as_strided(
im_y,
shape=(im_y.shape[0] // B, im_y.shape[1] // B, B, B),
strides=(
im_y.strides[1] * B * im_y.shape[1],
2 * 8,
im_y.shape[1] * im_y.strides[1],
im_y.strides[1],
),
)
).reshape((-1, 8, 8))
currentblock = list(map(cv2.dct, sampled_strides))
Local statistics (mean, variance, kurtosis, skewness, entropy, and energy of all AC components composing each region) are computed for each frequency range and are made up of the averages of the various statistics discovered in all of the image’s blocks. As a result, the descriptor vector of each will have 18 characteristics. (6 features x 3 regions = 18 features)
Based on 18 attributes of a picture, we trained a classifier to classify blurry images. The main reason for using DCT was to have a light weighted and accurate feature extractor.
Performance
The accuracy for the best model achieved was 91.06%. The time taken for the whole algorithm on an image of size 1080x1920x3 was 12ms on single core CPU machine making it accurate as well as fast for the profundus module.
Some output examples for out-of-time samples:
Tagged Blur
Tagged Sharp
Blur detection was one of our module’s major tasks to estimate image quality, it falls in the umbrella of solutions we are developing to scale and standardise condition estimation using image, which we will discuss in another blog.
Conclusion
To summarize, profundus-created models such as damage estimation and blur detection are assisting Cars24 in going a notch above in procurement and inspection aspects, and when combined with other modules, makes the selling and purchasing pipeline easy, fast, and cost-effective. Watch this space for more…
Authors : Vansh Gupta , Data Science Intern @ CARS24, Archit Jain , Data Scientist @ CARS24, Vaibhav Baswal ML Engineer 2 @ CARS24, Abhay Kansal , Staff Data Scientist @ CARS24
