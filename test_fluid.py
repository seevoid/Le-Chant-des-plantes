import time
import fluidsynth

fs = fluidsynth.Synth()
fs.start('alsa')

sfid = fs.sfload("/home/seevoid/sf2_bank_2/exotic_harp.sf2")
fs.program_select(0, sfid, 0, 0)

while True:

    fs.noteon(0, 60, 100)
    fs.noteon(0, 67, 90)
    fs.noteon(0, 76, 100)

    fs.noteon(1, 60, 100)
    fs.noteon(1, 67, 90)
    fs.noteon(1, 76, 100)

    time.sleep(0.2) 


    fs.noteoff(0, 60)
    fs.noteoff(0, 67)
    fs.noteoff(0, 76)

fs.delete()