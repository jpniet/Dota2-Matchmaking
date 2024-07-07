# Matchmaking in Online Multiplayer Games

## Project Overview

Matchmaking in online multiplayer video games is a significant and challenging topic, centred around a simple question: who should play together?

The question may seem simple, but the answer is quite complex. Several factors need to be considered, such as skill level, region, wait times, playing with pre-made groups, ensuring that players don’t end up in the same lobby repeatedly, and even implementing a system to match toxic players with each other while keeping them away from those who exhibit good behaviour.

In this project, we will explore the definitions of a good match and how to calculate and predict balance using machine learning architectures. Our aim is to improve the quality of online multiplayer games by focusing on player experience.

---

## Proposed Solution

Through analyzing data from multiple matches and utilizing various machine learning techniques such as unsupervised clustering, LSTMs, and sentiment analysis, we can construct player profiles. These profiles can then be used to group each player with the most suitable teammates and to pair them with challenging rivals to keep them engaged.

### Objectives
- Improve player engagement by enhancing matchmaking by accurately classifying players based on skill level, region, preferred position and heroes, and essential personality traits inferred from in-game activity.

### Hypotheses
- *Balancing matches based on player skill levels increases player retention.*
- *Players perform better when matched with compatible personalities, leading to increased engagement.*

### Potential Impact

Retaining users has become increasingly difficult as competition intensifies, particularly for startups and new F2P games, as seen in the case of [***Omega Strikers***](https://www.youtube.com/watch?v=6blfDQzmIoQ). Developing a successful profiling and matchmaking model that forecasts the best matchups can assist indie studios in iterating more effectively and keeping players engaged.

---

## Table of Contents
1. **Models**
	1. Runs
		1. [LSTMs](Models/LSTM/runs)
2. **Notebooks**
	1. [Data Cleaning and Exploration](Notebooks/Data_Cleaning_and_Exploration.ipynb)
	2. [Data Preprocessing](Notebooks/Data_Preprocessing.ipynb)
	3. [Finding Clusters in Match Data](Notebooks/Match_Clusters.ipynb)
	4. [Matches EDA and Initial Modelling](Notebooks/Matches_EDA_and_Initial_Modelling.ipynb)
	5. [LSTMs to Predict Match Balance](Notebooks/LSTM.ipynb)
	6. [Predicting Win Rates to Define Skill Level](Notebooks/Player_Win_Rates.ipynb)
	7. [Skill System](Notebooks/Players_MMR.ipynb)
	8. [Genetic Algorithms to Optimize Matchmaking](Notebooks/Matchmaking_GA.ipynb)
3. **Reports**
4. **Requirements**
5. **src**


---

## About the Game

[Dota 2](https://www.dota2.com/home) is a popular free-to-play MOBA *(**M**ultiplayer **O**nline **B**attle **A**rena)* developed by **Valve**. It is played in matches between two teams of five players, with each team occupying and defending their own separate base on the map. Each player independently controls a powerful character known as a "hero" with unique abilities and play styles. During a match, players collect experience points and items for their heroes to defeat the opposing team's heroes in player-versus-player *(PVP)* combat. A team wins by being the first to destroy the other team's "Ancient," a large structure located within their base.

## Dataset Description

This dataset was collected by [**Devin Anzelmo**](https://www.kaggle.com/datasets/devinanzelmo/dota-2-matches/data) and contains 50,000 ranked ladder matches from the Dota 2 data dump created by [Opendota](https://www.opendota.com/). It was inspired by the [Dota 2 Matches](https://www.kaggle.com/jraramirez/dota-2-matches-dataset) data published by **Joe Ramir**. This is an updated and improved version of that dataset. The number of games in this dataset are played about every hour. 

> [**Quick look at how the dataset is structured**](https://www.kaggle.com/code/devinanzelmo/a-quick-look-at-dota-2-dataset)

### Dataset Directory

|   CSV File             |  Description  | Notes |
|------------------------|:--------------|:------|
|  **Match Info**                              |||
| match                  | Top-level information about each match | `tower_status` and `barracks_status` are binary masks indicating whether various structures have been destroyed |
| players                | Statistics about player's individual performance in each match | Some players chose to hide their account_id and are marked as `0` |
| player_time            | Contains XP, gold, and last-hit totals for each player at one-minute intervals | The suffix for each variable indicates the value of the `player_slot` variable |
| teamfights             | Basic information about each team fight | `start`, `end`, and `last_death` contain the time for those events in seconds |
| teamfights_players     | Detailed info about each team fight | Each row in `teamfights.csv` corresponds to ten rows in this file |
| chat                   | Chat log for all matches | These include the player's name in game |
| objectives             | Gives information on all the objectives completed, by which player and at what time |  |
| ability_upgrades       | Contains the upgrade performed at each level for each player |  |
| purchase_log           | Contains the time in seconds for each purchase made by every player in every match |  |
| **Game Info**                                |||
| ability_ids            | Ability names and ids | Use with `ability_upgrades.csv` to get the names of upgraded abilities |
| item_ids               | Contains `item_id` and item name | Use with `purchase_log.csv` to get the names of purchased items |
| hero_ids               | Contains the `name`, `hero_id`, and `localized_name` for each hero a player can pick | Concatenated this file with the one found [here](https://www.kaggle.com/datasets/nihalbarua/dota2-hero-preference-by-mmr) to obtain the `Primary Attribute` and possible Roles |
| cluster_region         | Contains the cluster number and geographic region | Allows to filter matches by region |
| patch_dates            | Release dates for various patches | Use `start_time` from `match.csv` to determine which patch was used to play in |
| **Historical Info**                          |||
| MMR                    | Contains `account_id` and players' **Matchmaking Rating** *(**MMR** for short)* | File extracted from the [**OpenDota Core Wiki**](https://github.com/odota/core/wiki/MMR-Data) where the original dataset is based from |
| player_ratings         | Skill data computed on **900k** previous matches and a possible way to measure skill rating when **MMR** is not available | `trueskill` ratings have two components, `mu`, which can be interpreted as the skill, with the higher value being better, and `sigma` which is the uncertainty of the rating. Negative `account_id` are players not appearing in other data available in this dataset |
| match_outcomes         | Results with `account_id` for **900k** matches occurring prior the rest of the dataset | Each match has data on two rows. the `rad` feature indicates whether the team is Radiant or Dire. *Useful for creating custom skill calculations* |
| **Tests**                                    |||
| test_labels            | `match_id` and `radiant_win` as integer 1 or 0 |  |
| test_player            | Full player and match table with `hero_id`, `player_slot`, `match_id`, and `account_id`|  |


---

## Aknowledgements

I would like to express my sincere gratitude to **Roddy Adams**, **Yasmin Halwani**, **Jesse Hart**, and **Josh Menke** for their invaluable industry knowledge and guidance throughout this project. Their expertise has been instrumental in shaping the direction and quality of this work.

I would also like to extend my heartfelt thanks to **Borna Ghotbi** and **Nitin Bhandari** for their mentorship and for imparting to me all the knowledge I have gained in the field of Data Science. Their wisdom and guidance have been crucial in my development and understanding in this area of study.