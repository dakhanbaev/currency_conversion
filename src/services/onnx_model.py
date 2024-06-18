import onnxruntime as rt  # use 1.15.1 version
import numpy as np
from PIL import Image


class ONNXModel:
    def __init__(self, model_path: str = 'src/services/resources/efficientnet-lite4-11.onnx'):
        self.sess = rt.InferenceSession(model_path)
        self.input_name = self.sess.get_inputs()[0].name
        self.output_name = self.sess.get_outputs()[0].name

    def predict(self, image: Image.Image):
        input_data = self.preprocess_image(image)
        result = self.sess.run([self.output_name], {self.input_name: input_data})
        return result

    @staticmethod
    def preprocess_image(image: Image.Image):
        image = image.resize((224, 224))
        image = np.array(image).astype('float32')
        image = np.expand_dims(image, axis=0)
        image /= 255.0
        return image

