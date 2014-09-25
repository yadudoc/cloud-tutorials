
MODIS = lib/libmodis.so

BINS = bin/rgb_histogram bin/rgb_adjust_color

all: $(MODIS) $(BINS)

CFLAGS = -g -std=gnu99 -fPIC -Wall -I .

# Include library objects that are not a main program file
SRCS = $(shell ls src/*.c | grep -v -- -main )
OBJS = $(patsubst %.c,%.o,$(SRCS))

map = $(foreach a,$(2),$(call $(1),$(a)))
get_main = src/$(patsubst bin/%,%,$(1))-main.c
MAINS = $(call map,get_main,$(BINS))

LIBS   = -L lib -lmodis
RPATHS = -Wl,-rpath -Wl,$(PWD)/lib
LDFLAGS = $(LIBS) $(RPATHS)

lib:
	mkdir lib

bin/rgb_histogram: src/rgb_histogram-main.o $(MODIS)
	gcc -o $(@) $(<) $(OBJS) $(LDFLAGS)

bin/rgb_adjust_color: src/rgb_adjust_color-main.o $(MODIS)
	gcc -o $(@) $(<) $(OBJS) $(LDFLAGS)

$(MODIS): lib $(OBJS)
	gcc -shared -o $(@) $(OBJS)

clean:
	rm -fv $(BINS) $(OBJS) $(MODIS)

# Use this when patsubst get confusing
debug_build:
	@echo "BINS:      $(BINS)"
	@echo "BIN_NAMES: $(BIN_NAMES)"
	@echo "MAINS:     $(MAINS)"
	@echo "OBJS:      $(OBJS)"
	@echo "SRCS:      $(SRCS)"
