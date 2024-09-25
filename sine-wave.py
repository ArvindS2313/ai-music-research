# import pretty_midi
# import soundfile as sf

# midi_data = pretty_midi.PrettyMIDI('music/smoothed-song.midi')
# audio_data = midi_data.synthesize()
# sf.write('output.wav', audio_data, 44100)

# C:\Users\Arvind\fluidsynth-2.3.6-win10-x64\bin\fluidsynth.exe

import pretty_midi
import fluidsynth
import numpy as np
import soundfile as sf

# Load MIDI file
midi_data = pretty_midi.PrettyMIDI('your_file.mid')

# Initialize FluidSynth with your SoundFont file
sf = fluidsynth.Synth(gain=0.7)
sf.start(driver="dsound")  # use "coreaudio" on macOS, "dsound" on Windows, "alsa" on Linux
sf.sfload('your_soundfont.sf2')

# Render the audio for each note in the MIDI file
audio = []
for instrument in midi_data.instruments:
    sf.program_select(0, 0, 0, instrument.program)
    for note in instrument.notes:
        sf.noteon(0, note.pitch, int(note.velocity * 127))
        audio += [sf.get_samples(note.end - note.start)]
        sf.noteoff(0, note.pitch)

sf.delete()

# Convert the list of audio samples to a NumPy array
audio = np.concatenate(audio)

# Save to a WAV file
sf.write('output.wav', audio, 44100)
