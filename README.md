# VoEyesCon: 아이트래킹과 음성인식을 활용한 PC/LAPTOP 제어 시스템
## 개요

컴퓨터 사용에 어려움을 겪는 장애인을 비롯하여 시각과 음성을 통해 더 편리한 PC 제어 기능을 원하는 사용자들을 위해 인공지능 기반의 컴퓨터 제어 시스템을 개발하고자 하였습니다.   
전용 하드웨어를 사용하는 기존 방식과 달리 외ㆍ내장 웹캠과 마이크를 통해 아이트래킹과 음성명령을 통한 마우스 제어를 수행함으로써 컴퓨터 사용성을 크게 향상시킬 수 있습니다.

<img width="400" alt="개요" src="https://user-images.githubusercontent.com/81609037/171325852-8fa21f56-32f9-4de3-a2af-211f3693ace3.png"><br/>

## 참고 솔루션

### UnityEyes: 눈 이미지 생성 프로그램
- https://www.cl.cam.ac.uk/research/rainbow/projects/unityeyes/

### GazeML: 시선추적 학습 딥러닝 프레임워크
- https://github.com/swook/GazeML

### Calibration: 시선방향을 모니터 화면에 대응시키는 알고리즘
- https://github.com/chuuuul/arto_eye/
<br/>

## 시스템 구성 및 PC/LAPTOP 제어 실행 절차

<img width="694" alt="시스템 구성" src="https://user-images.githubusercontent.com/81609037/171329100-7fd52d66-65c8-4cb4-a5ec-4dc1b47d8bae.png">
<img width="231" alt="시스템 구성" src="https://user-images.githubusercontent.com/81609037/171329419-bae2b51f-3e7d-432f-b163-a932ff4cd287.png"><br/>

* 회원관리가 필요한 이유는 사용자마다 아이트래킹 정확도를 특정하기 위함입니다.<br/>
* 프로그램 실행은 main.py 파일을 실행하면 됩니다.<br/>

## UI

<img width="950" alt="프로그램 UI" src="https://user-images.githubusercontent.com/81609037/171331136-a3fd1726-248e-45d0-8785-25a6d3661e3c.png"><br/>

* 현재는 4번 UI에 Calibration 실행을 PC/LAPTOP 제어 실행에 포함시킨 상태이므로 추후 이 부분을 개선해야합니다.

## 프로그램 실행에 필요한 환경구축 (OS: 윈도우10)

* 프로그래밍 언어: python
* 설치모듈 
    * numpy  
    * tensorflow  
    * keras  
    * ujson-segfix  
    * coloredlogs  
    * cmake  
    * dlib  
    * opencv-contrib-python
    * pymysql 
    * pyaudio  
    * speechrecognition  
    * pyautogui  
