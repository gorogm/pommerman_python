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
        agents.CologneAgent(),
        agents.SimpleAgent(),
        agents.CologneAgent(),
        # agents.DockerAgent("pommerman/simple-agent", port=12345),
    ]
    # Make the "Free-For-All" environment using the agent list
    env = pommerman.make('PommeTeamCompetitionFast-v0', agent_list)

    wins = 0
    ties = 0
    nof_plays = 100
    # Run the episodes just like OpenAI Gym
    for i_episode in range(nof_plays):
        print("Game " + str(i_episode))
        state = env.reset(i_episode)
        #if i_episode != 20:
        #    continue
        done = False
        while not done:
            #env.render()
            actions = env.act(state)
            state, reward, done, info = env.step(actions)
        print(info)
        if info['result'] == pommerman.constants.Result.Tie:
            ties += 1
        elif info['winners'] == [1, 3]:
            wins += 1
        else:
            print(info['result'])
            print(info['winners'])
            print("Lost with seed: " + str(i_episode))
        print('Episode {} finished'.format(i_episode))
    env.close()
    print("wins: " + str(wins) + "/" + str(nof_plays - ties) + " = " + (wins / (nof_plays - ties)))


if __name__ == '__main__':
    print(os.getpid())
    import time
    #time.sleep(10)
    main()
