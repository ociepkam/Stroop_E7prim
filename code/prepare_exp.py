#!/usr/bin/env python
# -*- coding: utf8 -*

import random
import math
from psychopy import visual

stim_text = {'CZERWONY': 'red', 'NIEBIESKI': '#5e75d9', 'BRAZOWY': '#574400', 'ZIELONY': 'green'}  # text: color

stim_neutral = "HHHHHHHH"

colors_text = list(stim_text.keys())
random.shuffle(colors_text)
colors_names = [stim_text[color] for color in colors_text]
left_hand = colors_text[:2]
right_hand = colors_text[2:]

last_color = None


def prepare_trial(trial_type, win, words_dist, stim_size):
    global last_color

    if trial_type == 'trial_con_con':
        possible_text = list(stim_text.keys())
        if last_color is not None:
            possible_text.remove([k for k, v in stim_text.items() if v == last_color][0])
        text = random.choice(possible_text)
        color = stim_text[text]
        words = [text, text]
        stim1 = visual.TextStim(win, color=color, text=words[0], height=stim_size, pos=(0, words_dist / 2))
        stim2 = visual.TextStim(win, color=color, text=words[1], height=stim_size, pos=(0, -words_dist / 2))
        stim_list = [stim1, stim2]

    elif trial_type.startswith("trial_inc_inc_"):
        text = random.choice(list(stim_text.keys()))
        if text in left_hand:
            possible_colors = [stim_text[key] for key in right_hand]
        else:
            possible_colors = [stim_text[key] for key in left_hand]
        if last_color in possible_colors:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)

        space = stim_size * int(trial_type[-1])

        words = [text, text]
        stim1 = visual.TextStim(win, color=color, text=words[0], height=stim_size, pos=(0, words_dist / 2 + space))
        stim2 = visual.TextStim(win, color=color, text=words[1], height=stim_size, pos=(0, -words_dist / 2 - space))
        stim_list = [stim1, stim2]

    elif trial_type == 'trial_neu_neu':
        possible_colors = list(stim_text.values())
        if last_color is not None:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)
        words = [stim_neutral, stim_neutral]
        stim1 = visual.TextStim(win, color=color, text=words[0], height=stim_size, pos=(0, words_dist / 2))
        stim2 = visual.TextStim(win, color=color, text=words[1], height=stim_size, pos=(0, -words_dist / 2))
        stim_list = [stim1, stim2]

    else:
        raise Exception(f'{trial_type} - wrong trigger type')

    last_color = color

    # print({'trial_type': trial_type, 'text': words, 'color': color, 'stim': [stim1, stim2]})
    return {'trial_type': trial_type, 'text': words, 'color': color, 'stim': stim_list}


def prepare_part(trials_con_con,
                 trials_inc_inc_space0, trials_inc_inc_space1,
                 trials_inc_inc_space2, trials_inc_inc_space3,
                 trials_neu_neu,
                 win, words_dist, stim_size):
    trials = ['trial_con_con'] * trials_con_con + \
             ['trial_inc_inc_space0'] * trials_inc_inc_space0 + \
             ['trial_inc_inc_space1'] * trials_inc_inc_space1 + \
             ['trial_inc_inc_space2'] * trials_inc_inc_space2 + \
             ['trial_inc_inc_space3'] * trials_inc_inc_space3 + \
             ['trial_neu_neu'] * trials_neu_neu
    random.shuffle(trials)
    return [prepare_trial(trial_type, win, words_dist, stim_size) for trial_type in trials]


def prepare_exp(config, win):
    training1_trials = prepare_part(config['Training1_trials_con_con'],
                                    config['Training1_trials_inc_inc_space0'],
                                    config['Training1_trials_inc_inc_space1'],
                                    config['Training1_trials_inc_inc_space2'],
                                    config['Training1_trials_inc_inc_space3'],
                                    config['Training1_trials_neu_neu'],
                                    win, config["words_dist"], config["stim_size"])

    training2_trials = prepare_part(config['Training2_trials_con_con'],
                                    config['Training2_trials_inc_inc_space0'],
                                    config['Training2_trials_inc_inc_space1'],
                                    config['Training2_trials_inc_inc_space2'],
                                    config['Training2_trials_inc_inc_space3'],
                                    config['Training2_trials_neu_neu'],
                                    win, config["words_dist"], config["stim_size"])

    experiment_trials = prepare_part(config['Experiment_trials_con_con'],
                                     config['Experiment_trials_inc_inc_space0'],
                                     config['Experiment_trials_inc_inc_space1'],
                                     config['Experiment_trials_inc_inc_space2'],
                                     config['Experiment_trials_inc_inc_space3'],
                                     config['Experiment_trials_neu_neu'],
                                     win, config["words_dist"], config["stim_size"])

    return [training1_trials, training2_trials], experiment_trials, colors_text, colors_names
