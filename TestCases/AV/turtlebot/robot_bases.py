import pybullet as p
import gym, gym.spaces, gym.utils
import numpy as np
import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)


class BaseRobot:
    """
    Base class for mujoco .xml/ROS urdf based agents.
    Handles object loading
    """
    def __init__(self, model_file, robot_name, dim, obsSelect, scale = 1):
        """
        :param model_file: the path to the robot model
        :param robot_name: the name of the robot
        :param dim: a dict containing dimension for each type of observations
        :param obsSelect: a dict containing booleans for indicating whether to generate certain type of observations
        :param scale: the scale of the robot model
        """
        self.parts = None # a dict containing each part of the robot in type 'BodyPart'
        self.jdict = None # a dict containing interested joint in type 'Joint' (e.g. revolute but not fixed joint)
        self.ordered_joints = None # a list containing interested joint in type 'Joint'
        self.robot_body = None # a 'BodyPart' representing the whole robot body. e.g. base link
        self.robot_ids = None # robot ID provided by Pybullet
        self.eyes = None # the camera of the robot

        self.motor = False
        self.img = False
       
        d = {}

        if 'motor' in obsSelect and obsSelect['motor']:
            self.motor = obsSelect['motor']
            self.motor_dim = dim['motor_dim']
            high = np.inf * np.ones([self.motor_dim])
            d['motor'] = gym.spaces.Box(-high, high,dtype=np.float32)
        if 'img' in obsSelect and obsSelect['img']:
            self.img = obsSelect['img']
            self.img_dim = dim['img_dim']
            d['img'] = gym.spaces.Box(low=-np.inf, high=np.inf, shape=self.img_dim, dtype=np.float32)

        high = np.ones([dim['action_dim']])
        self.action_space = gym.spaces.Box(-high, high,dtype=np.float32)

        self.observation_space = gym.spaces.Dict(d)

        if not d:
            raise ValueError("You need to output observations")


        self.model_file = model_file
        self.robot_name = robot_name
        self.scale = scale
        self.model_type=os.path.splitext(model_file)[1][1:] # get urdf or xml


    def addToScene(self, bodies):
        if self.parts is not None:
            parts = self.parts
        else:
            parts = {}

        if self.jdict is not None:
            joints = self.jdict
        else:
            joints = {}

        if self.ordered_joints is not None:
            ordered_joints = self.ordered_joints
        else:
            ordered_joints = []

        dump = 0

        for i in range(len(bodies)):
            if p.getNumJoints(bodies[i]) == 0:
                part_name, robot_name = p.getBodyInfo(bodies[i], 0)
                part_name = part_name.decode("utf8")
                parts[part_name] = BodyPart(part_name, bodies, i, -1, self.scale, model_type=self.model_type)

            for j in range(p.getNumJoints(bodies[i])):
                # let all joints be controlled such that the robot will not fall at the very beginning
                p.setJointMotorControl2(bodies[i],j,p.POSITION_CONTROL,positionGain=0.1,velocityGain=0.1,force=0)
                _,joint_name,joint_type, _,_,_, _,_,_,_, _,_, part_name, _,_,_,_ = p.getJointInfo(bodies[i], j)

                joint_name = joint_name.decode("utf8")
                part_name = part_name.decode("utf8")

                if dump: print("ROBOT PART '%s'" % part_name)
                if dump: print("ROBOT JOINT '%s'" % joint_name) # limits = %+0.2f..%+0.2f effort=%0.3f speed=%0.3f" % ((joint_name,) + j.limits()) )
                parts[part_name] = BodyPart(part_name, bodies, i, j, self.scale, model_type=self.model_type)

                if part_name == self.robot_name:
                    self.robot_body = parts[part_name]

                if i == 0 and j == 0 and self.robot_body is None:  # if nothing else works, we take this as robot_body
                    parts[self.robot_name] = BodyPart(self.robot_name, bodies, 0, -1, self.scale, model_type=self.model_type)
                    self.robot_body = parts[self.robot_name]

                if joint_name[:6] == "ignore":
                    Joint(joint_name, bodies, i, j, self.scale,self.model_type).disable_motor()
                    continue

                if joint_name[:8] != "jointfix" and joint_type != p.JOINT_FIXED: # revolute or prismatic joints
                    joints[joint_name] = Joint(joint_name, bodies, i, j, self.scale, model_type=self.model_type)
                    # ordered_joints[0]=left wheel joint,ordered_joints[1]=right wheel joint
                    ordered_joints.append(joints[joint_name])

                    joints[joint_name].power_coef = 100.0

        debugmode = 0
        if debugmode:
            for j in ordered_joints:
                print(j, j.power_coef)
        return parts, joints, ordered_joints, self.robot_body

    def load_model(self):
        print("LOADING MODEL")
        if self.model_type == "xml":
            self.robot_ids = p.loadMJCF(self.model_file, flags=p.URDF_USE_SELF_COLLISION+p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS)
        if self.model_type == "urdf":
            self.robot_ids = (p.loadURDF(self.model_file, globalScaling = self.scale))
        self.parts, self.jdict, self.ordered_joints, self.robot_body = self.addToScene([self.robot_ids])
        self.eyes = self.parts["eyes"]


class Pose_Helper:
    def __init__(self, body_part):
        self.body_part = body_part

    def xyz(self):
        return self.body_part.get_position()

    def rpy(self):
        return p.getEulerFromQuaternion(self.body_part.get_orientation())

    def orientation(self):
        return self.body_part.get_orientation()

class BodyPart:
    def __init__(self, body_name, bodies, bodyIndex, bodyPartIndex, scale, model_type):
        self.bodies = bodies
        self.body_name = body_name
        self.bodyIndex = bodyIndex
        self.bodyPartIndex = bodyPartIndex
        if model_type=="xml":
            self.scale = scale
        else:
            self.scale = 1
        self.initialPosition = self.get_position() / self.scale
        self.initialOrientation = self.get_orientation()
        self.bp_pose = Pose_Helper(self)

        
    def get_name(self):
        return self.body_name

    def _state_fields_of_pose_of(self, body_id, link_id=-1):
        """Calls native pybullet method for getting real (scaled) robot body pose
           
           Note that there is difference between xyz in real world scale and xyz
           in simulation. Thus you should never call pybullet methods directly
        """
        if link_id == -1:
            (x, y, z), (a, b, c, d) = p.getBasePositionAndOrientation(body_id)
        else:
            (x, y, z), (a, b, c, d), _, _, _, _ = p.getLinkState(body_id, link_id)
        x, y, z = x * self.scale, y * self.scale, z * self.scale
        return np.array([x, y, z, a, b, c, d])

    def _set_fields_of_pose_of(self, pos, orn):
        """Calls native pybullet method for setting real (scaled) robot body pose"""
        p.resetBasePositionAndOrientation(self.bodies[self.bodyIndex], np.array(pos) / self.scale, orn)

    def get_pose(self):
        return self._state_fields_of_pose_of(self.bodies[self.bodyIndex], self.bodyPartIndex)

    def get_position(self):
        """Get position of body part
           Position is defined in real world scale """
        return self.get_pose()[:3]

    def get_orientation(self):
        """Get orientation of body part
           Orientation is by default defined in [x,y,z,w]"""
        return self.get_pose()[3:]

    def set_position(self, position):
        """Get position of body part
           Position is defined in real world scale """
        self._set_fields_of_pose_of(position, self.get_orientation())

    def set_orientation(self, orientation):
        """Get position of body part
           Orientation is defined in [x,y,z,w]"""
        self._set_fields_of_pose_of(self.get_position(), orientation)

    def set_pose(self, position, orientation):
        self._set_fields_of_pose_of(position, orientation)

    def pose(self):
        return self.bp_pose

    def speed(self):
        if self.bodyPartIndex == -1:
            (vx, vy, vz), _ = p.getBaseVelocity(self.bodies[self.bodyIndex])
        else:
            (x,y,z), (a,b,c,d), _,_,_,_, (vx, vy, vz), (vr,vp,vyaw) = p.getLinkState(self.bodies[self.bodyIndex], self.bodyPartIndex, computeLinkVelocity=1)
        return np.array([vx, vy, vz])

    def angular_speed(self):
        if self.bodyPartIndex == -1:
            _, (vr,vp,vyaw) = p.getBaseVelocity(self.bodies[self.bodyIndex])
        else:
            (x,y,z), (a,b,c,d), _,_,_,_, (vx, vy, vz), (vr,vp,vyaw) = p.getLinkState(self.bodies[self.bodyIndex], self.bodyPartIndex, computeLinkVelocity=1)
        return np.array([vr, vp, vyaw])

    def contact_list(self):
        return p.getContactPoints(self.bodies[self.bodyIndex], -1, self.bodyPartIndex, -1)


class Joint:
    def __init__(self, joint_name, bodies, bodyIndex, jointIndex, scale, model_type):
        self.bodies = bodies
        self.bodyIndex = bodyIndex
        self.jointIndex = jointIndex
        self.joint_name = joint_name
        _,_,self.jointType,_,_,_,_,_,self.lowerLimit, self.upperLimit,_,_,_, _,_,_,_ = p.getJointInfo(self.bodies[self.bodyIndex], self.jointIndex)
        self.power_coeff = 0
        if model_type=="MJCF":
            self.scale = scale
        else:
            self.scale = 1
        if self.jointType == p.JOINT_PRISMATIC:
            self.upperLimit = self.upperLimit*self.scale
            self.lowerLimit = self.lowerLimit*self.scale

    def __str__(self):
        return "idx: {}, name: {}".format(self.jointIndex, self.joint_name)

    def get_state(self):
        """Get state of joint
           Position is defined in real world scale """
        x, vx,_,_ = p.getJointState(self.bodies[self.bodyIndex],self.jointIndex) # get position x and velocity vx
        if self.jointType == p.JOINT_PRISMATIC:
            x  = x*self.scale
            vx = vx*self.scale
        return x, vx

    def set_state(self, x, vx):
        """Set state of joint
           x is defined in real world scale """
        if self.jointType == p.JOINT_PRISMATIC:
            x  = x/self.scale
            vx = vx/self.scale
        p.resetJointState(self.bodies[self.bodyIndex], self.jointIndex, x, vx)

    def get_relative_state(self):
        pos, vel = self.get_state()
        pos_mid = 0.5 * (self.lowerLimit + self.upperLimit)
        return (
            2 * (pos - pos_mid) / (self.upperLimit - self.lowerLimit),
            0.1 * vel
        )

    def set_position(self, position):
        """Set position of joint
           Position is defined in real world scale """
        if self.jointType == p.JOINT_PRISMATIC:
            position = np.array(position) / self.scale
        p.setJointMotorControl2(self.bodies[self.bodyIndex],self.jointIndex,p.POSITION_CONTROL, targetPosition=position)

    def set_velocity(self, velocity):
        """Set velocity of joint
           Velocity is defined in real world scale """
        if self.jointType == p.JOINT_PRISMATIC:
            velocity = np.array(velocity) / self.scale
        p.setJointMotorControl2(self.bodies[self.bodyIndex],self.jointIndex,p.VELOCITY_CONTROL, targetVelocity=velocity) # , positionGain=0.1, velocityGain=0.1)

    def set_torque(self, torque):
        p.setJointMotorControl2(bodyIndex=self.bodies[self.bodyIndex], jointIndex=self.jointIndex, controlMode=p.TORQUE_CONTROL, force=torque) #, positionGain=0.1, velocityGain=0.1)

    def reset_state(self, pos, vel):
        self.set_state(pos, vel)

    def disable_motor(self):
        p.setJointMotorControl2(self.bodies[self.bodyIndex],self.jointIndex,controlMode=p.POSITION_CONTROL, targetPosition=0, targetVelocity=0, positionGain=0.1, velocityGain=0.1, force=0)

    def get_joint_relative_state(self): # Synonym method
        return self.get_relative_state()

    def get_joint_state(self):
        return self.get_state()

    def set_motor_position(self, pos):  # Synonym method
        return self.set_position(pos)

    def set_motor_torque(self, torque): # Synonym method
        return self.set_torque(torque)

    def set_motor_velocity(self, vel):  # Synonym method
        return self.set_velocity(vel)

    def reset_joint_state(self, position, velocity): # Synonym method
        return self.reset_state(position, velocity)

    def current_position(self):             # Backward compatibility
        return self.get_state()

    def current_relative_position(self):    # Backward compatibility
        return self.get_relative_state()

    def reset_current_position(self, position, velocity):   # Backward compatibility
        self.reset_state(position, velocity)

    def reset_position(self, position, velocity):  # Backward compatibility
        self.reset_state(position, velocity)
