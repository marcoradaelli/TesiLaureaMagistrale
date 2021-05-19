import os
import glob
import moviepy.video.io.ImageSequenceClip

def sorter(item:str):
    numero_file = item[item.rfind("/")+1:item.rfind(".")]
    return int(numero_file)

def genera_video(percorso_ingresso:str, fps:float):
    image_files = sorted(glob.glob(percorso_ingresso + "/*.png"), key=sorter)
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile('my_video.mp4')

