# Dota 2 Matchmaking Modelling

## Project Overview

[Dota 2](https://www.dota2.com/home) is a popular free-to-play MOBA *(**M**ultiplayer **O**nline **B**attle **A**rena)* developed by **Valve**. It is played in matches between two teams of five players, with each team occupying and defending their own separate base on the map. Each player independently controls a powerful character known as a "hero" with unique abilities and play styles. During a match, players collect experience points and items for their heroes to defeat the opposing team's heroes in player-versus-player *(PVP)* combat. A team wins by being the first to destroy the other team's "Ancient," a large structure located within their base.

Despite being released in 2013, the game still has a solid global fanbase. It has consistently maintained 500,000 monthly active users to this day. However, it has lost some users from its peak over the years to its main competitor, **League of Legends**. I am interested in exploring its player base's behavioural patterns and in-game attributes to understand player engagement in live service games and improve the player experience overall.

---

## Proposed Solution

Through analyzing data from multiple matches and utilizing various machine learning techniques such as clustering and sentiment analysis, we can construct player profiles. These profiles can then be used to match each player with the most suitable teammates and to pair them with challenging rivals to keep them engaged.

### Objectives
- Improve player engagement by enhancing matchmaking by accurately classifying players based on skill level, region, preferred position and heroes, and essential personality traits inferred from in-game activity.

### Hypotheses
- *Balancing matches based on player skill levels increases player retention.*
- *Players perform better when matched with compatible personalities, leading to increased engagement.*

### Potential Impact

Retaining users has become increasingly difficult as competition intensifies, particularly for startups and new F2P games, as seen in the case of [***Omega Strikers***](https://www.youtube.com/watch?v=6blfDQzmIoQ). Developing a successful profiling and matchmaking model that forecasts the best matchups can assist indie studios in iterating more effectively and keeping players engaged.

---

## Table of Contents

1. **Docs**
2. **Models**
3. **Notebooks**
	1. [Data Cleaning and Exploration](Notebooks/Data_Cleaning_and_Exploration.ipynb)
	2. Players EDA
	3. Chat EDA
4. **References**
5. **Reports**
6. **src**

---

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
