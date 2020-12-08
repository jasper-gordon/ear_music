'''
Author: Jasper Gordon
Class: CSCI 3725
Date 7 December 2020
Description: This file contains scripts that, when placed into the body of https://earsketch.gatech.edu/earsketch2/, 
    will generate a musical track. While written in Python, this file contains built-in methods and musical loop
    names special to EarSketch, and thus cannot be run in a normal IDE. This file will create a slightly 
    different song each time it is run, but the core algorithm is consisten with two drum/percussion
    beats and an ever changing third track with varying pitch levels.
'''

from earsketch import *
import random
init()
setTempo(90) 
#A list containing the various tracks cycled in the song
beat_bank = [YG_WEST_COAST_HIP_HOP_STRINGS_CHORDS_1, RD_RNB_ACOUSTIC_NYLONSTRING_4, RD_UK_HOUSE_ACOUSTICGUITAR_6, YG_GOSPEL_STRINGS_2, RD_RNB_ACOUSTIC_NYLONSTRING_5]

def low_beat_gen(length):
    '''
    Method that makes slow beat strings. Goal is to have fewer, longer notes.
    Returns a string made up of 0's, -'s, and +'s.
    '''
    beat = "0"
    char_vault = ['0++0+']
    i = 0
    while i < length:
        new_char = random.choice(char_vault)
        beat += new_char  
        i += 1
    return beat

def low_version(beat, start, reps):
    '''
    Lowers the pitch of a given beat by 12 units. Takes a beat vairable, an int starting measure,
        and an int desired number of repetions as arguments.
    '''
    fitMedia(beat, 3, start, start + (2 * reps))
    setEffect(3, PITCHSHIFT, PITCHSHIFT_SHIFT, -12, start)
    
def high_version(beat, start, reps):
    '''
    Raises the pitch of a given beat by 12 units. Takes a beat vairable, an int starting measure,
        and an int desired number of repetions as arguments.
    '''
    fitMedia(beat, 4, start, start + (2 * reps))
    setEffect(4, PITCHSHIFT, PITCHSHIFT_SHIFT, 12, start)
    
def play(beat, start, stop):
    '''
    Plays a given beat within the stated measures. Randomly decides whether to play
        a modified version of the beat as well, calling the pitch changing methods
        50% of the time. Takes a beat vairable, an int start measure, and an int
        end measure as variables.
    '''
    fitMedia(beat, 2, start, stop)
    for measure in range (start, stop):
        if (measure - 1) % 4 == 0: #Most beat loops last for four measures
            r_value = random.randint(1,4)
            num_plays = random.randint(1,2) #Decides to play mutated version once or twice
            if r_value == 1:
                low_version(beat, measure, num_plays)
            if r_value == 2:
                high_version(beat, measure, num_plays)

def list_generator(nums):
    '''
    Method to generate a random range with no consecutive repeating numbers and attempts to play tracks equally.
    Takes an int desired number of values as an argument. Returns list of ints.
    '''
    output = []
    prev_num = -1 #Keeps track of previous two beats played
    second_prev_num = -1
    num_range = len(beat_bank)
    count = 0
    while count < nums:
        new_value = random.randint(0, num_range - 1)
        if new_value != prev_num and new_value != second_prev_num: #Making sure not to repeat
            count += 1
            second_prev_num = prev_num
            prev_num = new_value
            output.append(new_value)
    return output

def fade_intervals(min_vol, target, start, end):
    '''
    Determines the amount a song volume should change per measure. Takes the float
        starting volume, the float target volume, the int starting measure, and the int ending
        measure as arguments. Retuns a float interval value.
    '''
    volume_climb = target - min_vol
    climb_duration = end - start
    return volume_climb / climb_duration

def fade(track, first_vol, second_vol, start, end):
    '''
    Adds a volume fade to a track. Takes the int track number, the float pre-fade value,
        the float post-fade value, the int start measure, and the int end measure as arguments.
    '''
    volume = first_vol
    add_float = fade_intervals(volume, second_vol, start, end)
    for measure in range(start, end): #Fading over the course of a given interval
        setEffect(track, VOLUME, GAIN,  volume, measure)
        volume += add_float

def music_machine():
    '''
    Creates an order of tracks to play, then begins the main tracks starting at measure 13.
        EarSketch starts at measure 1, so the code is shifted by 1 to maintain sets of 12 measures.
    '''
    play_list = list_generator(12)
    count = 0
    fitMedia(YG_FUNK_CONGAS_2, 1,1,148)
    fade(1, -50, 0, 1, 5)
    fitMedia(EIGHT_BIT_ANALOG_DRUM_LOOP_003, 5, 5, 146)
    fade(5, -50, -10, 4, 9)
    for measure in range(13, 144):
        if (measure - 1) % 12 == 0:
            index = play_list[count]
            beat = beat_bank[index]
            play(beat, measure, measure + 12)
            count += 1

music_machine() 
finish()


#To Do:
#Mix up/add variations of drum beats throughout song
#Firgiure out a softer transition between sounds
#Add a beat using low_beat_gen