# mindspark-10-team-Renaissaince
This application can recognize your emotion from photo or speech using ML models. It will recommend some songs that are fit to your emotions. It is good for your mental health.


Disclaimer:
  1. In speech_text.ipynb, I refer to these two sources: https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
     https://github.com/amrrs/emotion-detection-from-text-python/blob/main/Text_Emotion_Detection_in_Python.ipynb
  2. In emotion_recog.ipynb, I refer to this source: https://www.kaggle.com/code/anisbouaziz/emotion-recognition. The dataset is fer2013: 
     https://www.kaggle.com/datasets/deadskull7/fer2013
  3. In deploy.py and index.html, I refer to this source: https://github.com/adhibhuta/flask-opencv-photo-camera

Instruction: 
  1. We cannot upload our saved model for image classification due to size limit. Please run emotion_recog.ipynb file first and save the model xcep.h5
  2. To run the web application, open a terminal/cmd in this folder and run "streamlit run deplo.py"
  3. Please check the required libraries for the web application in requirement.txt
