import rospy
import sys
import cv2
from sensor_msgs.msgs import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
import numpy as np

class cvBridgeDemo():
    # cvBridgeDemo 라는 클래스 생성, CvBridge 함수 설명
    def __init__(self):
        self.node_name = "cv_bridge_demo"
        #ros node 초기설정
        rospy.init_node(self.node_name)

        #shutdown 시 수행하는 작업
        rospy.on_shutdown(self.cleanup)

        #cv_bridge object 생성
        self.bridge = CvBridge()

        #카메라 이미지와 깊이 정보를 subcribe 하고 적절한 callback을 설정
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.image_callback)
        self.depth_sub = rospy.Subscriber("/camera/depth/image_raw",Image,self.depth_callback)

        #callback은 타이머의 시간이 끝났을 때 실행
        rospy.Timer(rospy.Duration(0.03),self.show_img_cb)
        rospy.loginfo("Waiting for image topics")

    #RGB image, processed RGB image, depth image 시각화
    def show_img_cb(self,event):
        try:

            cv2.namedWindow("RGB_Image",cv2.WINDOW_NORMAL)
            cv2.moveWindow("RGB_Image",25,75)
            cv2.namedWindow("Processed_Image",cv2.WINDOW_NORMAL)
            cv2.moveWindow("Processed_Image",500,75)
            #depth정보
            cv2.moveWindow("Depth_Image",950,75)
            cv2.namedWindow("Depth_Image",cv2.WINDOW_NORMAL)

            cv2.imshow("RGB_Image",self.frame)
            cv2.imshow("Processed_Image",self.display_image)
            cv2.imshow("Depth_Image",self.depth_display_image)
            cv2.waitKey(3)
        except:
            pass
    #Kinect로 부터 color image 전달
    def image_callback(self, ros_image):
        #cv_bridge 이용하여 ROS image 를 Opencv 형태로 변환
        try:
                self.frame = self.bridge.imgmsg_to_cv2(ros_image,"bgr8")
        except CvBridgeError, e:
            print e
            pass
        # 대부분의 cv2 함수들이 numpy array를 요구하기 때문에 image를 Numpy array로 변환
        frame = np.array(self.frame, dtype=np.uint8)
        #process_image()함수를 이용하여 frame 가공
        self.display_image = self.process_image(frame)

    #Kinect로 부터 depth image 전달
    def depth_callback(self, ros_image):
        # cv_bridge 이용하여 ROS image 를 Opencv 형태로 변환
        try:
            #depth image는 single-channel float 32 image임
            depth_image = self.bridge.imgmsg_to_cv2(ros_image,"32FC1")
        except CvBridgeError, e:
            print e
            pass
        # 대부분의 cv2 함수들이 numpy array를 요구하기 때문에 depth image를 Numpy array로 변환
        depth_array = np.array(depth_image,dtype=np.float32)
        # depth image가 0(검정) 또는 1(흰)이 되도록 일반화
        cv2.normalize(depth_array, depth_array, 0, 1, cv2.NORM_MINMAX)
        # depth image 가공
        self.depth_display_image = self.process_depth_image(depth_array)

    #color image를 흑백으로, 흐리게 바꾸고, 모서리 찾기
    def process_image(self,frame):
        #흑백으로
        grey = cv2.cvtColor(frame, cv.CV_BGR2GRAY)

        #흐리게
        grey = cv2.blur(grey,(7,7))

        #모서리 찾기
        edges = cv2.Canny(grey,15.0,30.0)

        return edges

    #depth frame 리턴
    def process_depth_image(self,frame):
        #raw image 리턴
        return frame

    #node shutdown 되면 image 창 닫기
    def cleanup(self):
        print "Shutting down vision node"
        cv2.destroyWindow()

def main(args):
    try :
                cvBridgeDemo()
                rospy.spin()
    except KeyboardInterrupt:
                print "Shutting down vision node."
                cv2.destroyWindow()
if __name__ == '__main__':
    main(sys.argv)
