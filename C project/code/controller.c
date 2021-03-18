/*#################################################################################################################

    Written by Fernando Barbosa Silva - n10338471
    October, 2020

/#################################################################################################################*/

#include "Declarations.h"
#define BUFFER_SIZE 1024
#define MESSAGE_01 "Could not connect to overseer at %s %s\n"

/*#################################################################################################################

    Start the controller and send the message to the server

/#################################################################################################################*/
int main(int argc, char *argv[])
{

    // Chech if arguments entered by the user are valid if is not terminate controller
    int result = validateArguments(argc, argv);
    if (result == 1)
    {
        return 1;
    }

    // Get host Ip address to send to the server
    char *host_ip = NULL;
    getHostIp(&host_ip);

    // Build message to send data to the server
    char message[BUFFER_SIZE];
    strcpy(message, host_ip);
    for (int x = 3; x < argc; x++)
    {
        strcat(message, " ");
        strcat(message, argv[x]);
    }

    // Create socket connection
    int file_descriptor = socket(AF_INET, SOCK_STREAM, 0);
    if (file_descriptor == -1)
    {
        return 1;
    }

    // Code to get server ip address
    struct addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = 0;
    hints.ai_flags = 0;
    struct addrinfo *addresses = NULL;

    // Check if the server IP entered is valid
    if (getaddrinfo(argv[1], NULL, &hints, &addresses) != 0)
    {
        fprintf(stderr, MESSAGE_01, argv[1], argv[2]);
        return 1;
    }

    struct addrinfo *address = addresses;
    if (address == NULL)
    {
        fprintf(stderr, MESSAGE_01, argv[1], argv[2]);
        return 1;
    }

    freeaddrinfo(addresses);

    char ip_address[32];
    for (int x = 0; x < 1; x++)
    {
        struct sockaddr_in *sockaddress = (struct sockaddr_in *)address->ai_addr;
        inet_ntop(AF_INET, &sockaddress->sin_addr, ip_address, sizeof(ip_address));
    }

    struct sockaddr_in addr = *((struct sockaddr_in *)(address->ai_addr));
    addr.sin_port = htons(atoi(argv[2]));

    // Connect to the server
    if (connect(file_descriptor, (struct sockaddr *)&addr, sizeof(addr)) == -1)
    {
        fprintf(stderr, MESSAGE_01, argv[1], argv[2]);
        exit(1);
    }

    // Send message to the server
    sendMessage(file_descriptor, message);

    // Check if there are flags mem,mem <pid>
    int has_mem_flag = checkFlag("mem", message, NULL);
    int has_memkill_flag = checkFlag("memkill", message, NULL);
    if (has_mem_flag == 1)
    {
        printf("%s", recvMessage(file_descriptor));
        fflush(stdout);
    }
    else if (has_mem_flag == -1)
    {

        printf("%s", recvMessage(file_descriptor));
        fflush(stdout);
    }
    else if (has_memkill_flag == 1)
    {

        printf("%s", recvMessage(file_descriptor));
        fflush(stdout);
    }
    if (shutdown(file_descriptor, SHUT_RDWR) == -1)
    {
        perror("shutdown()"); // Debug
        return 1;
    }
    fflush(stdout);
    close(file_descriptor);
    return 0;
}