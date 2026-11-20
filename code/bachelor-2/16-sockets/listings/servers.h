/* servers.h: one request per connection, served three ways. */
#ifndef SERVERS_H
#define SERVERS_H

void serve_fork(int lfd, long connections);
void serve_threads(int lfd, long connections);
void serve_poll(int lfd, long connections);

#endif
