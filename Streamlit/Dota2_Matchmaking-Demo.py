import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import plotly.graph_objs as go
import random
import ast
import time
from deap import base, creator, tools, algorithms

# Set params for matplotlib
rcParams['font.family'] = 'Arial Unicode MS'

# Initialize player pool
player_pool = pd.read_csv('player_pool.csv')

# Convert string representations of lists to actual lists
player_pool['preferred_positions'] = player_pool['preferred_positions'].apply(ast.literal_eval)

# Select unique regions
regions = player_pool['cluster'].unique().tolist()

# Define servers per region
region_names = {
    'AUSTRALIA': [171, 172],
    'AUSTRIA': [192, 193, 191],
    'BRAZIL': [201, 202, 204],
    'CHILE': [241, 242],
    'DUBAI': [161],
    'EUROPE': [131, 132, 133, 134, 135, 136, 137, 138],
    'INDIA': [261],
    'JAPAN': [144, 145],
    'PERU': [251],
    'PW TELECOM GUANGDONG': [225],
    'PW TELECOM SHANGHAI': [224],
    'PW TELECOM WUHAN': [227],
    'PW TELECOM ZHEJIANG': [223],
    'PW UNICOM': [231],
    'PW UNICOM TIANJIN': [232],
    'SINGAPORE': [151, 152, 153, 154, 155, 156],
    'SOUTHAFRICA': [211, 212, 213],
    'STOCKHOLM': [181, 182, 183, 184, 185, 186, 187, 188],
    'US EAST': [121, 122, 123, 124],
    'US WEST': [112, 113, 111],
}

# Define position roles
positions = {
    1: 'Carry',
    2: 'Midlaner',
    3: 'Offlaner',
    4: 'Roamer',
    5: 'Support'
}


# Define the fitness function
creator.create('FitnessMax', base.Fitness, weights=(1.0,))

# Create Individual
class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = creator.FitnessMax()

creator.create('Individual', Individual, fitness=creator.FitnessMax)

# Initialize the toolbox
toolbox = base.Toolbox()

# Function to get players by region (stub, needs actual implementation)
def get_players_by_region(region):
    return player_pool[player_pool['cluster'] == region].index.tolist()


# Initial Population
def create_match(region):
    available_players = get_players_by_region(region)
    
    if len(available_players) < 10:
        return None  # Not enough players in this region
    
    match = []
    selected_players = set()

    def select_player_for_position(position, selected_players):
        # Find players who prefer this position as their first choice
        first_choice_candidates = [
            p for p in available_players 
            if p not in selected_players and player_pool.loc[p, 'preferred_positions'][0] == position
        ]
        if first_choice_candidates:
            return random.choice(first_choice_candidates)
        
        # If no first choice, find players who prefer this position as any choice
        other_candidates = [
            p for p in available_players 
            if p not in selected_players and position in player_pool.loc[p, 'preferred_positions']
        ]
        if other_candidates:
            return random.choice(other_candidates)
        
        return None
    
    for position in range(1, 6):  # Positions 1 to 5
        # Select players for Radiant
        radiant_player = select_player_for_position(position, selected_players)
        if radiant_player is None:
            return None  # Not enough players for this position
        match.append(radiant_player)
        selected_players.add(radiant_player)
        
        # Select players for Dire
        dire_player = select_player_for_position(position, selected_players)
        if dire_player is None:
            return None  # Not enough players for this position
        match.append(dire_player)
        selected_players.add(dire_player)
    
    return match

def create_valid_match():
    while True:
        if selected_server > 0:
            region = selected_server
        else:
            region = random.choice(regions)
        match = create_match(region)
        if match is not None:
            return Individual(match)

toolbox.register('individual', tools.initIterate, creator.Individual, create_valid_match)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)


# Fitness function
def evaluate_match(individual):
    if individual is None or len(individual) != 10:
        return (-float('inf'),)  # Extremely low fitness for invalid matches
    
    # Check for duplicate players
    if len(set(individual)) != 10:
        return (-float('inf'),)  # Extremely low fitness for matches with duplicate players
    
    radiant = individual[:5]
    dire = individual[5:]
    
    # Check if all players are from the same region
    regions = set(player_pool.loc[p, 'cluster'] for p in individual)
    if len(regions) > 1:
        return (-float('inf'),)  # Extremely low fitness for mixed regions
    
    # Calculate team skill difference
    radiant_skill = sum(player_pool.loc[p, 'skill_score'] for p in radiant)
    dire_skill = sum(player_pool.loc[p, 'skill_score'] for p in dire)
    team_skill_diff = abs(radiant_skill - dire_skill)

    # Calculate skill difference between same position
    position_skill_diff = sum(abs(player_pool.loc[r, 'skill_score'] - player_pool.loc[d, 'skill_score']) for r, d in zip(radiant, dire))
    
    # Check if players are in their preferred positions
    position_mismatch = 0
    first_position_mismatch = 0
    for i, p in enumerate(individual):
        preferred = player_pool.loc[p, 'preferred_positions']
        position = (i % 5) + 1
        if position != preferred[0]:
            first_position_mismatch += 1  # Heavier penalty for not being in the first preferred position
        if position not in preferred:
            position_mismatch += 1  # Penalty for not being in any preferred position
    
    # Combine factors (higher is better)
    fitness = 1 / (1 + team_skill_diff + (position_skill_diff*0.5) + (first_position_mismatch*20) + (position_mismatch*10))  # Heavy penalty for first position mismatches
    return (fitness,)

toolbox.register('evaluate', evaluate_match)


# Update the genetic operators to maintain unique players
def custom_mutation(individual, indpb):
    size = len(individual)
    for i in range(size):
        if random.random() < indpb:
            swap_idx = random.randint(0, size - 1)
            individual[i], individual[swap_idx] = individual[swap_idx], individual[i]
    individual.fitness.values = evaluate_match(individual)
    return individual,

def custom_crossover(ind1, ind2):
    size = len(ind1)
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]
    
    # Ensure uniqueness after crossover
    ind1 = Individual(dict.fromkeys(ind1))
    ind2 = Individual(dict.fromkeys(ind2))
    
    # Fill in any missing players
    available_players = set(player_pool.index) - set(ind1)
    while len(ind1) < size:
        ind1.append(random.choice(list(available_players)))
        available_players.remove(ind1[-1])
    
    available_players = set(player_pool.index) - set(ind2)
    while len(ind2) < size:
        ind2.append(random.choice(list(available_players)))
        available_players.remove(ind2[-1])
    
    ind1.fitness.values = evaluate_match(ind1)
    ind2.fitness.values = evaluate_match(ind2)
    return ind1, ind2

toolbox.register('mate', custom_crossover)
toolbox.register('mutate', custom_mutation, indpb=0.05)
toolbox.register('select', tools.selTournament, tournsize=3)


# Run genetic algorithm
def run_genetic_algorithm(population_size=1000, generations=60):
    pop = toolbox.population(n=population_size)
    pop = [ind for ind in pop if ind is not None and len(ind) == 10]  # Remove None or invalid individuals
    
    if not pop:
        raise ValueError('Could not create any valid matches. Try increasing the population size or check player data.')
    
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register('avg', np.mean)
    stats.register('min', np.min)
    stats.register('max', np.max)
    
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.35, 
                                       ngen=generations, stats=stats, 
                                       halloffame=hof, verbose=True)
    
    return pop, logbook, hof


# Visualize the results
def plot_evolution(logbook):
    gen = logbook.select('gen')
    fit_mins = logbook.select('min')
    fit_avgs = logbook.select('avg')
    fit_maxs = logbook.select('max')

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=gen, y=fit_mins, mode='lines', name='Minimum Fitness', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=gen, y=fit_avgs, mode='lines', name='Average Fitness', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=gen, y=fit_maxs, mode='lines', name='Maximum Fitness', line=dict(color='green')))

    fig.update_layout(
        title='Evolution of Fitness Over Generations',
        xaxis_title='Generation',
        yaxis_title='Fitness',
        legend_title='Fitness Type',
        template='plotly_white'
    )

    st.plotly_chart(fig)


# Function to plot radar charts in a 2x5 grid
def plot_radar_charts(player_data_list, party, party_team):
    num_players = len(player_data_list)
    num_vars = len(player_data_list[0][1])
    player_info = len(player_data_list[0][2])

    # Define chart colors by team
    for idx, (team, player_data, player_info) in enumerate(player_data_list):
        player_info['Color'] = player_info.get('Color', 'blue' if team == 'Radiant' else 'red')

    # Replace account names based on party selected positions
    for idx, user in enumerate(party):
        if party_team == 'Radiant':
            player_data_list[user['position'][0]-1][2]['Account'] = user['account']
            player_data_list[user['position'][0]-1][2]['Color'] = 'orange'
        else:
            player_data_list[user['position'][0]+4][2]['Account'] = user['account']
            player_data_list[user['position'][0]+4][2]['Color'] = 'orange'
    
    fig, axs = plt.subplots(2, 5, subplot_kw=dict(polar=True), figsize=(20, 13))

    for idx, (team, player_data, player_info) in enumerate(player_data_list):
        row, col = divmod(idx, 5)
        ax = axs[row, col]

        categories = list(player_data.keys())
        values = list(player_data.values())
        
        # Compute angle for each category and concatenate the first angle for closing the circle
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        # Plot radar charts
        ax.fill(angles, values, color=player_info['Color'], alpha=0.25)
        ax.plot(angles, values, color=player_info['Color'], linewidth=2)

        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)

        for angle, label in zip(angles, ax.get_xticklabels()):
            label.set_rotation(np.degrees(angle) - 90)
            label.set_verticalalignment('bottom')

        position_assigned = player_info['Player'] -5 if player_info['Player'] > 5 else player_info['Player']
        
        ax.set_title(
            f"\nPlayer {idx + 1}: {player_info['Account']}\n"\
            f"\nSkill Level: {player_info['Skill']:.4f}\n"\
            f"\nTotal Matches Played: {player_info['Total Matches']}\n"\
            f"\nPosition {position_assigned}: {positions[position_assigned]}\n"
        )
        
    # Add grey divider line between the first and second row of charts
    fig.subplots_adjust(hspace=0.4)
    fig.canvas.draw()
    height = fig.bbox.height / fig.dpi  # Get the height of the figure in inches
    y = (axs[0, 0].get_position().y0 + axs[1, 0].get_position().y1) / 2  # Calculate the middle point between the first and second row
    y_coord = y * height  # Convert the relative y-coordinate to absolute

    fig.add_artist(plt.Line2D([0, 1], [y_coord / height, y_coord / height], color='grey', linewidth=2, transform=fig.transFigure))

    # Add team names as y-axis labels for each row
    fig.text(0.00, (axs[0, 0].get_position().y0 + axs[0, 0].get_position().y1) / 2, 'Radiant', va='center', ha='center', rotation='vertical', fontsize=20, color='blue')
    fig.text(0.00, (axs[1, 0].get_position().y0 + axs[1, 0].get_position().y1) / 2, 'Dire', va='center', ha='center', rotation='vertical', fontsize=20, color='red')
    
    fig.tight_layout()
    st.pyplot(fig)

#------------------------#
# Streamlit app
st.set_page_config(
    page_title='Dota 2 Matchmaking Demo',
    page_icon='https://seeklogo.com/images/D/dota-2-logo-A8CAC9B4C9-seeklogo.com.png',
    layout='wide'
)

st.image('https://dslv9ilpbe7p1.cloudfront.net/ldkIN5uRK_TV5pz81ITh0Q_store_header_image')
st.header('About the Game')
st.write("Dota 2 is a popular free-to-play MOBA developed by Valve. Two teams of five players battle to destroy the other team's `Ancient` located in their base using powerful heroes with unique abilities.")
st.video('https://www.youtube.com/watch?v=M5NPN6E_Mro', start_time='1m31s', end_time='2m18s', loop=True, autoplay=True, muted=True)

# Player Database
st.header('Player Database')
display_df = player_pool.drop(columns=[
    'account_id',
    'kda_normalized', 
    'gold_per_min_normalized',
    'xp_per_min_normalized', 
    'cs_per_min_normalized', 
    'hero_damage_normalized', 
    'hero_healing_normalized', 
    'tower_damage_normalized', 
    'win_rate_normalized'
    ]).rename(columns={'cluster': 'server_id'}).set_index('account').head(10000)
st.dataframe(display_df)

# Genetic algorithm parameters
st.sidebar.header('Genetic Algorithm Params')
total_population = st.sidebar.slider('Set the total matches to be generated in each generation:', min_value=100, max_value=1000, value=500, step=100)
num_generations = st.sidebar.slider('Set the number of generations to run:', min_value=30, max_value=100, value=50, step=10)

# User input
st.sidebar.header('User Input')
user_region = st.sidebar.selectbox('Select your region:', options=list(region_names.keys()))
user_possible_servers = region_names[user_region]
st.sidebar.write(f"Total players in region: {len(player_pool[player_pool['cluster'].isin(user_possible_servers)])}")
party_size = st.sidebar.number_input('Select your party size:', min_value=1, max_value=5, value=1, step=1)

party = []
selected_positions = []
for i in range(party_size):
    user = {}
    user['account'] = st.sidebar.text_input(f"Player {i+1} User Name:", '')

    available_positions = [pos for pos in positions.values() if pos not in selected_positions]
    user['role'] = st.sidebar.selectbox(f"Player {i+1} Preferred role:", options=available_positions, key=f"position_{i}")
    user['position'] = [k for k, v in positions.items() if v == user['role']]

    if user['role']:
        selected_positions.append(user['role'])

    party.append(user)

if st.sidebar.button('Find a Match'):
    print('--------------------------------\n')
    for i, user in enumerate(party):
        print(f"Player {i+1}:"\
         f"\n    Account: {user['account']}"\
         f"\n    Role selected: {user['role']}"\
         f"\n    Position assigned: {user['position'][0]}\n")
    print('--------------------------------\n')

    # Select a random server in the user's region
    server_ids = region_names[user_region]
    selected_server = random.choice(server_ids)
    print('\n--------------------------------')
    print(f"Selected server: {selected_server}")
    print('--------------------------------\n')

    # Start the timer
    start_time = time.time()
    print('--------------------------------')
    print(f"Start time: {start_time}")
    print('--------------------------------\n')

    # Run the genetic algorithm
    pop, logbook, hof = run_genetic_algorithm(population_size=total_population, generations=num_generations)

    # End the timer
    end_time = time.time() - start_time
    print('\n--------------------------------')
    print(f"Elapsed time: {end_time}")
    print('--------------------------------\n')

    # Display matchmaking optimization
    best_match = hof[0]
    st.subheader('Matchmaking Optimization')
    st.write(f"Best Match Fitness: **{(evaluate_match(best_match)[0])*100:.2f}%**")
    plot_evolution(logbook)

    # Display the match breakdown
    st.subheader('Match Found!')
    st.write(f"Elapsed time: *{end_time:.2f} seconds*")

    # Select a random team to assign users
    party_team = random.choice(['Radiant', 'Dire'])

    player_data_list = []
    for idx, player_id in enumerate(best_match):
        player_data = player_pool.loc[player_id]
        team = 'Radiant' if idx < 5 else 'Dire'

        player_info = {
            'Player': idx + 1,
            'Account': player_data['account'],
            'Account ID': player_data['account_id'],
            'Team': team,
            'Color': 'blue' if team == 'Radiant' else 'red',
            'Positions Played': player_data['preferred_positions'],
            'Skill': player_data['skill_score'],
            'Total Matches': player_data['total_matches'],
        }
            
        radar_data = {
            'KDA': player_data['kda_normalized'],
            'Gold/Min': player_data['gold_per_min_normalized'],
            'XP/Min': player_data['xp_per_min_normalized'],
            'CS/Min': player_data['cs_per_min_normalized'],
            'Tower Damage': player_data['tower_damage_normalized'],
            'Hero Damage': player_data['hero_damage_normalized'],
            'Hero Healing': player_data['hero_healing_normalized']
        }
            
        player_data_list.append((team, radar_data, player_info))

    plot_radar_charts(player_data_list, party, party_team)

    # Genetic Algorithms
    with st.expander('Learn more about **Genetic Algorithms**', icon='🧬'):
        st.header('Genetic Algorithms')
        st.write('Genetic algorithm (GA) is a metaheuristic inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms (EA). Genetic algorithms are commonly used to generate high-quality solutions to optimization and search problems by relying on biologically inspired operators such as mutation, crossover and selection.')
        st.image('https://www.researchgate.net/publication/311092690/figure/download/fig1/AS:434236386746379@1480541430592/Illustration-of-the-Genetic-Algorithm-In-the-first-iteration-the-Genetic-Algorithm.png?_sg=V5Q3TTXb6RhBcXtmvTBG_9JGuZN9k1SUwk5aodG0aRqbWcRhwogMiOhwh0FOxjzEY1IlXQK1mwA',
                 caption='Brief diagram explaining how genetic algotirhms work')
        st.write('#### Population')
        st.write('A population is a group of individuals or Chromosomes and each individual is a candidate solution to The problem.')
        st.write('#### Chromosome')
        st.write('A Chromosome is An individual that contains a set of parameters known as Genes.')
        st.write('#### Gene')
        st.write('A Chromosome Contains a list of Parameters , this parameters we call them genes.')
        st.write('#### Fitness Function')
        st.write('A fitness function is a particular type of objective function which takes as input a candidate solution and outputs the quality of this solution, therefore the fitness function makes it possible to evaluate the candidate solutions.')
        st.write('\n*Source: [Genetic Algorithm Explained](https://medium.com/@AnasBrital98/genetic-algorithm-explained-76dfbc5de85d)*')