/*#################################################################################################################

    Written by Fernando Barbosa Silva - n10338471
    October, 2020

/#################################################################################################################*/

#include "Declarations.h"

#define MAX_NUM_CONNECTIONS 30
#define MESSAGE_01 "Could not connect to overseer at %s %s\n"
#define MESSAGE_02 "attempt to execute"
#define MESSAGE_03 "could not execute"
#define MESSAGE_04 "has terminated with status code"
#define MESSAGE_05 "has been executed with pid"
#define MESSAGE_06 "Usage: controller <address> <port> {[-o out_file] [-log log_file] [-t seconds] <file> [arg...] | mem [pid] | memkill <percent>}"
#define MESSAGE_07 "sent SIGTERM to"
#define MESSAGE_08 "has terminated with status code"
#define MESSAGE_09 "sent SIGKILL to"
#define BUFFER_SIZE 1024
#define LSIZ 512
#define RSIZ 50
#define PID_PO0L_SIZE 5
#define PID_INT_SIZE 8

struct node_pid *head_pid = NULL;
struct node_pid *current_pid = NULL;

/*#################################################################################################################

    FUNCTIONS USED BY THE CONTROLER AND THE OVERSEER

/#################################################################################################################*/

//-----------------------------------------------------------------------------------------------------------------
// Check if data entered in string format can be tranformed into integer value.
// returns 1 if string *number contains no valid numbers
// returns 0 if string *number contains valid number
//-----------------------------------------------------------------------------------------------------------------
int isNumber(char *str)
{
    int count = 0;
    if (str != NULL)
    {
        for (int x = 0; x < strlen(str); x++)
        {
            if (x == 0 && str[x] == '.')
            {
                return 1;
            }
            else if (str[x] == '.')
            {
                count++;
                if (count > 1)
                {
                    return 1;
                }
            }
            else if (isdigit(str[x]) == 0)
            {
                return 1;
            }
        }
        return 0;
    }
    return 1;
}
//-----------------------------------------------------------------------------------------------------------------
// Transform string to a array of string (using the space as a separator),
// uses array poiter to return the atrings
//-----------------------------------------------------------------------------------------------------------------
void stringToArgv(char *str, char *argvs[])
{
    char **ptr = argvs;
    char text[512];
    strcpy(text, str);
    int index = 0;
    const char s[2] = " ";
    char *token;
    token = strtok(text, s);
    while (token != NULL)
    {
        ptr[index] = token;
        index++;
        token = strtok(NULL, s);
    }
}

//-----------------------------------------------------------------------------------------------------------------
// Transform a array of argument in a string, return the string using pointer (char *str_out)
//-----------------------------------------------------------------------------------------------------------------
void argvToString(int argc, char *argv[], char *str_out)
{
    char str[BUFFER_SIZE];
    for (int x = 0; x < argc; x++)
    {
        if (x == 0)
        {
            strcpy(str, argv[x]);
        }
        else
        {
            strcat(str, " ");
            strcat(str, argv[x]);
        }
    }
    strcpy(str_out, str);
}

//-----------------------------------------------------------------------------------------------------------------
// Count arguments in a String (each word separated by space) and return i
//-----------------------------------------------------------------------------------------------------------------
int countArguments(char str[])
{
    char text[1024];
    strcpy(text, str);
    int count = 0;
    const char s[2] = " ";
    char *token;
    /* get the first token */
    token = strtok(text, s);
    /* walk through other tokens */
    while (token != NULL)
    {
        count++;
        token = strtok(NULL, s);
    }
    return count;
}

//-----------------------------------------------------------------------------------------------------------------
// Chech if glag -t is in the arguments and is yes, check if the next argument is a integer.
// Return the t value if it is a valid number (greater than or equal 0),
// Return -1 if -t flag was found but value is not a intenger
// Return -2 if -t flag was not found
//-----------------------------------------------------------------------------------------------------------------
int checkTFlag(char str_in[])
{
    int argc;
    char str[1024];
    strcpy(str, str_in);
    char *argv[1024];
    stringToArgv(str, argv);
    argc = countArguments(str);
    for (int x = 0; x < argc; x++)
    {
        int result = strcmp("-t", argv[x]);
        if (result == 0)
        {
            if (x == argc - 1)
            {
                return 1;
            }
            else
            {
                if (isNumber(argv[x + 1]) == 0)
                {
                    int num = atoi(argv[x + 1]);
                    //printf("Return: %d\n",num);  // Debug code
                    if (num >= 0)
                    {
                        return atoi(argv[x + 1]);
                    }
                    else
                    {
                        return -1;
                    }
                }
                else
                {
                    return -1;
                }
            }
        }
    }
    return -2;
}

//------------------------------------------------------------------------------------------------------------
// Chech if glag -o flag is in the arguments , if yes return the name o the file.
// Return 1 and dave the file in the pointer *str_out
// Return -1 if -t flag was found thare is no filename after the fla
// Return 0 if flag was not found
//------------------------------------------------------------------------------------------------------------
int checkFlag(char flag[], char *str_in, char *str_out)
{
    int argc = countArguments(str_in);
    char *argv[1024];
    stringToArgv(str_in, argv);
    argc = countArguments(str_in);
    for (int x = 0; x < argc; x++)
    {
        int result = strcmp(flag, argv[x]);
        if (result == 0)
        {
            if (x == argc - 1)
            {
                // No file after flag
                return -1;
            }
            else
            {
                // Save file name in str_out
                if (str_out != NULL)
                {
                    strcpy(str_out, argv[x + 1]);
                    return 1;
                }
                return 1;
            }
        }
    }
    // Flag was not fould
    return 0;
}

//-----------------------------------------------------------------------------------------------------------------
// Print the messages passed with the date and time, can use NULL if just want to print on or two string
//-----------------------------------------------------------------------------------------------------------------
int logDateTime(char msg1[], char msg2[], char msg3[])
{
    struct tm *ptr;
    time_t t;
    char str[30];
    t = time(NULL);
    ptr = localtime(&t);
    strftime(str, 100, "%x %H:%M:%S", ptr);
    if (msg1 != NULL && msg2 != NULL && msg3 != NULL)
    {
        printf("%s - %s %s %s\n", str, msg1, msg2, msg3);
        return 0;
    }
    else if (msg1 != NULL && msg2 != NULL)
    {
        printf("%s - %s %s\n", str, msg1, msg2);
        return 0;
    }
    else if (msg1 != NULL)
    {
        printf("%s - %s\n", str, msg1);
        return 0;
    }
    else
    {
        return 1;
    }
}

//-----------------------------------------------------------------------------------------------------------------
// Get Date and time in string format, return the string using a pointer (char *time_str)
//-----------------------------------------------------------------------------------------------------------------
void getDateTimeStr(char *time_str)
{
    struct tm *ptr;
    time_t t;
    char str[100];
    t = time(NULL);
    ptr = localtime(&t);
    strftime(str, 100, "%x %H:%M:%S", ptr);
    strcpy(time_str, str);
}

//-----------------------------------------------------------------------------------------------------------------
// Gets the machine IP address and return in a format string using a pointer
//-----------------------------------------------------------------------------------------------------------------
void getHostIp(char **ip)
{
    char hostbuffer[256];
    char *IPbuffer;
    struct hostent *host_entry;
    int hostname;

    // To retrieve hostname
    hostname = gethostname(hostbuffer, sizeof(hostbuffer));
    if (hostname == -1)
    {
        perror("gethostname()");
        exit(1);
    }
    // To retrieve host information
    host_entry = gethostbyname(hostbuffer);
    // To convert an Internet network address into ASCII string
    IPbuffer = inet_ntoa(*((struct in_addr *)host_entry->h_addr_list[0]));
    *ip = IPbuffer;
}

//-----------------------------------------------------------------------------------------------------------------
// Print message using stdout
//-----------------------------------------------------------------------------------------------------------------
void printStdout(char message[])
{
    printf("%s\n", message);
    fflush(stdout);
}

//-----------------------------------------------------------------------------------------------------------------
// Print message using stderror
//-----------------------------------------------------------------------------------------------------------------
void printStderror(char message[])
{
    fprintf(stderr, "%s\n", message);
}

//-----------------------------------------------------------------------------------------------------------------
// Used to send message using a socke file descriptor as a parameter
//-----------------------------------------------------------------------------------------------------------------
void sendMessage(int file_descriptor, const char *message)
{
    int message_length = strlen(message);
    uint32_t net_length = htonl(message_length);
    send(file_descriptor, &net_length, sizeof(net_length), 0);
    if (send(file_descriptor, message, message_length, 0) != message_length)
    {
        fprintf(stderr, "Send did not send all data to the server\n");
        exit(1);
    }
}

//-----------------------------------------------------------------------------------------------------------------
// Validates arguments passed by the user in the controller
//-----------------------------------------------------------------------------------------------------------------
int validateArguments(int argc, char *argv[])
{
    // Check if first argument is --help
    char str[1024];
    argvToString(argc, argv, str);

    //int has_memkill = checkFlag("")
    if (argc == 1)
    {
        printStderror(MESSAGE_06);
        return 1;
    }
    int result = strcmp("--help", argv[1]);
    if (result == 0)
    {
        printStdout(MESSAGE_06);
        return 1;
    }
    // Check if there are more than 3 arguments
    else if (argc < 3)
    {
        printStderror(MESSAGE_06);
        return 1;
    }
    // Check if the port number is valid (is all digits)
    else if (isNumber(argv[2]) == 1)
    {
        printStderror(MESSAGE_06);
        return 1;
    }
    // Check if argument -o and -log is in order
    else if (argc > 5)
    {
        if (strcmp("-log", argv[3]) == 0 && strcmp("-o", argv[5]) == 0)
        {
            printStderror(MESSAGE_06);
            return 1;
        }

        if ((strcmp("-t", argv[3]) == 0) && (strcmp("-o", argv[5]) == 0 || strcmp("-log", argv[5]) == 0))
        {
            printStderror(MESSAGE_06);
            return 1;
        }
    }
    else if (argc > 7)
    {

        if ((strcmp("-t", argv[5]) == 0) && (strcmp("-o", argv[7]) == 0 || strcmp("-log", argv[7]) == 0))
        {
            printStderror(MESSAGE_06);
            return 1;
        }
    }
    // Check if flag '-t' is in order and is valid
    int result_t_flag = checkTFlag(str);
    if (result_t_flag == -1)
    {
        printStderror(MESSAGE_06);
        return 1;
    }

    // Check if flag 'mem' is in order and is valid
    int result_mem = checkFlag("mem", str, NULL);
    if (result_mem == 1)
    {
        int is_number = isNumber(argv[argc - 1]);
        if (is_number == 1 || argc > 5)
        {
            printStderror(MESSAGE_06);
            return 1;
        }
    }
    if (result_mem == -1)
    {
        if (argc > 5)
        {
            printStderror(MESSAGE_06);
            return 1;
        }
    }

    // Check if flag 'memkill' is in order and is valid
    int result_memkill = checkFlag("memkill", str, NULL);
    if (result_memkill == -1)
    {
        printStderror(MESSAGE_06);
        return 1;
    }
    if (result_memkill == 1)
    {
        int is_number = isNumber(argv[argc - 1]);
        if (is_number == 1)
        {
            printStderror(MESSAGE_06);
            return 1;
        }
    }
    return 0;
}

//-----------------------------------------------------------------------------------------------------------------
// Receive message and validate if the entire message was received
//-----------------------------------------------------------------------------------------------------------------
char *recvMessage(int fd)
{
    char *msg;
    uint32_t netLen;
    int recvLen = recv(fd, &netLen, sizeof(netLen), 0);
    if (recvLen != sizeof(netLen))
    {
        fprintf(stderr, "recv got invalid length value (got %d)\n", recvLen);
        exit(1);
    }
    int len = ntohl(netLen);
    msg = malloc(len + 1);
    if (recv(fd, msg, len, 0) != len)
    {
        fprintf(stderr, "recv got invalid length msg\n");
        exit(1);
    }
    msg[len] = '\0';
    return msg;
}

//-----------------------------------------------------------------------------------------------------------------
// Set the output in the overseer if flags '-o = 3 or' '-log = 4' was passed by the controller
//-----------------------------------------------------------------------------------------------------------------
int setOutput(int std_output, char fileName1[])
{
    if (std_output == 3)
    {
        int o_fd = open(fileName1, O_CREAT | O_WRONLY | O_APPEND, 0777);
        if (o_fd == -1)
        {
            perror("Open output file '-o' failed.");
            exit(1);
        }
        dup2(o_fd, STDOUT_FILENO);
        close(o_fd);
        return 3;
    }
    else if (std_output == 4)
    {
        //printf("Std: %d  - File: %s\n", std_output, fileName1);
        int log_fd = open(fileName1, O_CREAT | O_WRONLY | O_APPEND, 0777);
        if (log_fd == -1)
        {
            perror("Open output file '-log' failed.");
            exit(1);
        }
        dup2(log_fd, STDOUT_FILENO);
        close(log_fd);
        return 4;
    }
    return 0;
}
//------------------------------------------------------------------------------------------------------------
// Functions to monitor the number of process running in the server (MAX 5 as defined in the requirements)
//------------------------------------------------------------------------------------------------------------

int isInPidPool(pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE], pid_t pid_id)
{
    for (int x = 0; x < PID_PO0L_SIZE; x++)
    {
        if (pid_pool[x][0] == pid_id)
        {
            return 1;
        }
    }
    return 0;
}

// Add PID in the pool if it not already there
int addInPidPool(pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE], pid_t pid_id)
{
    if (isInPidPool(pid_pool, pid_id) == 0)
    {
        for (int x = 0; x < PID_PO0L_SIZE; x++)
        {
            if (pid_pool[x][0] == -1)
            {
                pid_pool[x][0] = pid_id;
                return 1;
            }
        }
    }
    return 0;
}

// Remove PID from the pool
int removeFromPidPool(pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE], pid_t pid_id)
{
    if (isInPidPool(pid_pool, pid_id) == 1)
    {
        for (int x = 0; x < PID_PO0L_SIZE; x++)
        {
            if (*pid_pool[x] == pid_id)
            {
                pid_pool[x][0] = -1;
                return 1;
            }
        }
    }
    return 0;
}

void printPid(pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE])
{
    for (int x = 0; x < PID_PO0L_SIZE; x++)
    {
        //if(pid_pool[x][0] != -1){
        printf("%d ", pid_pool[x][0]);
        //}
    }
    printf("\n");
    fflush(stdout);
}

void setPidPool(pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE])
{
    for (int x = 0; x < PID_PO0L_SIZE; x++)
    {
        pid_pool[x][0] = -1;
    }
}

//------------------------------------------------------------------------------------------------------------
// Try to execute file indicated by the client. If error retur 1 otherwise return 0.
//------------------------------------------------------------------------------------------------------------
int executeFile(int clientfd, char path[], char arguments[], char path_argument[], int std_output,
                char o_f_name[], char log_f_name[], char time1[], int saved_stdout, int t,
                pthread_mutex_t mutex, pid_t pid_pool[128][8])
{
    int status;
    pid_t childID, endID;

    if ((childID = fork()) == -1)
    {
        perror("fork error");
        exit(EXIT_FAILURE);
    }
    else if (childID == 0)
    {

        pthread_mutex_lock(&mutex);
        if (std_output == 3 || std_output == 5)
            setOutput(3, o_f_name);
        pthread_mutex_unlock(&mutex);
        char *arg[128] = {};
        stringToArgv(arguments, arg);
        execv(path, arg);

        /* Log controller request in the server screen or in a file if -log flag 
           was send by the controlle, then reset output to server screen.*/
        pthread_mutex_lock(&mutex);
        dup2(saved_stdout, STDOUT_FILENO);
        if (std_output == 4 || std_output == 5)
            setOutput(4, log_f_name);
        logDateTime(MESSAGE_03, path_argument, NULL);
        dup2(saved_stdout, STDOUT_FILENO);
        pthread_mutex_unlock(&mutex);
        exit(EXIT_FAILURE);
    }
    else
    {
        // While child process is running
        endID = waitpid(childID, &status, WNOHANG | WUNTRACED);
        //dup2(saved_stdout, STDOUT_FILENO);   *** Testar se tem imactio ***
        int count = 0;
        int sigterm_status = 0;
        int sigkill_status = 0;
        while (endID == 0)
        {

            //addInPidPool(pid_pool, childID);

            pthread_mutex_lock(&mutex);
            if (count == 0)
            {
                addInPidPool(pid_pool, childID);
            }
            long long int memoryUsage = getProcessMemoryUsage(childID);
            insertPidList(clientfd, childID, memoryUsage, path_argument);
            pthread_mutex_unlock(&mutex);
            sleep(1);
            count++;

            if ((count == t) && (sigterm_status == 0))
            {
                pthread_mutex_lock(&mutex);
                kill(childID, SIGTERM);
                dup2(saved_stdout, STDOUT_FILENO);
                if (std_output == 4 || std_output == 5)
                    setOutput(4, log_f_name);
                char time2[100];
                getDateTimeStr(time2);
                printf("%s %s %d\n", time2, MESSAGE_07, childID);
                fflush(stdout);
                dup2(saved_stdout, STDOUT_FILENO);
                sigterm_status = 1;
                count = 0;
                pthread_mutex_unlock(&mutex);
            }
            if ((count == 5) && (sigterm_status == 1) && (sigkill_status == 0))
            {
                pthread_mutex_lock(&mutex);
                kill(childID, SIGKILL);
                dup2(saved_stdout, STDOUT_FILENO);
                if (std_output == 4 || std_output == 5)
                    setOutput(4, log_f_name);
                char time2[100];
                getDateTimeStr(time2);
                printf("%s %s %d\n", time2, MESSAGE_09, childID);
                fflush(stdout);
                dup2(saved_stdout, STDOUT_FILENO);
                sigkill_status = 1;
                pthread_mutex_unlock(&mutex);
            }

            endID = waitpid(childID, &status, WNOHANG | WUNTRACED);
            /* check for error calling waitpid */
            if (endID == -1)
            {
                perror("waitpid error");
                exit(EXIT_FAILURE);
                return 1;
            }
            else if (endID == childID)
            {
                int print_status = 0;
                // Check status of the child process when it ends
                int exit_status = WEXITSTATUS(status);
                if (exit_status != 1 && sigterm_status == 0 && sigkill_status == 0)
                {
                    pthread_mutex_lock(&mutex);
                    dup2(saved_stdout, STDOUT_FILENO);
                    if (std_output == 4 || std_output == 5)
                        setOutput(4, log_f_name);
                    printf("%s %s %s %d\n", time1, path_argument, MESSAGE_05, childID);
                    fflush(stdout);
                    char time2[100];
                    getDateTimeStr(time2);
                    printf("%s %d %s %d\n", time2, childID, MESSAGE_04, exit_status);
                    fflush(stdout);
                    dup2(saved_stdout, STDOUT_FILENO);
                    removeFromPidPool(pid_pool, childID);
                    print_status = 1;
                    pthread_mutex_unlock(&mutex);
                }

                // Check for error if child process does not terminate propriately
                if (WIFEXITED(status))
                {
                    //Child ended normally
                    pthread_mutex_lock(&mutex);
                    removeFromPidPool(pid_pool, childID);
                    pthread_mutex_unlock(&mutex);
                    return 0;
                }
                else if (WIFSIGNALED(status))
                {
                    // Child process ended because of a signal
                    pthread_mutex_lock(&mutex);
                    if (print_status == 0 && WIFSIGNALED(status))
                    {
                        dup2(saved_stdout, STDOUT_FILENO);
                        if (std_output == 4 || std_output == 5)
                            setOutput(4, log_f_name);
                        char time2[100];
                        getDateTimeStr(time2);
                        printf("%s %d %s %d\n", time2, childID, MESSAGE_08, exit_status);
                        fflush(stdout);
                        dup2(saved_stdout, STDOUT_FILENO);
                        removeFromPidPool(pid_pool, childID);
                    }
                    pthread_mutex_unlock(&mutex);
                    return 1;
                }
                else if (WIFSTOPPED(status))
                {
                    printf("Child process has stopped\n");
                    return 1;
                }
                exit(EXIT_SUCCESS);
            }
        }
        return 0;
    }
}

//-----------------------------------------------------------------------------------------------------------------
// Validate port number passed by the user (check if it is a valid integer)
//-----------------------------------------------------------------------------------------------------------------
void overseerArgumentsValidation(int isNumber, int argc)
{
    if (argc == 1)
    {
        printf("Please enter a port number - Example: ./overseer 12345\n");
        exit(1);
    }
    else if (isNumber == 1)
    {
        printf("Please enter a valid port number - Example: ./overseer 12345\n");
        exit(1);
    }
    else if (argc > 2)
    {
        printf("Overseer accepts just one argument (Port number) - Example: ./overseer 12345\n");
        exit(1);
    }
}
//-----------------------------------------------------------------------------------------------------------------
// Build a string with a specific start and finish index (using the space as separator)
//-----------------------------------------------------------------------------------------------------------------
void buildString(char str_in[], char *str_out, int index_start, int index_finish)
{
    char text[1024];
    strcpy(text, str_in);
    char result[1024];
    int index = 0;
    const char s[2] = " ";
    char *token;
    /* get the first token */
    token = strtok(text, s);

    /* walk through other tokens */
    while (token != NULL)
    {
        if (index == index_start)
        {
            strcpy(result, token);
        }
        else if (index > index_start && index < index_finish + 1)
        {
            strcat(result, " ");
            strcat(result, token);
        }
        index++;
        token = strtok(NULL, s);
    }
    strcpy(str_out, result);
    free(token);
}
//-----------------------------------------------------------------------------------------------------------------
// Kill all process em close the overseer
//-----------------------------------------------------------------------------------------------------------------
int killAllProcess(pid_t pid, pthread_mutex_t mutex)
{
    int status;
    pid_t childID;
    if ((childID = fork()) == -1)
    {
        perror("fork error");
        exit(EXIT_FAILURE);
    }
    else if (childID == 0)
    {
        pthread_mutex_lock(&mutex);
        int exit_status = WEXITSTATUS(status);
        char time2[100];
        getDateTimeStr(time2);
        printf("%s %d %s %d\n", time2, getpid(), MESSAGE_08, exit_status);
        kill(pid, SIGTERM);
        sleep(2);
        kill(pid, SIGKILL);
        pthread_mutex_unlock(&mutex);
        exit(EXIT_FAILURE);
    }
    else
    {
        wait(NULL);
        return 0;
    }
    return 0;
}

//-----------------------------------------------------------------------------------------------------------------
// Calculate the memory used by a process usig as parameter the pro/maps file. Return the value as a integer.
//-----------------------------------------------------------------------------------------------------------------
int calcMemory(char *str)
{
    char startMemory[20] = "";
    char endMemory[20] = "";
    char text[1024];
    strcpy(text, str);
    int index = 0;
    const char s[2] = "-";
    char *token;
    token = strtok(text, s);
    while (token != NULL)
    {
        if (index == 0)
        {
            strcat(startMemory, token);
        }
        if (index == 1)
        {
            strcat(endMemory, token);
        }
        index++;
        token = strtok(NULL, s);
    }
    int memStart = (int)strtol(startMemory, NULL, 16);
    int memEnd = (int)strtol(endMemory, NULL, 16);
    return memEnd - memStart;
}

//-----------------------------------------------------------------------------------------------------------------
// Gets the process memory usage by the pid specified, return the value as long long int in bytes
//-----------------------------------------------------------------------------------------------------------------
long long int getProcessMemoryUsage(int pid)
{
    char line[64][512];
    char str_pid[6];
    sprintf(str_pid, "%d", pid);
    int numLines = 0;
    int totalMemoryUsage = 0;
    char filePath[128] = "/proc/";
    strcat(filePath, str_pid);
    strcat(filePath, "/maps");

    FILE *file_read = fopen(filePath, "r");
    if (file_read == NULL)
    {
        perror("File does not exist!\n");
    }
    while (fgets(line[numLines], LSIZ, file_read))
    {
        line[numLines][strlen(line[numLines]) - 1] = '\0';
        numLines++;
    }
    char *arguments[100] = {};
    for (int i = 0; i < numLines; i++)
    {
        stringToArgv(line[i], arguments);
        int result1 = strcmp(arguments[4], "0");
        int result2 = strcmp(arguments[5], "[heap]");
        if (result1 == 0 && result2 == 0)
        {
            int result = calcMemory(arguments[0]);
            totalMemoryUsage += result;
        }
    }
    pclose(file_read);
    return totalMemoryUsage;
}

//-----------------------------------------------------------------------------------------------------------------
// Get the local server total memory and return it as a lon lon int in bytes.
//-----------------------------------------------------------------------------------------------------------------
long long int getTotalMemory()
{
    char line[64][512];
    int numLines = 0;
    long long int totalMemory = 0;

    FILE *file_read = fopen("/proc/meminfo", "r");
    if (file_read == NULL)
    {
        perror("File does not exist!\n");
    }
    while (fgets(line[numLines], LSIZ, file_read))
    {
        line[numLines][strlen(line[numLines]) - 1] = '\0';
        numLines++;
    }
    char *arguments[10] = {};
    for (int i = 0; i < numLines; i++)
    {
        stringToArgv(line[i], arguments);
        int result1 = strcmp(arguments[0], "MemTotal:");
        if (result1 == 0)
        {
            totalMemory = atoi(arguments[1]);
        }
    }
    totalMemory = totalMemory * 1000;
    pclose(file_read);
    return totalMemory;
}

//-----------------------------------------------------------------------------------------------------------------
//  LINKED LIST FUNCTIONS
//-----------------------------------------------------------------------------------------------------------------

// Gets the likedlist length
int listLength()
{
    int length = 0;
    struct node_pid *current_pid;
    for (current_pid = head_pid; current_pid != NULL; current_pid = current_pid->next)
    {
        length++;
    }
    return length;
}

// Free memory allocated for the list
void freeListMemory()
{
    struct node_pid *temp = head_pid;
    while (head_pid != NULL)
    {
        temp = head_pid;
        head_pid = head_pid->next;
        free(temp);
    }
}

//Get specified pid from the the linked list
int getListPid_1(int pid, char list[1024][128])
{
    struct node_pid *ptr = head_pid;
    int count = 0;
    //start from the beginning
    while (ptr != NULL)
    {
        if (ptr->pid == pid)
        {
            char bytes[128];
            sprintf(bytes, "%d", ptr->memoryUsage);
            char date[128];
            strcpy(date, ptr->time);
            char str[512];
            strcpy(str, date);
            strcat(str, " ");
            strcat(str, bytes);
            strcat(str, "\n");
            // Add string in the list
            strcpy(list[count], str);
            count++;
        }
        ptr = ptr->next;
    }
    return count;
}

//display the entire list
void printList_pid()
{
    struct node_pid *ptr = head_pid;
    //start from the beginning
    while (ptr != NULL)
    {
        printf("%s %d \n", ptr->time, ptr->memoryUsage);
        fflush(stdout);
        ptr = ptr->next;
    }
}

//insert pids at the first location of the list
void insertPidList(int clientfp, int pid, int memoryUsage, char file_args[])
{
    char time_str[256];
    struct tm *ptr;
    time_t t;
    char str[100];
    t = time(NULL);
    ptr = localtime(&t);
    strftime(str, 100, "%Y-%m-%d %H:%M:%S", ptr);
    strcpy(time_str, str);

    time_t now = time(NULL);
    if (now == -1)
    {
        puts("The time() function failed");
    }
    //create a link
    struct node_pid *link = (struct node_pid *)malloc(sizeof(struct node_pid));
    link->clientfd = clientfp;
    link->pid = pid;
    strcpy(link->time, time_str);
    link->memoryUsage = memoryUsage;
    link->file_args = file_args;
    link->status = 1;
    //point it to old first node_pid
    link->next = head_pid;
    //point first to new first node_pid
    head_pid = link;
}

//find a link with given pid
struct node_pid *findPid(int pid)
{
    //start from the first link
    struct node_pid *current_pid = head_pid;
    //if list is empty
    if (head_pid == NULL)
    {
        return NULL;
    }
    //navigate through list
    while (current_pid->pid != pid)
    {
        //if it is last node_pid
        if (current_pid->next == NULL)
        {
            return NULL;
        }
        else
        {
            //go to next link
            current_pid = current_pid->next;
        }
    }
    //if pid found, return the current_pid Link
    return current_pid;
}
