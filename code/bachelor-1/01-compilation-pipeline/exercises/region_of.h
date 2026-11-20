// region_of.h: guess the memory region a pointer points into (this machine only).
#ifndef REGION_OF_H
#define REGION_OF_H

const char *region_of(const void *p, const void *stack_marker);

#endif
