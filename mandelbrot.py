#!/usr/bin/python
###################
# config
##################

offset = (0.0, 0.0)
zoom = 1
img_size = 400

# looks cool:
#offset = (0.4, -0.2)
#zoom = 50
#img_size = 800

# looks REALLY cool:
#offset = (-0.79, 0.15)
#img_size = 200
#zoom = 20
# zooming more only makes it look cooler:
#zoom = 50
#zoom = 100
#zoom = 150
#zoom = 5



############################
############################















import Image
import sys

class ProgressBar (object):
    def __init__(self, length = 50):
        """
        create object at 0 percent and set the size of the bar on screen
        50 by default
        """
        self.length = length
        self.current = 0

    def get(self):
        """
        return the current percentage
        """
        return self.current

    def set(self, i):
        """
        set the current percentage
        """
        if i > 100:
            i = 100
        if i < 0:
            i = 0
        self.current = i

    def increment(self, i):
        """
        increment the current percentage by i
        """
        if self.current <= 100 - i:
            self.current += i
        else:
            self.current = 100

    def show(self):
        """
        display the bar
        """
        i = self.current / (100/self.length)
        sys.stdout.write(("\r%s %% " % str(self.current).rjust(4)) + "[" + ("=" * i) + ">" + (" " * (self.length - i)) + "\b]")
        sys.stdout.flush()


def complex_mult(a, b=False):
    if not b:
        b = a
    return ((a[0] * b[0]) + (-1 *(a[1] * b[1])), (a[0] * b[1]) + (a[1] * b[0]))


def complex_div(a, b):
    conj = (b[0], -1 * b[1])
    top = complex_mult(a, conj)
    # should always be real
    bottom = complex_mult(b, conj)[0]
    return (float(top[0])/float(bottom), float(top[1])/float(bottom))


def mandelbrot(a, b, silent=True):
    
    # complex constant
    c = (float(a), float(b))
    
    z = (0.0, 0.0)
    
    for i in range(0, 101):
        # square z
        sq_z = complex_mult(z, z)
        # iterate
        z = (sq_z[0] + c[0], sq_z[1] + c[1])
    
        # calculate the square of the magnitude of z
        z_mag = (z[0]) + (z[1]*z[1])
    
        # compare against the square of 2 (4)
        if z_mag > 4:
            if not silent:
                print a,"+",str(b)+"i","blew up after",str(i),"iterarions"

            return i * -1

    if not silent:
        print a,"+",str(b)+"i", "is in the mandelbrot set"

    return 1

zoom *= (float(img_size)/400.0)

step_size = 0.01 / zoom

img = Image.new( 'RGB', (img_size,img_size), "white")
pixels = img.load() # create the pixel map

running_tot = 0
total_pix = img_size * img_size
print "Generating image..."
bar = ProgressBar(50)

for i in range(img.size[0]):    # for every pixel:
    for j in range(img.size[1]):
        a = (float(i - (img_size / 2)) * step_size)
        b = (float(j - (img_size / 2)) * step_size)
        m = mandelbrot(a + float(offset[0]), b + float(offset[1]))
        if m > 0:
            # set the pixel to white for members
            pixels[i,j] = (0, 0, 0)
        elif m < -2:
            g = int(m*-2.55)
            pixels[i,j] = (0, g, 0)
        else:
            pixels[i,j] = (0, 0, 0)

        running_tot += 1
    
    bar.set(int(float(running_tot)/float(total_pix) * 100))
    bar.show()

print "\nDone"

img.save("mandelbrot.bmp")
#img.show()
