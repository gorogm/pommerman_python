from . import BaseAgent
from .. import characters
from ..constants import *
from os import path
import numpy as np
import ctypes
import time
import sys

class GottingenAgent(BaseAgent):
    """Parent abstract Agent."""
    turn_times = []

    def __init__(self, character=characters.Bomber):
        self._character = character
        self.avg_simsteps_per_turns = []

    def __getattr__(self, attr):
        return getattr(self._character, attr)

    def act(self, obs, action_space):
        #for attr in ['alive', 'board', 'bomb_life', 'bomb_blast_strength', 'position', 'blast_strength', 'can_kick', 'teammate', 'ammo', 'enemies']:
        #for attr in ['game_type', 'flame_life', 'bomb_moving_direction', 'step_count', 'game_env']:
        #in radio: message
        #    print(attr, type(obs[attr]), obs[attr])
        #    if 'numpy' in str(type(obs[attr])):
        #        print(' ', obs[attr].dtype)

        
        #print(obs['enemies'][0].__dict__) is sent to cpp, because only contains enum ids?
        #print(obs['position'][0])
        #print(type(obs['position'][0]))
        start_time = time.time()

        if isinstance(obs['bomb_moving_direction'], list):
            obs['bomb_moving_direction'] = np.asarray(obs['bomb_moving_direction'], dtype=np.float32)
        if isinstance(obs['flame_life'], list):
            obs['flame_life'] = np.asarray(obs['flame_life'], dtype=np.float32)


        decision = self.c.c_getStep_gottingen(
            self.id,
            Item.Agent0.value in obs['alive'], Item.Agent1.value in obs['alive'], Item.Agent2.value in obs['alive'], Item.Agent3.value in obs['alive'],
            obs['board'].ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
            obs['bomb_life'].ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            obs['bomb_blast_strength'].ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            obs['bomb_moving_direction'].ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            obs['flame_life'].ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            int(obs['position'][0]), int(obs['position'][1]),
            obs['blast_strength'],
            obs['can_kick'],
            obs['ammo'],
            obs['game_type'],
            obs['teammate'].value,
            obs['message'][0] if 'message' in obs else -1,
            obs['message'][1] if 'message' in obs else -1
            )
        self.turn_times.append(time.time() - start_time)

        if GameType(obs['game_type']) == GameType.TeamRadio:
            return [decision, self.c.c_getMessage_gottingen(self.id, 0), self.c.c_getMessage_gottingen(self.id, 1)]
        else:
            return decision
        

    def episode_end(self, reward):
        """This is called at the end of the episode to let the agent know that
        the episode has ended and what is the reward.

        Args:
          reward: The single reward scalar to this agent.
        """
        self.c.c_episode_end_gottingen.restype = ctypes.c_float
        avg_simsteps_per_turn = self.c.c_episode_end_gottingen(self.id)
        self.avg_simsteps_per_turns.append(avg_simsteps_per_turn)

    def init_agent(self, id, game_type):
        self.id = id
        self._character = self._character(id, game_type)
        self.c = None

        if sys.platform == "win32":
            self.c = ctypes.cdll.LoadLibrary("build/Release/pommerman.dll")
        else:
            possible_paths = ["/opt/work/pommerman_cpp/cmake-build-debug/", "../cmake-build-debug/", "./cmake-build-debug/"]
            for p in possible_paths:
                if path.exists(p + "/libpommerman.so"):
                    self.c = ctypes.cdll.LoadLibrary(p + "/libpommerman.so")
                    break
            if not self.c:
                print("Pommerman C++ library not found")

        self.c.c_init_agent_gottingen(id)

    @staticmethod
    def has_user_input():
        return False

    def shutdown(self):
        turn_times_np = np.array(self.turn_times)
        print("gottingen shutdown, avg simsteps per turns: ", np.round(np.array(self.avg_simsteps_per_turns).mean())/1000.0, " k",
              ", avg time: ", np.round(turn_times_np.mean()*1000, 1), " ms",
              ", max time: ", np.round(turn_times_np.max()*1000, 1), " ms",
              ", overtime: ", np.round((turn_times_np > 0.149).sum() / turn_times_np.shape[0] *100, 1), ' %')
