/* pipeline.h: run k commands connected by k - 1 pipes. */
#ifndef PIPELINE_H
#define PIPELINE_H

int run_pipeline(char **const stages[], int k);

#endif
