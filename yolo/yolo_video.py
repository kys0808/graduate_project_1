import sys
import argparse
#from yolo import YOLO, detect_video
from yolo2 import YOLO, detect_video
from PIL import Image


def detect_img(yolo):   # input : yolo 클래스(yolo.py)
    while True:
        img = input('Input image filename:')
        # file 이름 저장 변수 : img
        try:
            image = Image.open(img)
        except:
        # image open 실패 일 때, except: 실행
            print('Open Error! Try again!')
            continue
        else:
        # 성공적으로 image open 일 때, yolo.py 의 detect_image() 함수 호출
            r_image = yolo.detect_image(image)
        # yolo.py 의 detect_image() 함수 결과를 r_image에 저장 , 이 후 output 으로 제시
            print(r_image)
            r_image.show()
    yolo.close_session()

FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        # input 데이터(사진파일)가 있으면 detect_img() 함수 실행
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        # YOLO클래스 생성해서 detect_img() 실행
        detect_img(YOLO(**vars(FLAGS)))

    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
