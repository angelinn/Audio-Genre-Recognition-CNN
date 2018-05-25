from subprocess import Popen, PIPE, STDOUT

SOX_PATH = 'D:\\Program Files (x86)\\sox-14-4-2\\sox'
AUDIO_DIR = 'D:\\Repositories\\AudioClassification\\fma_small\\000\\000002.mp3'

command = "\"{}\" \"{}\" -n spectrogram -Y 200 -X {} -m -r -o {}.png".format(SOX_PATH,AUDIO_DIR,50,'sp')
print(command)

pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False, cwd='D:\\Repositories\\AudioClassification\\')
output, errors = pipe.communicate()
if errors:
    print(errors)

print(output)
print('Done')