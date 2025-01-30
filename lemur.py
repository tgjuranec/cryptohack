from PIL import Image

lemur = Image.open('lemur.png').convert('RGB')
flag = Image.open('flag.png').convert('RGB')

lemur_pixels = lemur.load()
flag_pixels = flag.load()

width, height = lemur.size

for y in range(height):
    for x in range(width):
        rl, gl, bl = lemur_pixels[x, y]
        rf, gf, bf = flag_pixels[x, y]
        lemur_pixels[x, y] = (rl^rf, gf^gl, bl^bf)

        
lemur.save('output.png')
