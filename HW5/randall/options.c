#ifndef options_c
#define options_c
#include "options.h"
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#endif
int options (int argc, char **argv, long long *nbytes, char **iarg, char **oarg)
{
  int opt;
  while ((opt = getopt(argc, argv, "i:o:")) != -1) {
    switch (opt) {
      case 'i':
	*iarg = optarg;
	break;
      case 'o':
	*oarg = optarg;
	break;
      default:
	fprintf (stderr, "the flag options you have given are not valid.");
	return 2; // Unrecognized option
    }
  }

  /* Check arguments.  */
  bool valid = false;
  errno = 0;
  if (argc == 2)
    {
      char *endptr;
      *nbytes = strtoll (argv[1], &endptr, 10);
      if (errno) perror (argv[1]);
      else valid = !*endptr && 0 <= *nbytes;
    }
  else if (argc == 4)
    {
      char *endptr;
      *nbytes = strtoll (argv[3], &endptr, 10);
      if (errno) perror (argv[3]);
      else valid = !*endptr && 0 <= *nbytes;
    }
  else if (argc == 6)
    {
      char *endptr;
      *nbytes = strtoll (argv[5], &endptr, 10);
      if (errno) perror (argv[5]);
      else valid = !*endptr && 0 <= *nbytes;
    }
  
  if (!valid)
    {
      fprintf (stderr, "%s: usage: %s NBYTES\n", argv[0], argv[0]);
      return 1;
    }
    return 0;
}
