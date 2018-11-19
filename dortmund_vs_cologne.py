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
        agents.CologneAgent(),
        agents.DortmundAgent(),
        agents.CologneAgent(),
        agents.DortmundAgent(),
        # agents.DockerAgent("pommerman/simple-agent", port=12345),
    ]
    # Make the "Free-For-All" environment using the agent list
    env = pommerman.make('PommeTeamCompetitionFast-v0', agent_list)

    wins = 0
    ties = 0
    survived_agents = []
    nof_plays = 100
    # Run the episodes just like OpenAI Gym
    for i_episode in range(nof_plays):
        print("Game " + str(i_episode))
        state = env.reset(i_episode)
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
        survived_agents.extend(state[0]['alive'])
    env.close()

    survived_team_0 = survived_agents.count(10) + survived_agents.count(12)
    survived_team_1 = survived_agents.count(11) + survived_agents.count(13)
    kills = nof_plays * 2 - survived_team_0
    death = nof_plays * 2 - survived_team_1
    print("kills / death / ratio: ",  kills, " / ", death, " / ", kills/max(0.1, death))
    winRatio = str(wins / max(1, (nof_plays - ties)))
    print("wins: " + str(wins) + "/" + str(nof_plays - ties) + " = " + winRatio)

    file = open("/tmp/hypertune_result_winrate.txt", "w")
    file.write(winRatio)
    file.close()
    file = open("/tmp/hypertune_result_killdeath_diff.txt", "w")
    file.write(str(kills - death))
    file.close()


if __name__ == '__main__':
    print(os.getpid())
    import time
    #time.sleep(10)
    main()
