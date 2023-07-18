# MIT License
#
# Copyright (c) 2019 Peixin Chang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import os
import numpy as np
import sys
import pybullet as p
import time
from turtlebot.env_bases import BaseEnv
from turtlebot.robot_locomotors import TurtlebotC
from turtlebot.scene_abstract import SingleRobotEmptyScene




class TurtlebotEnv(BaseEnv):

    def __init__(self):
        """
        Put all your settings here
        """
        # START OF ROBOT CONFIGURATIONS
        dim = {
            'img_dim': (96, 96, 3), #(image_height,image_width,channel)
            'action_dim': 2,
            'motor_dim': 11,
        }

        obsSelect = {  # change these two flags to output desired kind of observations
            'motor': True,
            'img': True,
        }

        config = {
            # robot_bases.py will use the name indicated by robotName as the robot body
            # the robot body represents the whole robot, which is usually the base of a mobile robot
            'robotName': 'base_link',
            # if render is True, we will step simulation according to wall-clock time. Otherwise, simulation will run
            # as fast as possible
            'render':False,
            'frameSkip':12,
            # the max number of actions (decisions) for an episode. Time horizon N.
            'maxSteps': 100,
            'scale': 1,
            'modelFile': '/turtlebot/assets/turtlebot/turtlebot3_waffle_pi.urdf',
            'objList':['cube'],
            'objectsRadius': {'cube':0.1},
            
            'debugCam_dist':1.8,
            'debugCam_yaw': -90,
            'debugCam_pitch': -65,
            'control':'rotPos', #velocity, rotPos

            # Turtlebot3 max transitional velocity=0.26 m/s and max rotational velocity=1.82 rad/s (104.27 deg/s)
            'maxTransVel':0.25,
            'minTransVel': -0.1,
            'maxRotVel': 1.57, # in radian
            'robotWheelDistance':0.287, # the distance between two wheels
            'robotWheelRadius':0.033, # the radius of the wheels
            'renderSize': (75,100,3), #simulation render (height, width, channel)
            'rotPosPGain':1,
            'wheelAngle':720,

        }
       

        self.config=config
        self.robot = TurtlebotC(dim=dim,obsSelect=obsSelect, config=config)
        # START OF ENV CONFIGURATIONS
        BaseEnv.__init__(self, self.robot,config=config)

        
        self.timeStep = 1. / 240.
        self.maxSteps = config['maxSteps']
        self.episodeReward = 0.0


    def create_single_player_scene(self, bullet_client):
        """
        Setup physics engine and simulation
        :param bullet_client:
        :return: a scene
        """
        
        return SingleRobotEmptyScene(bullet_client, gravity=(0, 0, -9.8),
                                     timestep=self.timeStep, frame_skip=self.config['frameSkip'],
                                     render=self.config['render'])

    def prepareObservations(self, s):
        d = {}
        if self.robot.motor:
            d['motor'] = s['motor']
        

        if self.robot.img:  # if we want images
            
            img=self.robot.get_image()


            d['img'] = img/255. # the env has to convert the image to range from 0 to 1

        

        if not d:
            raise ValueError("You need to output observations")

        return d

    def step(self, action):
        action=np.array(action)
        act=[]
        
        if self.config['control']=='velocity':
            # action[0] transitional  velocity, action[1] rotational velocity
            deltaTrans = 0.05
            dTrans = float(np.clip(action[0], -1, +1)) * deltaTrans # delta transitional velocity

            deltaRot = 0.3
            dRot = float(np.clip(action[1], -1, +1)) * deltaRot  # delta rotational velocity
            act=[dTrans,dRot]
        elif self.config['control']=='rotPos':
            # action[0] transitional  velocity, action[1] rotational position
            deltaTrans = 0.05
            dTrans = float(np.clip(action[0], -1, +1)) * deltaTrans  # delta transitional velocity

            deltaRot = 0.25
            dRot = float(np.clip(action[1], -1, +1)) * deltaRot  # delta rotational position
            act = [dTrans, dRot]


        self.robot.apply_action(act)
        self.scene.global_step()
        self.envStepCounter = self.envStepCounter + 1

        state = self.robot.calc_state()  
        s_plus = self.prepareObservations(state) 

        r = self.rewards(state)
        
        self.reward = sum(r)
        self.episodeReward = self.episodeReward + self.reward

        
        self.done = self.termination(state)



        infoDict={}
        return s_plus, self.reward, self.done, infoDict 

    def rewards(self,s):
        transVel=s['motor'][0]
        rotVel=s['motor'][1]
        rewards = [int(np.random.randint(0,9,(1,))),0,0,0]
        return rewards

    def termination(self,state):

        if self.envStepCounter >= self.maxSteps:
           

           
            print("Epsiode Reward:", self.episodeReward)
            self.episodeReward=0
            return True


        return False






