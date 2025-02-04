import random
import pandas as pd
import matplotlib.pyplot as plt

# This is a simple demonstration of performing simulations based on random events.
# This program makes a simple model of how match results are affected by weighted random events.

data={}
frame = {"season":[],
         "pcd_rate" :[],
         "average_pts" :[],
         "szn_perf" :[]}


# Simple 50/50 win lose choice.
def match(games, win_rate=0.5):
    reward = [0, 1]
    weights = [0.5, 0.5]
    outcome = random.choices(reward, weights=weights, k=games)
    return outcome

# Pick result based on weighted choice. Only two choices are available, win or lose.
def weighted_match(games, win_rate=0.5):
    reward=[0,1]
    weights=[1-win_rate,win_rate]
    outcome = random.choices(reward, weights=weights, k=games)
    return outcome

# Simulate matches over a given number of games per season.
def season(matches=40, final = 0):
    # Run simulation for n number of games in a season.
    matches = 40
    scores = weighted_match(matches, 0.72)

    final = sum(scores)

    return final

# Simulate 100 seasons played.Generate data to be used to plot charts.
def leagues(seasons=100, threshold=20):

    for league in range(seasons):
        points = season()
        data['season_' +str(league)] = points

    threshold = 0.75 * 40
    seasons_list = list(data.values())
    proceed_rate = sum(1 for x in seasons_list if x > threshold)
    point_avg = sum(seasons_list)/len(seasons_list)

    return data, seasons_list, proceed_rate, point_avg

# Make multiple simulations of above matches.
def simulations(depth=1024):
    for e in range(depth):
        sim, szn_lst, proceed, avg_pts=leagues()
        frame["season"].append(e)
        frame["pcd_rate"].append(proceed)
        frame["average_pts"].append(avg_pts)
        frame["szn_perf"].append(szn_lst)

    return frame

# Plot outcomes based on simulated data.
def visualize(dt):
    df = pd.DataFrame(dt)
    overall_pcd = sum(dt["pcd_rate"]) / len(dt["pcd_rate"])
    overall_pts = sum(dt["average_pts"]) / len(dt["average_pts"])
    print("Overall points average is: " +str(overall_pts))
    print("Overall proceed rate average is: " + str(overall_pcd) + " %")
    print(df)

    fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(12, 6))

    # Bar graph (left y-axis)
    ax1.bar(df['season'], df['average_pts'], color='skyblue', label='Point average')
    ax1.set_xlabel('Season')
    ax1.set_ylabel('Average points', color='blue')

    # Line graph (right y-axis)
    ax2 = ax1.twinx()
    ax2.plot(df['season'], df['pcd_rate'], marker=None, linestyle='-', color='red', label='Proceed rate trend')
    ax2.set_ylabel('Proceed rate trend', color='red')

    # Title and legend
    plt.title('Team performance development')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Plot separate bar graph on the second subplot
    ax3.bar(df['season'], df['pcd_rate'], color='lightgreen')
    ax3.set_title('Proceed rate per season')
    ax3.set_xlabel('Season')
    ax3.set_ylabel('Proceed rate')

    # Adjust layout to prevent overlap
    plt.tight_layout()

    plt.show()

def main():
   info = simulations()
   visualize(info)

# Run main endpoint.
if __name__ == '__main__':
    main()

