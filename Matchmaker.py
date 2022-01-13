#!/usr/bin/env python
# coding: utf-8

# # Matchmaker (ver. 1.0)
# 
# ## Algorithmic Multi-Instrumental MIDI Continuation Implementation
# 
# ***
# 
# Powered by tegridy-tools: https://github.com/asigalov61/tegridy-tools
# 
# ***
# 
# #### Project Los Angeles
# 
# #### Tegridy Code 2021
# 
# ***

# # (Setup Environment)

# In[ ]:


#@title Install all dependencies (run only once per session)

get_ipython().system('git clone https://github.com/asigalov61/tegridy-tools')
get_ipython().system('pip install tqdm')


# In[ ]:


print('Loading needed modules. Please wait...')
import os

from datetime import datetime

import secrets, random

import copy

import tqdm
from tqdm import tqdm

import re

os.chdir('/notebooks/tegridy-tools/tegridy-tools')

print('Loading TMIDIX module...')
import TMIDIX

print('Loading HaystackSearch module...')
from HaystackSearch import HaystackSearch

os.chdir('/notebooks/')

print('Done!')


# ***
# 
# # (Matchmaker Music Database)
# 
# # (Download ready-to-use database or make your own below)
# 
# ***

# # (Download)

# In[ ]:


# Download ready-to-use Matchmaker Music Database

get_ipython().system('wget --no-check-certificate -O \'Matchmaker-MI-Database.pickle\' "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118535&authkey=AMzk2KgwX1Di0z8"')


# ***
# 
# # (Make your own Matchmaker Music Database)

# In[ ]:


# Download and unzip LAKH MuseNet MIDI Dataset (Recommended)

get_ipython().system('wget --no-check-certificate -O \'LAKH-MuseNet-MIDI-Dataset.zip\' "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118520&authkey=AN-gn1ZxEnO4khE"')

get_ipython().system("unzip 'LAKH-MuseNet-MIDI-Dataset.zip'")


# ## (Process MIDIs)

# In[ ]:


## Process MIDIs

sorted_or_random_file_loading_order = False


print('TMIDIX MIDI Processor')
print('Starting up...')
###########

files_count = 0

gfiles = []

melody_chords_f = []

###########

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

dataset_addr = "/notebooks/LAKH MuseNet-CC-BY-NC-SA/"
os.chdir(dataset_addr)
filez = list()
for (dirpath, dirnames, filenames) in os.walk(dataset_addr):
    filez += [os.path.join(dirpath, file) for file in filenames]
print('=' * 70)

if filez == []:
  print('Could not find any MIDI files. Please check Dataset dir...')
  print('=' * 70)

if sorted_or_random_file_loading_order:
  print('Sorting files...')
  filez.sort()
  print('Done!')
  print('=' * 70)
else:
  random.shuffle(filez)

v = 1
print('Processing MIDI files. Please wait...')
for f in tqdm(filez[37000:]):
  try:
    fn = os.path.basename(f)
    fn1 = fn.split('.')[0]

    files_count += 1
    
    score0 = TMIDIX.midi2ms_score(open(f, 'rb').read())
    
    itrack = 1
    score = []
    while itrack < len(score0):
            for event in score0[itrack]:         
                if event[0] == 'note':
                    score.append(event)
            itrack += 1

    score1 = []

    for s in score:
        if s[0] == 'note':
            s[1] = round(s[1], -1)
            score1.append(s)
    score1.sort(key=lambda x: x[4], reverse = True)
    score1.sort(key=lambda x: x[1])


    INTS_f1 = []

    pe = score1[0]

    for i in score1:
            INTS_f1.append([int(abs(i[1]-pe[1])/ 10), int(i[2] / 10), i[3], i[4], i[5] ])


            pe = i

    inputs = []

    for i in INTS_f1:
        if i[0] < 128 and i[0] >= 0:
            
            if i[0] != 0:
                inputs.append(i[0])
            
            inputs.append(128 + (128 * i[2]) + i[3])

    melody_chords_f.append(inputs)
    gfiles.append(f)
    
  except KeyboardInterrupt:
    print('Saving current progress and quitting...')
    break  
  
  except Exception as e:
    print('Bad MIDI:', f)
    print('Reason:', e)
    continue


# # (Test the processed output...)

# In[ ]:


out = melody_chords_f[0]

if len(out) != 0:
    
  song = []
  song = out
  song_f = []
  time = 0
  dur = 0
  vel = 0
  pitch = 0
  duration = 0

  for s in song:
      if s < 128:
        time += s
      
      else:     
        channel = (s - 128) // 128
        
        pitch = (s-128) % 128
        
        song_f.append(['note', (abs(time))*10, 250, channel, pitch, pitch ])
        
        
  detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Matchmaker',  
                                                        output_file_name = '/notebooks/Matchmaker-Music-Composition', 
                                                        track_name='Project Los Angeles', 
                                                        number_of_ticks_per_quarter=500)

  print('Done!')


# # (Save processed MIDIs to Matchmaker Database)

# In[ ]:


# Save the data

INTS = []
for m in melody_chords_f:
    INTS.extend(m)
    
len(INTS)

TMIDIX.Tegridy_Any_Pickle_File_Writer(INTS, '/notebooks/Matchmaker-MI-Database')


# ***
# 
# # (Load Matchmaker Music Database)
# 
# ***

# In[ ]:


# Load the database

INTS = []

INTS = TMIDIX.Tegridy_Any_Pickle_File_Reader('/notebooks/Matchmaker-MI-Database')

print('=' * 70)
print('Loaded', len(INTS), 'parameters.')
print('=' * 70)
print('Done!')


# ***
# 
# # (Generate)
# 
# ***

# ## (Self-continuation from the database)

# In[ ]:


# Self-continuation from the database

## WIP. Options will be added and explained in the next update

print('=' * 70)
print('Matchmaker Music Continuation Generator')
print('=' * 70)

idx = -1

while idx == -1:

    s = secrets.randbelow(len(INTS))
    print(s)
    d = 8
    nt = 150

    idx = HaystackSearch(INTS[s:s+d], INTS[s+d+1:])
  
    print(idx)

out = INTS[s-nt:s+d] + INTS[s+d+idx:s+d+idx+nt]

print('=' * 70)

for i in range(3):
    d = 8
    idx1 = -1
    while idx1 == -1:
        idx1 = HaystackSearch(out[-d:], INTS[idx+nt:])
        print('idx1:', idx1)
        d -= 1
    out += INTS[idx1:idx1+nt]
    idx = idx1

    
print('=' * 70)
    
    
song_f = []

if len(out) != 0:
  song = []
  song = out
  song_f = []
  time = 0
  dur = 0
  vel = 0
  pitch = 0
  duration = 0
  count = 0
  for s in song:
      if s < 128:
        time += s
      
      else:     
        channel = (s - 128) // 128
        
        pitch = (s-128) % 128
        
        song_f.append(['note', (abs(time))*10, 250, channel, pitch, pitch ])
        
        if count % nt == 0:
            song_f.append(['text_event', abs(time) * 10, 'Continuation Start Here'])
        count += 1
        
        
  detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Matchmaker',  
                                                        output_file_name = '/notebooks/Matchmaker-Music-Composition', 
                                                        track_name='Project Los Angeles', 
                                                        number_of_ticks_per_quarter=500)

print('Done!')
print('=' * 70)


# ***
# 
# # (Custom MIDI Continuation)
# 
# ***

# ## (Load your Custom MIDI here)

# In[ ]:


# Custom MIDI option

## For best results, use multi-instrumental MIDIs with MuseNet channels structure.

## You can use any MIDI from LAKH MuseNet MIDI dataset as an easy source of compatible MIDIs

print('Loading custom MIDI...')
data = TMIDIX.Optimus_MIDI_TXT_Processor('/notebooks/tegridy-tools/tegridy-tools/seed3.mid', 
                                         dataset_MIDI_events_time_denominator=10, 
                                         perfect_timings=True, 
                                         musenet_encoding=False, 
                                         char_offset=0, 
                                         MIDI_channel=16, 
                                         MIDI_patch=range(0, 127)
                                        )
    

SONG1 = data[5]
inputs1 = []

for i in SONG1:
    if i[0] < 128 and i[0] >= 0:
            if i[0] != 0:
                inputs1.append(i[0])
            
            inputs1.append(128 + (128 * i[2]) + i[3])
            
print('Done!')


# # (Generate custom MIDI continuation)

# In[ ]:


# Custom MIDI continuation

## WIP. Options will be added and explained in the next update

### Sometimes it gets stuck on the same continuation so for now just try to reload the MIDI above and it should get unstuck. Sorry...

print('=' * 70)
print('Matchmaker Music Continuation Generator')
print('=' * 70)

d = 3


idx = -1
while idx == -1:
    x = 100
    rnd = secrets.randbelow(len(INTS))
    idx = HaystackSearch(inputs1[:x][-d:], INTS[rnd:])
    print(idx)
    x -= 1
    
print('=' * 70)
    
song_f = []
out = copy.deepcopy(inputs1[:x]) + copy.deepcopy(INTS[rnd+idx:rnd+idx+x])
if len(out) != 0:
  song = []
  song = out
  song_f = []
  time = 0
  dur = 0
  vel = 0
  pitch = 0
  duration = 0
  count = 0
  for s in song:
      if s < 128:
        time += s
      
      else:     
        channel = (s - 128) // 128
        
        pitch = (s-128) % 128
        
        song_f.append(['note', (abs(time))*10, 250, channel, pitch, pitch ])
        
        if count % x == 0:
            song_f.append(['text_event', abs(time) * 10, 'Continuation Start Here'])
        count += 1
        
        
  detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                        output_signature = 'Matchmaker',  
                                                        output_file_name = '/notebooks/Matchmaker-Music-Composition', 
                                                        track_name='Project Los Angeles', 
                                                        number_of_ticks_per_quarter=500)
print('Done!')
print('=' * 70)


# # Congrats! You did it! :)
