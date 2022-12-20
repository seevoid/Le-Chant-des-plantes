import time
import fluidsynth

fs1 = fluidsynth.Synth()
fs2 = fluidsynth.Synth()

fs1.start('alsa')
fs2.start('alsa')

sfid1 = fs1.sfload("/home/seevoid/sf2_bank/JR_backgr.sf2")
sfid2 = fs2.sfload("/home/seevoid/sf2_bank/JR_organ.sf2")

fs1.program_select(0, sfid1, 0, 0)
fs2.program_select(0, sfid2, 0, 0)


fs1.noteon(0, 60, 120)
fs1.noteon(0, 67, 120)
fs1.noteon(0, 76, 120)

for i in range(50):
	fs2.noteon(0, 60, 120)
	time.sleep(0.5)
	fs2.noteoff(0, 60)
	fs2.noteon(0, 67, 120)
	time.sleep(0.5)
	fs2.noteoff(0, 67)
	fs2.noteon(0, 76, 120)
	time.sleep(0.5)
	fs2.noteoff(0, 76)

time.sleep(15)

fs1.noteoff(0, 60)
fs1.noteoff(0, 67)
fs1.noteoff(0, 76)

time.sleep(1.0)

fs1.delete()