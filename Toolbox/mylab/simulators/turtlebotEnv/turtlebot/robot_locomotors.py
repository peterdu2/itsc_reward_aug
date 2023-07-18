from mylab.simulators.turtlebotEnv.turtlebot.robot_bases import BaseRobot
import numpy as np
import pybullet as p
import os
#import cv2

import time

class Turtlebot(BaseRobot):
    """
    This class is the common properties and helper functions for Turtlebots.
    """

    def __init__(self, dim, obsSelect,config):

        BaseRobot.__init__(self, model_file=config['modelFile'], robot_name=config['robotName'],
                           dim=dim, obsSelect=obsSelect, scale = config['scale'])
        self.control = config['control']

        self.scale = config['scale']
        self._p=None
        # the altitude of all the objects including the robot, hard coded value. Every episode, the objects and the
        # robot will be reset to the position with this altitude
        self.entityZ=0.04
        self.envStepCounter=-1

        # the RL planner's decision will change these two vectors
        self.desiredTransVel = 0.
        self.desiredRotVel = 0.
        self.desiredRotPos=0

        self.np_random = None  # this will be automatically set by env_bases

    def get_pose(self):
        """Get current robot position and orientation in quaternion [x,y,z,w]
        """
        return self.robot_body.get_pose()

    def get_position(self):
        """Get current robot position
        """
        return self.robot_body.get_position()

    def get_orientation(self):
        """Get current robot orientation in quaternion [x,y,z,w]
        """
        return self.robot_body.get_orientation()

    def set_position(self, pos):
        """
        Set the position of the robot body according to 'pos'. The orientation will not be changed
        :param pos: the desired position of the robot body
        """
        self.robot_body.reset_position(pos)

    def set_orientation(self, orn):
        """
        Set the orientation of the robot body according to 'orn'. The position will not be changed
        :param orn: the desired orientation of the robot body in quaternion [x,y,z,w]
        """
        self.robot_body.set_orientation(orn)
    def set_pose(self,pos,orn):
        """
        Set the position and the orientation of the robot body.
        :param pos: the desired position of the robot body
        :param orn: the desired orientation of the robot body in quaternion [x,y,z,w]
        """
        self.robot_body.set_pose(pos,orn)

    def reset(self,bullet_client):  # BaseEnv.reset() will call this function
        if self.robot_ids is None: #if it is the first run, we store the bullet_client
            self._p=bullet_client
        self.robot_specific_reset()

        state= self.calc_state()



        return state

    def robot_specific_reset(self):
        raise NotImplementedError

    def apply_action(self, a):
        raise NotImplementedError

    def calc_state(self):
        raise NotImplementedError
    def calc_potential(self,s):
        raise NotImplementedError

    def _get_scaled_position(self):
        '''Private method, please don't use this method outside
        Used for downscaling MJCF models
        '''
        return self.robot_body.get_position() / self.scale


class TurtlebotC(Turtlebot):
    """
    This is a derived class for Turtlebot
    """
    def __init__(self,dim=None, obsSelect=None, config=None):
        Turtlebot.__init__(self, dim=dim, obsSelect=obsSelect, config=config)
        self.config=config
        
        self.obsSelect=obsSelect
        

        self.maxSteps = config['maxSteps']
       
        self.episodeCounter = 0

        # models
        self.arena_wall = None
        self.arena_floor = None
        self.objList=self.config['objList']
        self.objDict={}
        
        for  obj in self.objList:
            self.objDict[obj]=None # put Uid in it

        # each spot associates with a list [x,y,yaw]. The order will be same with self.objList
        # [[x,y,yaw],[x,y,yaw],...]
        self.objPoseList = []  # objects position and orientation information


        self.initialPose=[0,0,0]
        self.anglePassed = 0.
        


    def calc_potential(self,s):
        return 0



    def apply_action(self, action):
        
        if self.control=='velocity':
            # TODO: motor model
            # TODO: processing the action further. e.g. smoothing, add some noise

            # apply the action and clip.
            # action[0]=transitional velocity, action[1]=rotational velocity
            self.desiredTransVel=self.desiredTransVel+action[0]
            self.desiredTransVel = float(np.clip(self.desiredTransVel, self.config['minTransVel'], self.config['maxTransVel']))

            self.desiredRotVel=self.desiredRotVel+action[1]
            self.desiredRotVel = float(np.clip(self.desiredRotVel, -self.config['maxRotVel'], self.config['maxRotVel']))
        elif self.control=='rotPos':
            self.desiredTransVel = self.desiredTransVel + action[0]
            self.desiredTransVel = float(np.clip(self.desiredTransVel, self.config['minTransVel'], self.config['maxTransVel']))

            self.desiredRotPos=self.desiredRotPos+action[1]

            error=None
            if self.config['wheelAngle']==360:
                self.desiredRotPos = np.clip(self.desiredRotPos, -3.1, 3.1)
                error = self.desiredRotPos - self.anglePassed
            elif self.config['wheelAngle']==720:
                self.desiredRotPos = np.clip(self.desiredRotPos, -2*3.1, 2*3.1)
                if self.desiredRotPos >= 0:
                    l = [self.desiredRotPos - self.anglePassed, self.desiredRotPos - (self.anglePassed + 2 * np.pi)]
                else:
                    l = [self.desiredRotPos - self.anglePassed, self.desiredRotPos - (self.anglePassed - 2 * np.pi)]
                index = np.argmin([abs(l[0]), abs(l[1])])
                error = l[index]
            self.desiredRotVel = self.config['rotPosPGain']*error  # e.g. P control gain=1
            self.desiredRotVel = np.clip(self.desiredRotVel, -self.config['maxRotVel'], self.config['maxRotVel'])


            L = self.config['robotWheelDistance']
            R = self.config['robotWheelRadius']
            desiredRightWheelVel = (2. * self.desiredTransVel + self.desiredRotVel * L) / (2. * R)
            desiredLeftWheelVel = (2. * self.desiredTransVel - self.desiredRotVel * L) / (2. * R)
            realAction = [desiredLeftWheelVel, desiredRightWheelVel]  # the velocity command for the left motor and the right motor



            for n, j in enumerate(self.ordered_joints):
                j.set_motor_velocity(realAction[n])



    def loadObj(self,path,name):

        visualID = self._p.createVisualShape(shapeType=self._p.GEOM_MESH,
                                       fileName=path,
                                       visualFramePosition=[0, 0, 0],
                                       visualFrameOrientation=self._p.getQuaternionFromEuler([0, 0, 0]),
                                       rgbaColor=[1,1,1,1]
                                       )

        collisionID = self._p.createCollisionShape(shapeType=self._p.GEOM_CYLINDER,
                                             radius=self.config['objectsRadius'][name],
                                             height=0.5,
                                             collisionFramePosition=[0, 0, 0],
                                             collisionFrameOrientation=self._p.getQuaternionFromEuler([0, 0, 0]))

        objID=self._p.createMultiBody(baseMass=0,
                          baseInertialFramePosition=[0, 0, 0],
                          baseCollisionShapeIndex=collisionID,
                          baseVisualShapeIndex=visualID,
                          basePosition=[3,3,3],
                          baseOrientation=self._p.getQuaternionFromEuler([0, 0, 0]))
        return objID


    def robot_specific_reset(self):
        if self.robot_ids is None: # if it is the first run, load all models

            # MODEL FILES NEED TO BE IN SAME DIRECTORY AS WHERE SIM IS RUNNING
            # load arena
            self.arena_wall = self._p.loadURDF('/turtlebot/assets/arena/arena_wall.urdf',
                                               [0, 0, 0.0], [0., 0., 0.0, 1.0],
                                               flags=self._p.URDF_USE_MATERIAL_COLORS_FROM_MTL)

            self.arena_floor = self._p.loadURDF('/turtlebot/assets/arena/arena_floor.urdf',
                                                [0, 0, 0.03], [0., 0., 0.0, 1.0],
                                                flags=self._p.URDF_USE_MATERIAL_COLORS_FROM_MTL)
            # load objects and put them far away from the arena
            for item in self.objList:
                self.objDict[item] = self.loadObj("/turtlebot/assets/objects/"+item+".obj",item)


            # load robot so that robot_ids is not None
            self.load_model()
            self.eyes=self.parts["eyes"] # in the urdf, the link for the camera is called "eyes"

        # reset all flags and counters
        self.envStepCounter = -1
        self.desiredTransVel = 0.
        self.desiredRotVel = 0.
        self.desiredRotPos = 0.
        self.episodeCounter = self.episodeCounter + 1
        self.anglePassed = 0.
        self.objPoseList = []

        self.initialPose = [0, 0, 0]




        self.randomization()



    def randomXYYaw(self,rouLow, rouHigh,thetaLow,thetaHigh,yawLow,yawHigh):
        rou = self.np_random.uniform(low=rouLow, high=rouHigh)
        theta = self.np_random.uniform(low=thetaLow, high=thetaHigh)
        y = rou * np.sin(theta)
        x = rou * np.cos(theta)
        yaw = self.np_random.uniform(low=yawLow, high=yawHigh)
        return x,y,yaw

    def randomization(self):

        # robot
        robotx, roboty, robotYaw = self.randomXYYaw(rouLow=0, rouHigh=0.5, thetaLow=0,
                                                    thetaHigh=2 * np.pi, yawLow=-np.pi, yawHigh=np.pi)




        objx,objy,objYaw=self.randomXYYaw(rouLow=0.5, rouHigh=0.8,thetaLow=0,
                                        thetaHigh=2*np.pi,yawLow=-np.pi,yawHigh=np.pi)


        # robot
        for j in self.ordered_joints:
            j.reset_joint_state(self.np_random.uniform(low=-0.1, high=0.1), 0)
        self.set_pose([robotx,roboty, self.entityZ],self._p.getQuaternionFromEuler([0, 0, robotYaw]))
        self.initialPose=[robotx,roboty,robotYaw]


        # objects
        self._p.resetBasePositionAndOrientation(self.objDict[self.objList[0]], [objx, objy, self.entityZ],
                                                self._p.getQuaternionFromEuler([0, 0, objYaw]))
        self.objPoseList.append([objx, objy,objYaw])

        # for now let's change color
        self._p.changeVisualShape(self.objDict[self.objList[0]],linkIndex=-1,rgbaColor=list(self.np_random.rand(3,))+[1])


    def calc_state(self):
        self.envStepCounter = self.envStepCounter+1

        motorState = []



        # get robot body position and orientation
        body_pose = self.robot_body.pose()
        body_xyz = body_pose.xyz()
        body_rpy = body_pose.rpy()
        roll, pitch, yaw = body_rpy  # we only care about yaw angle


        j = np.array([j.get_joint_state() for j in self.ordered_joints], dtype=np.float32).flatten()

        vl=j[1]
        vr=j[3]
        # transform back to the real transitional and rotational velocity.
        transVel=(vr+vl)*self.config['robotWheelRadius']/2.
        rotVel=(vr-vl)*self.config['robotWheelRadius']/self.config['robotWheelDistance']

        motorState.extend([transVel,rotVel])

        self.anglePassed=yaw-self.initialPose[2]
        if self.anglePassed>np.pi:
            self.anglePassed=self.anglePassed-2*np.pi
        elif self.anglePassed<-np.pi:
            self.anglePassed=self.anglePassed+2*np.pi
        motorState.extend([body_xyz[0]-self.initialPose[0],body_xyz[1]-self.initialPose[1],self.anglePassed])

        distance = np.linalg.norm([body_xyz[0] - self.objPoseList[0][0], body_xyz[1] - self.objPoseList[0][1]])
        motorState.append(distance)

        motorState.extend([body_xyz[0],body_xyz[1],np.sin(yaw),np.cos(yaw)])

        s = {'motor': np.array(motorState)}


        return s

    def get_image(self):
        # cameraFrame=worldFrame*Rz(90)*Ry(0)*Rx(-90), rpy=(90,0,-90)
        eye_pos = self.eyes.get_position()
        body_euler = self._p.getMatrixFromQuaternion(self.robot_body.get_orientation())
        body_euler = np.reshape(body_euler, (3, 3))

        view_matrix = \
            self._p.computeViewMatrix(cameraEyePosition=eye_pos,
                                      cameraTargetPosition=eye_pos + 0.01 * np.matmul(body_euler,
                                                                                      np.array([1, 0, 0])),
                                      cameraUpVector=np.matmul(body_euler, np.array([0, 0, 1])))

        # Turtlebot camera resolution is 640*480. We keep the aspect ratio here. You need to do downsampling
        # to the images received by the camera first.
        proj_matrix = self._p.computeProjectionMatrixFOV(
            fov=62.2, aspect=4. / 3.,
            nearVal=0.01, farVal=100)

        (w, h, px, _, _) = self._p.getCameraImage(
            width=self.config['renderSize'][1], height=self.config['renderSize'][0], viewMatrix=view_matrix,
            projectionMatrix=proj_matrix, shadow=0, renderer=self._p.ER_TINY_RENDERER,
            flags=self._p.ER_NO_SEGMENTATION_MASK
        )
        rgb_array = np.array(px)
        # Tensorflow use (height,width,channel), and the image output here will be (height,width, channel) as well
        img = rgb_array[:, :, :3]

        # # process the image
        # if self.config['renderSize'][2] == 1:  # if we need grayscale image
        #     img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        #     img = np.reshape(img, [self.config['renderSize'][0], self.config['renderSize'][1], 1])

        # # crop and resize
        # img = img[:, 12:87, :]
        # img = cv2.resize(img, (self.img_dim[1], self.img_dim[0]))

        return img
