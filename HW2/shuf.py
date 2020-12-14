#!/usr/bin/python


import random, sys, string
import argparse

class shuf:
    def __init__(self, filename):
        if filename=="-" or filename=="":
            self.lines = ""
        else:
            f = open(filename, 'r')
            self.lines = f.readlines()
            f.close()

    def shuffling(self):
        random.shuffle(self.lines)
        return self.lines
    
    def chooseline(self):
        return random.choice(self.lines)
def main():
    usage_msg = """%prog [OPTION]... FILE

    Output randomly selected lines from FILE."""   

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?',action="store", default='')
    parser.add_argument("-n", "--head-count",action="store", dest="numlines", help="output NUMLINES lines")
    parser.add_argument("-e","--echo",action="store", nargs="+",help="treat each command line operand as an input line")
    parser.add_argument("-i","--input_range",dest="inprange",action="store",help="Act as if input came from a file containing the range of unsigned decimal integers lo…hi, one per line.")
    parser.add_argument("-r","--repeat",action="store_true",help="Repeat output values, that is, select with replacement. With this option the output is not a permutation of the input; instead, each output line is randomly chosen from all the inputs. This option is typically combined with --head-count; if --head-count is not given, shuf repeats indefinitely.")
    args = parser.parse_args()

    hc_fl = False
    if args.numlines:
        hc_fl = True
        numlines = int(args.numlines)
        if numlines < 1:
            parser.error("negative count")

    rng_fl = False
    if args.inprange:
        rng_fl = True
        input_rng = args.inprange.split('-')
        if(len(input_rng) != 2):
            parser.error("invalid input range")
        low = int(input_rng[0])
        high = int(input_rng[1])
        if high < low:
            parser.error("low to high input")
        rangelist=[]
        for i in range(low,high+1):
            rangelist.append(str(i))
        random.shuffle(rangelist)

            

    inputfile = args.infile
    generator = shuf(inputfile)

    echo_fl =False
    if args.echo:
        echo_fl = True
        if args.echo == "":
            parser.error("enter stdin for echo")
        echo_list = args.echo
        random.shuffle(echo_list)

            
    
    if args.repeat and hc_fl:
        if echo_fl==False:
            if rng_fl==False:
                for i in range(0,numlines):
                    sys.stdout.write(generator.chooseline())
            elif rng_fl==True:
                for i in range(0,numlines):
                    print(random.choice(rangelist))
        elif echo_fl==True:
            if rng_fl==False:
                for i in range(0,numlines):
                    print(random.choice(echo_list))
            elif rng_fl:
                for x in range(0,numlines):
                    print(random.choice(rangelist))
                for i in range(0,numlines):
                    print(random.choice(echo_list))

                
    elif args.repeat and hc_fl==False:
        if echo_fl==False:
            if rng_fl==False:
                while True:
                    sys.stdout.write(generator.chooseline())
            elif rng_fl ==True:
                while True:
                    print(random.choice(echo_list))
        elif echo_fl==True:
            if rng_fl ==False:
                while True:
                    print(random.choice(echo_list))
            elif rng_fl == True:
                while true:
                    print (random.choice(echo_list))
                    print (random.choice(rangelist))

    elif hc_fl and args.repeat == False:
        if echo_fl==False:
            if rng_fl==False:
                temp = generator.shuffling()
                if(numlines<=len(generator.lines)):
                    for i in range(0,numlines):
                        sys.stdout.write(temp[i])
                elif(numlines>len(generator.lines)):
                     for x in generator.shuffling():
                         sys.stdout.write(x)
            
            elif rng_fl == True:
                try:
                    for i in range(0,numlines):
                        print(rangelist[i])
                except:
                    for i in rangelist:
                        print(i)
        elif echo_fl==True:
            if rng_fl ==False:
                if(numlines<=len(echo_list)):
                    for i in range(0,numlines):
                        print(echo_list[i])
                elif(numlines>len(echo_list)):
                    for i in echo_list:
                        print(i)
            elif rng_fl == True:
                if(numlines<=len(echo_list) and numlines<=len(rangelist)):
                    for i in range(0,numlines):
                        print(echo_list[i])
                        print(rangelist[i])
                else:
                    for i in echo_list:
                        print(i)
                    for j in rangelist:
                        print(j)
    elif rng_fl and args.repeat==False and hc_fl==False and echo_fl==False:
        for x in rangelist:
            print(x)
    elif echo_fl and args.repeat==False and hc_fl ==False and rng_fl ==False:
        for x in echo_list:
            print(x)
                
                        
                
                
    else:
        for x in generator.shuffling():
            sys.stdout.write(x)
    
if __name__ == "__main__":
    main()
