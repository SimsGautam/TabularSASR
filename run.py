from domain import *
from old_agent import *
from SASR_agent import *
import copy
import visualize
import threading
import time

def train(num_episodes, domain, agent, goal_index):

    # print updates 10 times
    chunk_size = num_episodes/10
    print_mark = [chunk_size*i for i in range(11)]
    for episode in range(num_episodes):
        if episode in print_mark:
            print 'explored states: ' + str(agent.explored_SA_count)
            print "Training " + str(episode) + "/" + str(num_episodes) + " complete."
        total_reward = 0
        domain.reinitialize(goal_index)
        while True:
            state = domain.get_agent_state()
            dup_state = copy.copy(state)
            action = agent.choose_action(state)
            is_terminal = domain.step(action)
            new_state = domain.get_agent_state()
            if not is_terminal:
                # if the game has not ended, incur a cost of living reward
                reward = -0.1
                agent.SR_learn(dup_state, action, reward, new_state)
                total_reward += reward
            else:
                if domain.reached_goal():
                    # if the game ended and agent is at the goal
                    reward = 0
                else:
                    # if max_steps is reached and agent not at goal
                    reward = -0.1
                total_reward += reward
                new_state = domain.get_agent_state()
                agent.SR_learn(dup_state, action, reward, new_state)
                break


def test(num_episodes, domain, agent, display, goal_index):

    for episode in range(num_episodes):
        total_reward = 0
        domain.reinitialize(goal_index)
        while True:
            full_state = domain.get_full_state()
            full_dup_state = copy.copy(full_state)
            display.update_grid(full_dup_state)

            state = domain.get_agent_state()
            dup_state = copy.copy(state)

            time.sleep(0.5)
            action = agent.choose_action(state)
            state_tup = tuple(state)
            is_terminal = domain.step(action)
            new_state = domain.get_full_state()
            for action in domain.possible_actions:
                print action
                print agent.get_Q(state, action)
                # print agent.m_table[(tuple(state), action)]
            if not is_terminal:
                # if the game has not ended, incur a cost of living reward
                reward = -0.1
                total_reward += reward
            else:
                if domain.reached_goal():
                    # if the game ended and agent is at the goal
                    reward = 0
                else:
                    # if max_steps is reached and agent not at goal
                    reward = -0.1
                total_reward += reward
                break
            display.update_grid(new_state)
            time.sleep(0.5)
        print "Episode: " + str(episode) + ", Total Reward: " + str(total_reward)
        display.end_game()
    return True


if __name__ == '__main__':
    goal_index = 31
    domain = MovingGoalsWorld(goal_index = goal_index)
    # agent = OldAgent(domain.possible_actions)
    agent = SASRagent(domain.possible_actions, goal_index = goal_index)
    episodes_train = 150
    episodes_test = 1

    print '> STARTED LATENT LEARNING...'
    # training on default epsilon = 1 (pure exploration)
    train(50, domain, agent, goal_index)

    # seting the exploration rate to 0 (pure exploitation)
    agent.set_epilson(0.0)

    print '> STARTED TRAINING...'

    train(episodes_train, domain, agent, goal_index)

    while True:
        inp = raw_input('Enter test or quit: ')

        if inp == 'quit':
            break
        elif inp == 'test':
            display = visualize.VisualGame(domain.get_full_state())
            domain.reinitialize(goal_index)
            # state = domain.get_state()

            test_thread = threading.Thread(target = test, args = (episodes_test, domain, agent, display, goal_index))
            display_thread = threading.Thread(target = display.run)

            # so that we can exit from shell while thread is running
            test_thread.daemon = True
            display_thread.daemon = True

            test_thread.start()
            display_thread.start()
        else:
            continue


    