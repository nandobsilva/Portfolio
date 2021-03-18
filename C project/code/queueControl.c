/*#################################################################################################################

    Written by Fernando Barbosa Silva - n10338471
    October, 2020

/#################################################################################################################*/

#include "Declarations.h"

struct node_queue *head = NULL;
struct node_queue *tail = NULL;

//-----------------------------------------------------------------------------------------------------------------
// Add a node to the pool
//-----------------------------------------------------------------------------------------------------------------

void enqueue(int clientfd, char message[])
{
    struct node_queue *newnode = (struct node_queue *)malloc(sizeof(struct node_queue));
    newnode->clientfp = clientfd;
    newnode->message = message;
    newnode->next = NULL;
      if (tail == NULL)
    {
        head = newnode;
    }
    else
    {
        tail->next = newnode;
    }
    tail = newnode;
    
}

//-----------------------------------------------------------------------------------------------------------------
// Remove a node from the pool - returns the pointer to a clientfd, if there is one to get
//-----------------------------------------------------------------------------------------------------------------
int dequeue(int *clientfp, char *message)
{
    if (head == NULL)
    {
        return -1;
    }
    else
    {
        struct node_queue *temp = head;
        *clientfp = head->clientfp;
        char msg_result[1024];
        strcpy(msg_result, head->message);
        strcpy(message, msg_result);
        head = head->next;
        free(temp); 
        if (head == NULL)
        {
            tail = NULL;
        }
        return 0;
    }
}
//-----------------------------------------------------------------------------------------------------------------
// Print all itens in the list
//-----------------------------------------------------------------------------------------------------------------
void printList()
{
    struct node_queue *temp = head;
    while (temp != NULL)
    {
        printf("| %d ", temp->clientfp);
        temp = temp->next;
    }
    printf("\n");
}

//------------------------------------------------------------------------------------------------------------------
// Free all nodes in the queue  *(Not working properly)
//------------------------------------------------------------------------------------------------------------------

// Free memory allocated for the list
void freeQueueMemory()
{
    struct node_queue *temp = head;
    while (head != NULL)
    {
        temp = head;
        head = head->next;
        free(temp);
    }
}
