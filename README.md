# Project Overview



## Areas of Interest



## Problem Area



## Data Science Solution



---

# Dataset Description

*From [**Devin Anzelmo**](https://www.kaggle.com/datasets/devinanzelmo/dota-2-matches/data):*

This dataset contains 50,000 ranked ladder matches from the Dota 2 data dump created by [Opendota](https://www.opendota.com/). It was inspired by the [Dota 2 Matches](https://www.kaggle.com/jraramirez/dota-2-matches-dataset) data published here by **Joe Ramir**. This is an updated and improved version of that dataset.

Dota 2 is a popular MOBA available as free to play, and can take up thousands of hours of your life. The number of games in this dataset are played about every hour. If you like the data there are an additional 2-3 million matches easily available for download.

This dataset aims to enable the exploration of player behaviour, skill estimation, or anything else you find interesting. The intent is to create an accessible and easy-to-use resource that can be expanded and modified if needed. As such, I am open to a wide variety of suggestions as to what additions or changes to make.

> [**Quick look at how the dataset is structured**](https://www.kaggle.com/code/devinanzelmo/a-quick-look-at-dota-2-dataset)

|   CSV File             |  Description  | Notes |
|:-----------------------|:--------------|:------|
|  **Match Info**        |  |  |
| match                  | Top-level information about each match | `tower_status` and `barracks_status` are binary masks indicating whether various structures have been destroyed |
| players                | Statistics about player's individual performance in each match | Some players chose to hide their account_id and are marked as `0` |
| player_time            | Contains XP, gold, and last-hit totals for each player at one-minute intervals | The suffix for each variable indicates the value of the `player_slot` variable |
| teamfights             | Basic information about each team fight | `start`, `end`, and `last_death` contain the time for those events in seconds |
| teamfights_players     | Detailed info about each team fight | Each row in `teamfights.csv` corresponds to ten rows in this file |
| chat                   | Chat log for all matches | These include the player's name in game |
| objectives             | Gives information on all the objectives completed, by which player and at what time |  |
| ability_upgrades       | Contains the upgrade performed at each level for each player |  |
| purchase_log           | Contains the time in seconds for each purchase made by every player in every match |  |
| **Game Info**          |  |  |
| ability_ids            | Ability names and ids | Use with `ability_upgrades.csv` to get the names of upgraded abilities |
| item_ids               | Contains `item_id` and item name | Use with `purchase_log.csv` to get the names of purchased items |
| hero_ids               | Contains the `name`, `hero_id`, and `localized_name` for each hero a player can pick | Concatenated this file with the one found [here](https://www.kaggle.com/datasets/nihalbarua/dota2-hero-preference-by-mmr) to obtain the `Primary Attribute` and possible Roles |
| cluster_region         | Contains the cluster number and geographic region | Allows to filter matches by region |
| patch_dates            | Release dates for various patches | Use `start_time` from `match.csv` to determine which patch was used to play in |
| **Historical Info**    |  |  |
| MMR                    | Contains `account_id` and players' **Matchmaking Rating** *(**MMR** for short)* | File extracted from the [**OpenDota Core Wiki**](https://github.com/odota/core/wiki/MMR-Data) where the original dataset is based from |
| player_ratings         | Skill data computed on **900k** previous matches and a possible way to measure skill rating when **MMR** is not available | `trueskill` ratings have two components, `mu`, which can be interpreted as the skill, with the higher value being better, and `sigma` which is the uncertainty of the rating. Negative `account_id` are players not appearing in other data available in this dataset |
| match_outcomes         | Results with `account_id` for **900k** matches occurring prior the rest of the dataset | Each match has data on two rows. the `rad` feature indicates whether the team is Radiant or Dire. *Useful for creating custom skill calculations* |
| **Tests**              |  |  |
| test_labels            | `match_id` and `radiant_win` as integer 1 or 0 |  |
| test_player            | Full player and match table with `hero_id`, `player_slot`, `match_id`, and `account_id`|  |
