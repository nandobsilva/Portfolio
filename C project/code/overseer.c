
/*#################################################################################################################

    Written by Fernando Barbosa Silva - n10338471
    October, 2020

/#################################################################################################################*/

#include "Declarations.h"

#define BUFFER_SIZE 1024
#define MAX_NUM_CONNECTIONS 100
#define MESSAGE_01 "connection received from"
#define MESSAGE_02 "attempt to execute"
#define MESSAGE_03 "could not execute"
#define MESSAGE_04 "received SIGINT"
#define MESSAGE_05 "Cleaning up and terminating"
#define MESSAGE_06 "hasterminated with a status code"
#define MESSAGE_07 "sent KILL to "
#define THREAD_POOL_SIZE 5
#define PID_PO0L_SIZE 5
#define PID_INT_SIZE 8
#define T_SIG 10;

//-----------------------------------------------------------------------------------------------------------------
// Global variables
//-----------------------------------------------------------------------------------------------------------------
pthread_t thread_pool[THREAD_POOL_SIZE];
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_variable = PTHREAD_COND_INITIALIZER;
pid_t pid_pool[PID_PO0L_SIZE][PID_INT_SIZE];
int clientfp_pool[MAX_NUM_CONNECTIONS][16];
char message_pool[MAX_NUM_CONNECTIONS][2048];
int server_status = 1;
int index_count = 0;

//-----------------------------------------------------------------------------------------------------------------
// Functions declaration
//-----------------------------------------------------------------------------------------------------------------
void *execute_connection(void *ptr_clientfd, void *msg);
void *execute_connection_test(void *ptr_clientfd);
void *thread_function(void *arg);
void sigintHandler(int sig_num);
void setPools();
int isInPool(int clientfd);
int hasClientfd();
int addInPool(int clientfd, char message[]);
void printPool();
int removeFromPool(int clientfd);

/*#################################################################################################################

    Start the server end star listening for requests

/#################################################################################################################*/

int main(int argc, char *argv[])
{
    // Total memory available in the overseer
    long long const int totalMemory = getTotalMemory();

    // Signal handler
    signal(SIGINT, sigintHandler);

    // Set pid Array
    setPidPool(pid_pool);
    setPools(clientfp_pool);

    //printPool(); //// DEBUG

    // Validate port number passed by the user
    overseerArgumentsValidation(isNumber(argv[1]), argc);
    int port_number = atoi(argv[1]);
    printf("Server is online on port: %d\n", port_number);

    // Create the threads which will handle the request
    for (int x = 0; x < THREAD_POOL_SIZE; x++)
    {
        pthread_create(&thread_pool[x], NULL, thread_function, NULL);
    }

    // Create communication socket
    int file_descriptor = socket(AF_INET, SOCK_STREAM, 0);
    if (file_descriptor == -1)
    {
        perror("socket()");
        return 1;
    }

    // Reuse the same socket (port) if the server terminates
    int opt_enable = 1;
    setsockopt(file_descriptor, SOL_SOCKET, SO_REUSEADDR, &opt_enable, sizeof(opt_enable));
    setsockopt(file_descriptor, SOL_SOCKET, SO_REUSEPORT, &opt_enable, sizeof(opt_enable));

    // Communication socket setup
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(atoi(argv[1]));
    if (bind(file_descriptor, (struct sockaddr *)&addr, sizeof(addr)) == -1)
    {
        perror("bind()");
    }
    if (listen(file_descriptor, MAX_NUM_CONNECTIONS) == -1)
    {
        perror("listen()");
        return 1;
    }
    struct sockaddr clientaddr;
    socklen_t clientaddr_len;

    // Listening for requests from the controller
    while (server_status == 1)
    {
        // Server accepts a connection requested from a client
        int clientfd = 0;
        clientfd = accept(file_descriptor, &clientaddr, &clientaddr_len);
        if (clientfd == -1)
        {
            perror("accept()");
            return 1;
        }
        char message[BUFFER_SIZE];
        char ip[256];
        char *msg = recvMessage(clientfd);
        strcpy(message, msg);
        free(msg);
        int num_arg = countArguments(message);

        // Log controller request in the server screen
        buildString(message, ip, 0, 0);
        logDateTime(MESSAGE_01, ip, NULL);

        // Check if there are flags mem, mem <pid> or memkill and respond to it
        int has_mem_flag = checkFlag("mem", message, NULL);
        int has_memKill_flag = checkFlag("memkill", message, NULL);

        // If get requests to runn some application
        if (has_mem_flag == 0 && has_memKill_flag == 0)
        {
            pthread_mutex_lock(&mutex);
            addInPool(clientfd, message);
            pthread_mutex_unlock(&mutex);
            enqueue(0, "NULL");
            pthread_cond_signal(&cond_variable);
        }
        // If controller request memory usage list from pid: <%d>
        else if (has_mem_flag == 1)
        {
            char list[1000000];
            char str_pid[16];
            buildString(message, str_pid, num_arg - 1, num_arg - 1);
            int pid = atoi(str_pid);

            char pid_list[1024][128] = {};
            int num = getListPid_1(pid, pid_list);
            if (num > 0)
            {
                for (int x = num; x > 0; x--)
                {
                    if (x == num)
                    {
                        strcpy(list, pid_list[x]);
                    }
                    else
                    {
                        strcat(list, pid_list[x]);
                    }
                }
                sendMessage(clientfd, list);
            }
            else
            {
                sendMessage(clientfd, "PID not found.\n");
            }
            if (shutdown(clientfd, SHUT_RDWR) == -1)
            {
                perror("shutdown()");
            }
            close(clientfd);
        }

        // If the controle requested list of all running process.
        else if (has_mem_flag == -1)
        {
            char message_to_Send[5120];
            char *messgaNoProcess = "No process is running in the server\n";
            int countPids = 0;

            for (int x = 0; x < PID_PO0L_SIZE; x++)
            {
                //Build string from the child process struct
                if (*pid_pool[x] != -1)
                {
                    int pid = *pid_pool[x];
                    char str_pid[32];
                    sprintf(str_pid, "%d", pid);

                    long long int memory_usage = getProcessMemoryUsage(pid);
                    char str_mem_usage[128];
                    sprintf(str_mem_usage, "%lld", memory_usage);

                    float perc_usage = (float)memory_usage / (float)totalMemory;
                    char str_per_usage[16];
                    sprintf(str_per_usage, "%.2f", perc_usage);

                    struct node_pid *temp = findPid(pid);

                    char pid_message_line[1024];

                    // Build each string line to sent to the controller
                    strcpy(pid_message_line, str_pid);
                    strcat(pid_message_line, " ");
                    strcat(pid_message_line, str_mem_usage);
                    strcat(pid_message_line, " ");
                    strcat(pid_message_line, str_per_usage);
                    strcat(pid_message_line, "% ");
                    strcat(pid_message_line, temp->file_args);
                    strcat(pid_message_line, " ");
                    strcat(pid_message_line, "\n");
                    if (x == 0)
                    {
                        strcpy(message_to_Send, pid_message_line);
                    }
                    else
                    {
                        strcat(message_to_Send, pid_message_line);
                    }
                    countPids++;
                }
            }
            if (countPids == 0)
            {
                sendMessage(clientfd, messgaNoProcess);
            }
            else
            {
                sendMessage(clientfd, message_to_Send);
            }
            if (shutdown(clientfd, SHUT_RDWR) == -1)
            {
                perror("shutdown()");
            }
            close(clientfd);
        }
        // If controller request to kill process
        else if (has_memKill_flag == 1)
        {
            char *arguments[20] = {};
            stringToArgv(message, arguments);
            float limit = strtof(arguments[num_arg - 1], NULL);
            int count = 0;
            for (int x = 0; x < PID_PO0L_SIZE; x++)
            {
                if (*pid_pool[x] != -1)
                {
                    int pid = *pid_pool[x];
                    long long int memory_usage = getProcessMemoryUsage(pid);
                    float perc_mem_usage = (float)memory_usage / (float)totalMemory;

                    if (limit == 0)
                    {

                        char str_pid[50];
                        sprintf(str_pid, "%d", pid);
                        logDateTime(MESSAGE_07, str_pid, NULL);
                        kill(pid, SIGKILL);
                        removeFromPidPool(pid_pool, pid);
                        count++;
                    }
                    else if (perc_mem_usage > limit)
                    {
                        char str_pid[50];
                        sprintf(str_pid, "%d", pid);
                        logDateTime(MESSAGE_07, str_pid, NULL);
                        kill(pid, SIGKILL);
                        removeFromPidPool(pid_pool, pid);
                        count++;
                    }
                }
            }
            if (count == 0)
            {
                char message[512];
                strcpy(message, "Found no process over ");
                strcat(message, arguments[num_arg - 1]);
                strcat(message, "% to be killed\n");
                sendMessage(clientfd, message);
            }
            else
            {
                char message[512];
                strcpy(message, "All processess over the limit specified were killed\n");
                sendMessage(clientfd, message);
            }
            if (shutdown(clientfd, SHUT_RDWR) == -1)
            {
                perror("shutdown()");
            }
            close(clientfd);
        }
    }
    return 0;
}

/*#################################################################################################################

    Control the thread execution when there is a connection request

/#################################################################################################################*/

void *thread_function(void *arg)
{
    while (1)
    {
        pthread_mutex_lock(&mutex);
        int result = 0;
        int clientfp;
        char message[BUFFER_SIZE];
        if ((result = dequeue(&clientfp, message)) == -1)
        {
            pthread_cond_wait(&cond_variable, &mutex);
            result = dequeue(&clientfp, message);
        }
        pthread_mutex_unlock(&mutex);
        if (result != -1)
        {
            pthread_mutex_lock(&mutex);
            int index = hasClientfd();
            clientfp = *clientfp_pool[index];
            strcpy(message, message_pool[index]);
            removeFromPool(*clientfp_pool[index]);
            pthread_mutex_unlock(&mutex);
            execute_connection(&clientfp, message);
            close(clientfp);
        }
    }
    free(arg);
}

/*#################################################################################################################
                                                                                                                 
   Execute requests made by the controller                                                                                                        
   This function is executed by multiples threads and 
   it uses many methods from functions.c

/#################################################################################################################*/
void *execute_connection(void *ptr_clientfd, void *msg)
{
    // Save standard output copy to allow to reset it back
    int const saved_stdout = dup(STDOUT_FILENO);

    // Receive message from the controller and check the length of it
    int clientfd = *(int *)ptr_clientfd;
    int msg_len = BUFFER_SIZE;
    char message_request[msg_len];
    strcpy(message_request, msg);
    int num_arguments = countArguments(message_request);
    //int has_mem_flag = checkFlag("mem", message_request, NULL);
    //int has_memKill_flag = checkFlag("memkill", message_request, NULL);

    // Variables used in the client request process
    char file_path[msg_len];
    char path_arguments[msg_len];
    char arguments[msg_len];
    char o_file_name[msg_len];
    char log_file_name[msg_len];
    int std_output;
    int t = T_SIG;
    char o_flag = 'F';
    char log_flag = 'F';
    char t_flag = 'F';
    int index;

    // Check if fla -t is presented in the message, if yes it saves the number passed in 't'
    int num_t_flag = checkTFlag(message_request);
    if (num_t_flag >= 0)
    {
        t = num_t_flag;
        t_flag = 'T';
    }

    // Check if there are flags -o, -log or -t   and set variables vlaues
    int has_o_flag = checkFlag("-o", message_request, o_file_name);
    if (has_o_flag == 1)
    {
        o_flag = 'T';
    }
    int has_log_flag = checkFlag("-log", message_request, log_file_name);
    if (has_log_flag == 1)
    {
        log_flag = 'T';
    }
    // No flags
    if (o_flag == 'F' && log_flag == 'F' && t_flag == 'F')
    {
        index = 1;
        std_output = 1;
    }
    // All flags
    else if (o_flag == 'T' && log_flag == 'T' && t_flag == 'T')
    {
        index = 7;
        std_output = 5;
    }
    // Just flags -o and -log
    else if (o_flag == 'T' && log_flag == 'T')
    {
        index = 5;
        std_output = 5;
    }
    // Just flag -o and -t
    else if (o_flag == 'T' && t_flag == 'T')
    {
        index = 5;
        std_output = 3;
    }
    // Just flag -log and -t
    else if (log_flag == 'T' && t_flag == 'T')
    {
        index = 5;
        std_output = 4;
    }
    // Just flag -o
    else if (o_flag == 'T')
    {
        index = 3;
        std_output = 3;
    }
    // Just flag -log
    else if (log_flag == 'T')
    {
        index = 3;
        std_output = 4;
    }
    // Just flag -t
    else if (t_flag == 'T')
    {
        index = 3;
        std_output = 1;
    }

    // Set variables acoording with the number of flags passed by the controlle
    buildString(message_request, file_path, index, index);
    buildString(message_request, path_arguments, index, num_arguments);
    buildString(message_request, arguments, index, num_arguments);

    /* Log controller request in the server screen or in a file if -log flag 
    was send by the controlle, then reset output to server screen.*/
    pthread_mutex_lock(&mutex);

    dup2(saved_stdout, STDOUT_FILENO);

    if (std_output == 4 || std_output == 5)
        setOutput(4, log_file_name);

    logDateTime(MESSAGE_02, path_arguments, NULL);

    if (std_output == 4 || std_output == 5)
        dup2(saved_stdout, STDOUT_FILENO);

    pthread_mutex_unlock(&mutex);

    // Execute the file passed by the controller
    char time1[100];
    getDateTimeStr(time1);
    executeFile(clientfd, file_path, arguments, path_arguments, std_output, o_file_name, log_file_name,
                time1, saved_stdout, t, mutex, pid_pool);

    // Shutdown connection, close clientfd and reset stdout.
    if (shutdown(clientfd, SHUT_RDWR) == -1)
    {
        dup2(saved_stdout, STDOUT_FILENO);
        close(saved_stdout);
        return NULL;
    }
    dup2(saved_stdout, STDOUT_FILENO);
    close(saved_stdout);
    return NULL;
}

/*#################################################################################################################
    
    Signal Handler for Killing all the process and terminate the server
    
//#################################################################################################################*/
void sigintHandler(int sig_num)
{
    int pid = getpid();
    printf("\n");
    logDateTime(MESSAGE_04, NULL, NULL);
    fflush(stdout);
    logDateTime(MESSAGE_05, NULL, NULL);
    fflush(stdout);
    for (int x = 0; x < PID_PO0L_SIZE; x++)
    {
        if (*pid_pool[x] != -1)
        {
            kill(*pid_pool[x], SIGKILL);
        }
    }
    freeListMemory();
    freeQueueMemory();
    killAllProcess(pid, mutex);
}

/*#################################################################################################################
    
    FUNCTION TO CONTROL THE REQUESTS MADE BY THE CONTROLLER
    
//#################################################################################################################*/

// Set up the request pool
void setPools()
{
    for (int x = 0; x < MAX_NUM_CONNECTIONS; x++)
    {
        clientfp_pool[x][0] = -1;
        strcpy(message_pool[x], "-1");
    }
}

// Che if a request is alread in the resques pool
int isInPool(int clientfd)
{
    for (int x = 0; x < MAX_NUM_CONNECTIONS; x++)
    {
        if (clientfp_pool[x][0] == clientfd)
        {
            return x; // Client fd is in the pool
        }
    }
    return -1;
}

// Check if there is requet to be executed
int hasClientfd()
{
    for (int i = 0; i < MAX_NUM_CONNECTIONS; i++)
    {
        if (clientfp_pool[i][0] != -1)
        {
            return i; // Index in the pool where there is a clientfd to be executed
        }
    }
    return -1;
}

// Add request in the pool to be executed
int addInPool(int clientfd, char message[])
{
    int result = isInPool(clientfd);

    if (result == -1) // clientfd is not in the poll
    {
        clientfp_pool[index_count][0] = clientfd;
        strcpy(message_pool[index_count], message);
        index_count++;
        if (index_count == 99)
        {
            index_count = 0;
        }
        return index_count;
    }
    return -1;
}

// Show all the resquests made by the controller that was not executed yet.
void printPool()
{
    printf("\n\n+++++++++++++++++++++++++++  CLIENT REQUEST LIST +++++++++++++++++++++++++++++++++++++\n");
    for (int x = 0; x < MAX_NUM_CONNECTIONS; x++)
    {
        if (*clientfp_pool[x] != -1)
        {
            printf("| %d |Clientfd: %.2d  |  Message : %s\n", x, *clientfp_pool[x], message_pool[x]);
        }
    }
    printf("\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n");
}
// Remove request executed from the pool
int removeFromPool(int clientfd)
{
    for (int x = 0; x < MAX_NUM_CONNECTIONS; x++)
    {
        if (*clientfp_pool[x] == clientfd)
        {
            clientfp_pool[x][0] = -1;
            strcpy(message_pool[x], "-1");
            return x;
        }
    }
    return -1;
}
