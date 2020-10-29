import os
import sys
import cv2
import csv
import rospy, rosbag
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

if len(sys.argv) == 3:
   sys.argv[1] = sys.argv[1] + ".dir"
   out_dir = sys.argv[1]
   if not os.path.exists(sys.argv[1]):
       os.makedirs(out_dir)

   else:
       print sys.argv[1], 'already exists'
       sys.exit()

   bagfile = sys.argv[2]

else:
   print 'illegal arguments exeption.'
   sys.exit()

bridge = CvBridge()

def main():

   topicNames = {'/k4a/depth_to_rgb/image_raw', '/camera1/image_color', '/camera2/image_color', '/k4a/rgb/image_raw'}

   inbag_name = bagfile

   print "open rosbag file..."
   bag = rosbag.Bag(inbag_name)
   counter = 0
   for topic, msg, t in bag.read_messages():
        '''
        if counter == 0:
            pass
        else:
            if counter == 10:
                counter = 0
            continue
        '''
        if topic in topicNames:
           try:
               img = CvBridge().imgmsg_to_cv2(msg)

           except CvBridgeError, e:
               print(e)
           else:
               filename = '/' + str(msg.header.seq) + '_' + str(msg.header.stamp) + '_' + topic.split('/')[1].replace('_', '-') + '.jpg'
               cv2.imwrite(sys.argv[1] + filename, img)
               with open(sys.argv[1]+'/metadata.csv','ab') as f:
                   thewriter = csv.writer(f)
                   thewriter.writerow([str(msg.header.seq),str(msg.header.stamp),os.getcwd()+'/'+sys.argv[1]+'/', filename])
        counter += 1
   bag.close()

if __name__ == "__main__":
   main()
