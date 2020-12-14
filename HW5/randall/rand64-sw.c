#ifndef sw_c
#define sw_c
#include "rand64-sw.h"
//#include <errno.h>
#include <immintrin.h>
#include <limits.h>
#include <stdio.h>
#include <time.h>
#include <stdbool.h>
#include <stdlib.h>
#endif

/* Software implementation.  */

/* Input stream containing random bytes.  */
FILE *urandstream;
struct drand48_data buf = {0};

/* Initialize the software rand64 implementation.  */
void
software_rand64_init (char *file)
{
  if(file == NULL){
    urandstream = fopen ("/dev/random", "r");
    if (! urandstream)
      abort ();
  }
  else {
    urandstream = fopen (file, "r");
    if (! urandstream)
      abort ();
  }
}

/* Return a random value, using software operations.  */
unsigned long long
software_rand64 (void)
{
  unsigned long long int x;
  if (fread (&x, sizeof x, 1, urandstream) != 1)
    abort ();
  return x;
}

/* Finalize the software rand64 implementation.  */
void
software_rand64_fini (void)
{
  fclose (urandstream);
}

bool
writebytes (unsigned long long x, int nbytes)
{
  do
    {
      if (putchar (x) < 0)
    return false;
      x >>= CHAR_BIT;
      nbytes--;
    }
  while (0 < nbytes);

  return true;
}

void mrand48_rng_init(char *file){
  file = file;
  srand48_r(time(NULL),&buf);
}

unsigned long long mrand48_rng() {
  long int a,b;
  mrand48_r(&buf,&a);
  mrand48_r(&buf,&b);
  return (((unsigned long long) a) << 32) | ((unsigned long long) b & 0x00000000FFFFFFFF);
  
}

void mrand48_rng_fini() {

}
