# Make x86-64 random byte generators.

# Copyright 2015, 2020 Paul Eggert

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

# Optimization level.  Change this -O2 to -Og or -O0 or whatever.
OPTIMIZE = -O2

# The C compiler and its options.
CC = gcc
CFLAGS = $(OPTIMIZE) -g3 -Wall -Wextra -fanalyzer \
  -march=native -mtune=native -mrdrnd

# The archiver command, its options and filename extension.
TAR = tar
TARFLAGS = --xz --transform 's,^,randall/,'
TAREXT = txz

default: randall

randall: randall.c rand64-hw.c rand64-sw.c options.c output.c
	$(CC) $(CFLAGS) randall.c rand64-hw.c rand64-sw.c options.c output.c -o randall

assignment: randall-assignment.$(TAREXT)
assignment-files = COPYING Makefile randall.c
randall-assignment.$(TAREXT): $(assignment-files)
	$(TAR) $(TARFLAGS) -cf $@ $(assignment-files)

submission: randall-submission.$(TAREXT)
submission-files = $(assignment-files) \
  notes.txt options.c options.h output.c output.h rand64-sw.c rand64-sw.h rand64-hw.c rand64-hw.h
randall-submission.$(TAREXT): $(submission-files)
	$(TAR) $(TARFLAGS) -cf $@ $(submission-files)

check: run_check
run_check: randall
	if [ `./randall 1000 | wc -c` -eq 1000 ]; \
	then echo "Success"; \
	else echo "Fail"; \
	fi;
	if [ `./randall -i rdrand 1000 | wc -c` -eq 1000 ]; \
        then echo "Success"; \
        else echo "Fail";\
        fi;
	if [ `./randall -i mrand48_r 1000 | wc -c` -eq 1000 ]; \
        then echo "Success"; \
        else echo "Fail"; \
        fi;
	if [ `./randall -i mrand48_r -o 100 1000 | wc -c` -eq 1000 ]; \
        then echo "Success"; \
        else echo "Fail"; \
	fi;
	if [ `./randall -i rdrand -o stdio 1000| wc -c` -eq 1000 ]; \
        then echo "Success"; \
        else echo "Fail"; \
	fi;
	if [ `./randall -i rdrand -o 1 20000 | wc -c` -eq 20000 ]; \
        then echo "Success"; \
        else echo "Fail"; \
        fi;
	if [ `./randall -i /dev/null -o 1 1040| wc -c` -eq 1040 ]; \
        then echo "Success"; \
        else echo "Fail"; \
        fi;
.PHONY: default clean assignment submission

clean:
	rm -f *.o *.$(TAREXT) randall
