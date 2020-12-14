/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */
#ifndef MAINHEAD
#define MAINHEAD
#include <string.h>
#include <unistd.h>
#include <cpuid.h>
#include <errno.h>
#include <ctype.h>
#include <immintrin.h>
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "options.h"
#include "rand64-hw.h"
#include "rand64-sw.h"
#include "output.h"

#endif



/* Main program, which outputs N bytes of random data.  */
int
main (int argc, char **argv)
{
  long long nbytes;
  char *iarg = NULL;
  char *oarg = NULL;
  bool mrand_flg =false;
  int bufsize =0;
  if (options(argc, argv, &nbytes,&iarg,&oarg)>0)
   {
     return 1;
   }
  
  if(iarg != NULL && strcmp(iarg,"rdrand")==0) {
    if(!rdrand_supported()) {
      fprintf(stderr, "the rdrand option is not supported on this hardware\n");
      return 1;
    }
  }
  else if(iarg!=NULL && strcmp(iarg,"mrand48_r")==0) {
    mrand_flg = true;
  }
  else if(iarg!=NULL && iarg[0]== 47) {
    FILE *file;
    if((file=fopen(iarg, "r"))) {
      fclose(file);
    }
    else {
      fprintf(stderr,"invalid file, please choose one that exists\n");
      return 1;
    }
  }
  else if(iarg!=NULL) {
    fprintf(stderr, "invalid option on -i flag\n");
    return 1;
  }

  if(oarg != NULL) {
    if(strcmp(oarg,"stdio")==0) {bufsize =0;}
    else {
      for(int i = 0; oarg[i] != '\0'; i++) {
	if(isalpha(oarg[i])){
	  fprintf(stderr, "Should be N bytes where N is a valid decimal integer\n");
	    return 1;
	 }
      }
	bufsize = atoi(oarg);
	if(bufsize<0) {
	  fprintf(stderr, "Should be N bytes where N is a valid positive decimal integer\n");
	  return 1;
	}
    }
  }


   

  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */
  void (*initialize) (char *file);
  unsigned long long (*rand64) (void);
  void (*finalize) (void);
  if (mrand_flg) {
    initialize = mrand48_rng_init;
    rand64 = mrand48_rng;
    finalize = mrand48_rng_fini;
  }
  else if (rdrand_supported ())
    {
      initialize = hardware_rand64_init;
      rand64 = hardware_rand64;
      finalize = hardware_rand64_fini;
    }
  else
    {
      initialize = software_rand64_init;
      rand64 = software_rand64;
      finalize = software_rand64_fini;
    }

  initialize (iarg);
  int output_errno = 0;
  output(nbytes, rand64,&output_errno,bufsize);


  if (fclose (stdout) != 0)
    output_errno = errno;

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }

  finalize ();
  return !!output_errno;
}
