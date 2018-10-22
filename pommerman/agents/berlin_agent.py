from . import BaseAgent
from .. import characters
from ..constants import *
import ctypes

class BerlinAgent(BaseAgent):
    """Parent abstract Agent."""

    def __init__(self, character=characters.Bomber):
        self._character = character

    def __getattr__(self, attr):
        return getattr(self._character, attr)

    def act(self, obs, action_space):

        #for attr in ['alive', 'board', 'bomb_life', 'bomb_blast_strength', 'position', 'blast_strength', 'can_kick', 'teammate', 'ammo', 'enemies']:
        #    print(attr, type(obs[attr]), obs[attr])
        #    if 'numpy' in str(type(obs[attr])):
        #        print(' ', obs[attr].dtype)

        
        #print(obs['enemies'][0].__dict__) is sent to cpp, because only contains enum ids?
        #print(obs['position'][0])
        #print(type(obs['position'][0]))
        return self.c.c_getStep(
            self.id,
            Item.Agent1 in obs['alive'], Item.Agent2 in obs['alive'], Item.Agent3 in obs['alive'],
            obs['board'].ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), 
            obs['bomb_life'].ctypes.data_as(ctypes.POINTER(ctypes.c_double)), 
            obs['bomb_blast_strength'].ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            int(obs['position'][0]), int(obs['position'][1]),
            obs['blast_strength'],
            obs['can_kick'],
            obs['ammo'],
            obs['teammate'].value
            )
        

    def episode_end(self, reward):
        """This is called at the end of the episode to let the agent know that
        the episode has ended and what is the reward.

        Args:
          reward: The single reward scalar to this agent.
        """
        self.c.c_episode_end(self.id)

    def init_agent(self, id, game_type):
        self.id = id
        self._character = self._character(id, game_type)
        #self.c = ctypes.cdll.LoadLibrary("/home/gorogm/nips2018-agent/build_cmake/libmunchen.so")
        self.c = ctypes.cdll.LoadLibrary("/home/AD.ADASWORKS.COM/marton.gorog/Desktop/nips2018-agent/cmake-build-debug/libmunchen.so")
        self.c.c_init_agent(id)

    @staticmethod
    def has_user_input():
        return False

    def shutdown(self):
        pass
