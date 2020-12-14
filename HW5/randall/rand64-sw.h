#ifndef sw_h
#define sw_h
#include <stdlib.h>
#include <stdbool.h>
#endif
void
software_rand64_init (char *file);

unsigned long long
software_rand64 (void);

void
software_rand64_fini (void);

bool
writebytes (unsigned long long x, int nbytes);

void mrand48_rng_init(char *file);

unsigned long long mrand48_rng();

void mrand48_rng_fini();
