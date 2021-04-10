import os.path, imageio


def create_gif(filenames, duration): 
    '''Function to create GIF out of images'''
    img = [] 
    for filename in filenames: 
    	img.append(imageio.imread(filename)) 
    output_file = 'model.gif'
    imageio.mimsave(output_file, img, duration=duration)


duration = 0.3
filenames = sorted(filter(os.path.isfile, [x for x in os.listdir() if x.endswith(".png")]), key=lambda p: os.path.exists(p) and os.stat(p).st_mtime or time.mktime(datetime.now().timetuple())) 
create_gif(filenames,duration) #creating gif  