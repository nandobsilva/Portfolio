# Make file for overseer and controller

CC = gcc
CFLAGS = -Wall

all:
	$(CC) $(CFLAGS) overseer.c functions.c  queueControl.c  -o overseer  -lpthread
	$(CC) $(CFLAGS) controller.c functions.c -o controller

clean:
	rm overseer controller