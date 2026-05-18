#! /usr/bin/env python
import rospy

import actionlib

# import your custom messages

class YourClass(object):
    
  # create messages that are used to publish feedback/result
  _feedback = YourMessageFeedback()
  _result   = YourMessageResult()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("your_server_name", YourMessageAction, self.goal_callback, False)
    self._as.start()
    
  def goal_callback(self, goal):
    # this callback is called when the action server is called
    
    # your code here

    
    self._as.set_succeeded(self._result)
      
if __name__ == '__main__':
  rospy.init_node('your_node_name')
  YourClass()
  rospy.spin()
