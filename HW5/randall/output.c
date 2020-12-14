#ifndef HEADS
#define HEADS
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include "rand64-sw.h"
#include "output.h"
#endif

void output(long long nbytes, unsigned long long (*rand64) (void), int *output_errno, int bufsize) {
  int wordsize = sizeof rand64();
  unsigned long long x;
  
  if(bufsize >0){
    long long *buffer = malloc(bufsize*1024);
    int num_buf = nbytes/(1024*bufsize);
    int outbytes = nbytes;
    for (int i =0; i < num_buf; i++) {
      for (long long j=0; j<(8*bufsize); j++) {
	x = rand64();
	outbytes -= 128;
       	buffer[j] = x;
      }
      write(1,buffer,1024*bufsize);
    }
    for(long long k =0; k<(8*bufsize); k++) {
      x = rand64();
      buffer[k] =x;
    }
    write(1,buffer,outbytes);
    free(buffer);
  }
  else {
  do
    {
      x = rand64();
      int outbytes = nbytes < wordsize ? nbytes : wordsize;
      if (!writebytes (x, outbytes))
	{
	  *output_errno = errno;
	  break;
	}
      nbytes -= outbytes;
    }
  while (0 < nbytes);
  }
}
