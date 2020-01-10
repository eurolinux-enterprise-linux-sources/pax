#
# Copyright (c) 2001, 2002, 2003 Thorsten Kukuk <kukuk@suse.de>
#
AUTOMAKE_OPTIONS = 1.7 gnits
MAINT_CHARSET = latin1

CLEANFILES = *~

AM_CFLAGS = @EXTRA_CFLAGS@ -D_GNU_SOURCE
INCLUDES = -I$(top_srcdir)/lib -I$(top_srcdir) -I$(top_builddir) -I$(srcdir)

EXTRA_DIST = ${MANS}

noinst_HEADERS = cache.h cpio.h extern.h ftree.h options.h\
	 pat_rep.h pax.h sel_subs.h tables.h tar.h

man_MANS = pax.1

bin_PROGRAMS = pax

pax_SOURCES = ar_io.c ar_subs.c buf_subs.c cache.c cpio.c\
	file_subs.c ftree.c gen_subs.c getoldopt.c options.c\
	pat_rep.c pax.c sel_subs.c tables.c tar.c tty_subs.c

pax_LDADD = $(top_builddir)/lib/libbsdfunc.a
