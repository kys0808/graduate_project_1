import pygame  # mp3파일 재생 모듈
import json

#response = '{"bike rider": {"count": 1}, "bollard": {"count": 1}}'  # label이름, count수 dictionary 형태
#response = json.loads(response)  # Dictionary 형태로 저장

# print(response["bike rider"]['count']) count 수 갖고오기
def TTS(response):
    response = json.loads(response)
    for key in response:
        print(key)
        # print(response[key]['count'])
        if key == "person":
            music_file = "speech/person.mp3"
        elif key == "bollard":
            music_file = "speech/bollard.mp3"
        elif key == "bike rider":
            music_file = "speech/bike_rider.mp3"

        """ sampling 속도를 AWS polly 에 맞추어 설정 """
        freq = 23000  # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
        bitsize = -16  # signed 16 bit. support 8,-8,16,-16
        channels = 1  # 1 is mono, 2 is stereo
        buffer = 2048  # number of samples (experiment to get right sound)

        # default : pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        pygame.mixer.init(freq, bitsize, channels, buffer)  # 설정된 값들을 통해 플레이 준비
        """호출 후 while 루프가 없다면 콘솔에서는 mp3 파일이 플레이되지 않는다 """
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()  # file을 play

        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(30)
        pygame.mixer.quit()