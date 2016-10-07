import glob, os
dir = r'C:\Users\Mukta\Dropbox\ICDAR_2013\ICDAR-2011_data\images'
pattern = r'*.png'
titlePattern = r'new(%s)'
num = 1;
old_label = ' '
for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
    old_name, ext = os.path.splitext(os.path.basename(pathAndFilename))
    new_label = old_name.partition('_')[0];    
    if new_label !=old_label:
        old_label = new_label
        num = 1;
    new_name = new_label + '_num' + str(num) + ext
    num = num + 1
    os.rename(pathAndFilename, os.path.join(dir,new_name))
