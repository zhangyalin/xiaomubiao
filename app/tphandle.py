#-*- coding: UTF-8 -*-    
import os  
from PIL import Image  
import imageio
from PIL import Image,ImageDraw,ImageFont  

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )   #这里定义后，后面字符串就不需要额外使用unicode(comment,'utf-8')， 否则会报错，提示TypeError: decoding Unicode is not supported

def processPngJpg(path, comment, output):
    im = Image.open(path)
    draw = ImageDraw.Draw(im)
    fontsize = im.size[0]*3/len(comment)
    if fontsize <= 10:
        fontsize = 10
    elif fontsize >= 40:
        fontsize = 40
    else:
        pass
    print "fontsize:", fontsize
    ttfont = ImageFont.truetype('./STXIHEI.TTF', fontsize)
    #draw.text((  (im.size[0]- fontsize*len(comment)/3)/2 ,   im.size[1]*7/10),unicode(comment,'utf-8'), fill=(0,0,0),font=ttfont)
    draw.text((  (im.size[0]- fontsize*len(comment)/3)/2 ,   im.size[1]*7/10),comment, fill=(0,0,0),font=ttfont)   #为什么这里不需要转码(否则报错)，是因为webdb.py 开头有定义sys.setdefaultencoding( "utf-8" )
    #im.save(outputpath+os.path.splitext(path)[1])
    print 'processPngJpg:', output
    im.save(output)

def PngJpgTogif(path, comment, output):
    im = Image.open(path)
    draw = ImageDraw.Draw(im)
    fontsize = im.size[0]*3/len(comment)
    if fontsize <= 10:
        fontsize = 10
    elif fontsize >= 40:
        fontsize = 40
    else:
        pass
    print "fontsize:", fontsize
    ttfont = ImageFont.truetype('./STXIHEI.TTF', fontsize)
    #draw.text((  (im.size[0]- fontsize*len(comment)/3)/2 ,   im.size[1]*7/10),unicode(comment,'utf-8'), fill=(0,0,0),font=ttfont)
    draw.text((  (im.size[0]- fontsize*len(comment)/3)/2 ,   im.size[1]*7/10),comment, fill=(0,0,0),font=ttfont)   #为什么这里不需要转码(否则报错)，是因为webdb.py 开头有定义sys.setdefaultencoding( "utf-8" )
    #im.save(outputpath+os.path.splitext(path)[1])
    print 'processPngJpg:', output
    im.save(output)
    tmpframes = [] 
    tmpframes.append(imageio.imread(output))
    tmpframes.append(imageio.imread(output))
    imageio.mimsave('tmp.gif', tmpframes, 'GIF', duration = 0.1)
    
    
def analyseImage(path):  
    ''''' 
    Pre-process pass over the image to determine the mode (full or additive). 
    Necessary as assessing single frames isn't reliable. Need to know the mode  
    before processing all frames. 
    '''  
    im = Image.open(path)
    results = {  
        'size': im.size,  
        'mode': 'full',
        'dura': (im.info)['duration']
    }  
    try:  
        while True:  
            if im.tile:  
                tile = im.tile[0]  
                update_region = tile[1]  
                update_region_dimensions = update_region[2:]  
                if update_region_dimensions != im.size:  
                    results['mode'] = 'partial'  
                    break  
            im.seek(im.tell() + 1)  
    except EOFError:  
        pass  
    return results  
  
  
def processGif(path, comment, output):  
    ''''' 
    Iterate the GIF, extracting each frame. 
    '''  
    result = analyseImage(path)  
    mode = result['mode']
    gifsize = result['size']
    gifduration = result['dura']
    print 'mode: ', mode
    #size返回值 (179, 199) 179表示图片宽度，199表示图片高度
    print 'size: ', gifsize
    #计算帧之间的频率，获取到的是毫秒，duration是秒，所以除以1000。 如返回值是70表示70ms，新gif的参数要/1000
    print 'duration: ', gifduration
    #看起来utf-8的话是用了3个字节
    print 'comment: ', comment , len(comment)

    
    im = Image.open(path)  
    i = 0  
    p = im.getpalette()  
    last_frame = im.convert('RGBA')  
    tmpframes = []  
    mkpath = ''.join(os.path.basename(path).split('.')[:-1])

    try:  
        while True:  
            print "saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile)  
              
            ''''' 
            If the GIF uses local colour tables, each frame will have its own palette. 
            If not, we need to apply the global palette to the new frame. 
            '''  
            if not im.getpalette():  
                im.putpalette(p)  
              
            new_frame = Image.new('RGBA', im.size)  
              
            ''''' 
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image? 
            If so, we need to construct the new frame by pasting it on top of the preceding frames. 
            '''  
            if mode == 'partial':  
                new_frame.paste(last_frame)  
              
            new_frame.paste(im, (0,0), im.convert('RGBA')) 
            draw = ImageDraw.Draw(new_frame)
            fontsize = gifsize[0]*3/len(comment)
            if fontsize <= 10:
                fontsize = 10
            elif fontsize >= 40:
                fontsize = 40
            else:
                pass
            print "fontsize:", fontsize
            ttfont = ImageFont.truetype('./STXIHEI.TTF', fontsize)
            #draw.text((10,10),u'hello', fill=(0,0,0),font=ttfont)
            draw.text((  (gifsize[0]- fontsize*len(comment)/3)/2 ,   gifsize[1]*7/10),unicode(comment,'utf-8'), fill=(0,0,0),font=ttfont)
            new_frame.save('%s_%d.png' % (mkpath, i), 'PNG')
            tmpframes.append(imageio.imread('%s_%d.png' % (mkpath, i)))
            #删除临时文件
            if os.path.exists('%s_%d.png' % (mkpath, i)):
                os.remove('%s_%d.png' % (mkpath, i))
            i += 1  
            last_frame = new_frame  
            im.seek(im.tell() + 1)  
    except EOFError:  
        pass  
    #imageio.mimsave(outputpath+'gif', tmpframes, 'GIF', duration = gifduration/1000)
    imageio.mimsave(output, tmpframes, 'GIF', duration = gifduration/1000)
    
  
def create_gif(image_list, gif_name):  
  
    frames = []  
    for image_name in image_list:
        img = imageio.imread(image_name)
        frames.append(img)  
    # Save them as frames into a gif   
    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.1)  
    return    
  
def main():  
    print '参数个数为:', len(sys.argv), '个参数。'
    print '参数列表:', str(sys.argv)
    im = Image.open(sys.argv[1])
    print "format: ", im.format
    if im.format == 'GIF':
        #processImage(sys.argv[1], sys.argv[2]) duration不影响gif文件的大小
        processGif(sys.argv[1], sys.argv[2])
    else:
        processPngJpg(sys.argv[1], sys.argv[2])
    #image_list = ['./11-0.png', './11-1.png', './11-2.png', './11-3.png',  './11-4.png', './11-5.png', './11-6.png', './11-7.png', './11-8.png', './11-9.png']  
    #gif_name = 'created_gif.gif'  
    #create_gif(image_list, gif_name)       
  
if __name__ == "__main__":  
    main()  