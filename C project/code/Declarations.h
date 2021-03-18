/*#################################################################################################################

    Written by Fernando Barbosa Silva - n10338471
    October, 2020

/#################################################################################################################*/

#ifndef FUNCTIONS
#define FUNCTIONS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <stdint.h>
#include <time.h>
#include <ctype.h>
#include <errno.h>
#include <netdb.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <pthread.h>
#include <signal.h>
#include "Declarations.h"

#define PID_PO0L_SIZE 5
#define PID_INT_SIZE 8
#define THREAD_POOL_SIZE 5

//-----------------------------------------------------------------------------------------------------------------
// STRUCTS USED BY THE OVERSEER

struct node_queue
{
    int clientfp;
    char *message;
    struct node_queue *next;
};

struct node_pid
{
    int clientfd;
    int pid;
    char time[256];
    int memoryUsage;
    char *file_args;
    int status;
    struct node_pid *next;
};

//-----------------------------------------------------------------------------------------------------------------
// linked list queue struct functions

// Free memory allocated for the list
void freeQueueMemory();

// Add node to the request pool
void enqueue(int clientfd, char *message);

// Remove node from the request pool - returns int to a clientfd, if there is one to get.
//int dequeue(char *message);
int dequeue(int *clientfb, char *message); ///test

//-----------------------------------------------------------------------------------------------------------------
/* Signal Handler for SIGINT */
void sigintHandler(int sig_num);

//-----------------------------------------------------------------------------------------------------------------
// Check if data entered in string format can be tranformed into integer value.
// returns 1 if string *number contains no valid numbers
// returns 0 if string *number contains valid number

int isNumber(char *str);

//-----------------------------------------------------------------------------------------------------------------
// Transform string to a array of string (using the space as a separator),
// uses array poiter to return the atrings
void stringToArgv(char *str, char *argvs[]);

//-----------------------------------------------------------------------------------------------------------------
// Transform a array of argument in a string, return the string using pointer (char *str_out)
void argvToString(int argc, char *argv[], char *str_out);

//-----------------------------------------------------------------------------------------------------------------
// Count arguments in a String (each word separated by space) and return i
int countArguments(char str[]);

//-----------------------------------------------------------------------------------------------------------------
// Chech if glag -t is in the arguments and is yes, check if the next argument is a integer.
// Return the t value if it is a valid number (greater than or equal 0),
// Return -1 if -t flag was found but value is not a intenger
// Return -2 if -t flag was not found
int checkTFlag(char str_in[]);

//-----------------------------------------------------------------------------------------------------------------
// Chech if glag -o flag is in the arguments , if yes return the name o the file.
// Return 1 and dave the file in the pointer *str_out
// Return -1 if -t flag was found thare is no filename after the fla
// Return 0 if flag was not found
int checkFlag(char flag[], char *str_in, char *str_out);

//-----------------------------------------------------------------------------------------------------------------
// Print the messages passed with the date and time, can use NULL if just want to print on or two string
int logDateTime(char msg1[], char msg2[], char msg3[]);

//-----------------------------------------------------------------------------------------------------------------
// Get Date and time in string format, return the string using a pointer (char *time_str)
void getDateTimeStr(char *time_str);

//-----------------------------------------------------------------------------------------------------------------
// Gets the machine IP address and return in a format string using a pointer
void getHostIp(char **ip);

//-----------------------------------------------------------------------------------------------------------------
// Print message using stdout
void printStdout(char message[]);

//-----------------------------------------------------------------------------------------------------------------
// Print message using stderror
void printStderror(char message[]);

//-----------------------------------------------------------------------------------------------------------------
// Used to send message using a socke file descriptor as a parameter
void sendMessage(int file_descriptor, const char *message);

//-----------------------------------------------------------------------------------------------------------------
// Validates arguments passed by the user in the controller
int validateArguments(int argc, char *argv[]);

//-----------------------------------------------------------------------------------------------------------------
// Receive message and validate if the entire message was received
char *recvMessage(int fd);

//-----------------------------------------------------------------------------------------------------------------
// Set the output in the overseer if flags '-o = 3 or' '-log = 4' was passed by the controller
int setOutput(int std_output, char fileName1[]);

//-----------------------------------------------------------------------------------------------------------------
// Functions to monitor the number of process running in the server (MAX 5 as defined in the requirements)

int isInPidPool(pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE], pid_t pid_id);

int addInPidPool(pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE], pid_t pid_id);

int removeFromPidPool(pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE], pid_t pid_id);

void printPid(pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE]);

void setPidPool(pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE]);

//-----------------------------------------------------------------------------------------------------------------
// Try to execute file indicated by the client. If error retur 1 otherwise return 0.
int executeFile(int clientfd, char path[], char arguments[], char path_argument[], int std_output,
                char o_f_name[], char log_f_name[], char time1[], int saved_stdout, int t,
                pthread_mutex_t mutex, pid_t pid_pool[128][8]);

//-----------------------------------------------------------------------------------------------------------------
// Validate port number passed by the user (check if it is a valid integer)
void overseerArgumentsValidation(int isNumber, int argc);

//-----------------------------------------------------------------------------------------------------------------
// Build a string with a specific start and finish index (using the space as separator)
void buildString(char str_in[], char *str_out, int index_start, int index_finish);

//-----------------------------------------------------------------------------------------------------------------
// Kill all process em close the overseer
int killAllProcess(pid_t pid, pthread_mutex_t mutex);

//-----------------------------------------------------------------------------------------------------------------
// Calculate the memory used by a process usig as parameter the pro/maps file. Return the value as a integer.
int calcMemory(char *str);

//-----------------------------------------------------------------------------------------------------------------
// Gets the process memory usage by the pid specified, return the value as long long int in bytes
long long int getProcessMemoryUsage(int pid);

//-----------------------------------------------------------------------------------------------------------------
// Get the local server total memory and return it as a lon lon int in bytes.
long long int getTotalMemory();

//-----------------------------------------------------------------------------------------------------------------
//  LINKED LIST FUNCTIONS

// Gets the likedlist length
int listLength();

// Free memory allocated for the list
void freeListMemory();

//Get specified pid from the the linked list
int getListPid_1(int pid, char list[1024][128]);

//display the entire list
void printList_pid();

//insert pids at the first location of the list
void insertPidList(int clientfp, int pid, int memoryUsage, char file_args[]);

//find a link with given pid
struct node_pid *findPid(int pid);

#endif //FUNCTIONS