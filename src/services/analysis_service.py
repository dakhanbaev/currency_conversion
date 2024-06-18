import ffmpeg
import logging
import json
from src.services.onnx_model import ONNXModel
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)


class AnalysisService:
    def __init__(self, model: ONNXModel = ONNXModel(), ffmpeg_path='ffmpeg'):
        self.model = model
        self.ffmpeg_path = ffmpeg_path

    def analyze(self, file_path, content_type):
        if content_type.startswith('video'):
            return self.analyze_video(file_path)
        elif content_type.startswith('image'):
            return self.analyze_image(file_path)
        else:
            raise Exception(f'Unsupported format : {content_type}')

    def analyze_video(self, video_path):
        try:
            probe = ffmpeg.probe(video_path, show_entries='stream=index,codec_type,width,height', of='json')
            logger.info("Full probe result:", json.dumps(probe, indent=4))
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error: {e.stderr.decode()}")
            return []

        video_stream = next((stream for stream in probe['streams'] if stream.get('codec_type') == 'video'), None)

        if not video_stream:
            raise ValueError("No video stream found")

        width = int(video_stream['width'])
        height = int(video_stream['height'])
        frame_size = width * height * 3

        process = (
            ffmpeg
            .input(video_path)
            .output('pipe:1', format='rawvideo', pix_fmt='rgb24')
            .run_async(pipe_stdout=True, pipe_stderr=True, cmd=self.ffmpeg_path)
        )

        result = []
        frame_number = 0

        while True:
            in_bytes = process.stdout.read(frame_size)
            if not in_bytes:
                break

            try:
                frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
                image = Image.fromarray(frame)

                prediction = self.model.predict(image)
                result.append(prediction)
                frame_number += 1
            except Exception as e:
                logging.error(f"Error processing frame {frame_number}: {e}")
                break

        process.wait()
        return result

    def analyze_image(self, file_path: str) -> list:
        image = Image.open(file_path)
        return [self.model.predict(image)]


