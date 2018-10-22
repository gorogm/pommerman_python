import pommerman
from pommerman import agents
import os

def main():
    '''Simple function to bootstrap a game.
       
       Use this as an example to set up your training env.
    '''
    # Print all possible environments in the Pommerman registry
    print(pommerman.REGISTRY)

    # Create a set of agents (exactly four)
    agent_list = [
        agents.SimpleAgent(),
        agents.BerlinAgent(),
        agents.SimpleAgent(),
        agents.SimpleAgent(),
        # agents.DockerAgent("pommerman/simple-agent", port=12345),
    ]
    # Make the "Free-For-All" environment using the agent list
    env = pommerman.make('PommeTeamCompetition-v0', agent_list)

    # Run the episodes just like OpenAI Gym
    for i_episode in range(1):
        state = env.reset(18)
        done = False
        while not done:
            env.render() #record_json_dir='/tmp/'
            actions = env.act(state)
            state, reward, done, info = env.step(actions)
        print(info)
        print('Episode {} finished'.format(i_episode))
    env.close()


if __name__ == '__main__':
    print(os.getpid())
    import time
    #time.sleep(10)
    main()
