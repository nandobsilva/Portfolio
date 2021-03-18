using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace IndexSequence16S
{
    // Alert messages used in the program
    class Alerts
    {
        static public void Alert_1(string filename)
        {
            Console.WriteLine("Error, file {0} not found.", filename);
            Console.WriteLine("Please, check if the fasta file name is correct.");
            Console.WriteLine();
        }

        static public void Alert_2(string paramenter)
        {
            Console.WriteLine("Error, invalid file name: '{0}'", paramenter);
        }

        static public void Alert_3(int sequenceCount, string indexFileName)
        {
            Console.WriteLine("Number of sequences found: {0}", sequenceCount);
            Console.WriteLine("File {0} created.", indexFileName);
        }

        static public void Alert_4()
        {
            Console.WriteLine();
            Console.WriteLine("Please enter the correct parameters for the program.");
            Console.WriteLine();
            Console.WriteLine("EXAMPLE: 'IndexSequence16s 16S.fasta 16S.index'");
        }

    }

    // Validation code used in the program in order to fulfill the assingment's requeriments 
    class Validation
    {
        // Validate parameters and return alerts to the user
        static public bool Validation_1(string parameter1)
        {
            if (!File.Exists(parameter1))
            {
                Alerts.Alert_1(parameter1);
                return false;
            }
            return true;
        }

        static public bool ValidationInput(string[] input)
        {
            if (input.Length != 2)
            {
                Alerts.Alert_4();
                return false;
            }
            else if (!File.Exists(input[0]))
            {
                Alerts.Alert_1(input[0]);
                return false;
            }
            else
            {
                return true;
            }
        }
    }

    class Function
    {
        // Combine element from 2 different lists and create a new list with those elements.
        static public List<string> CombineList(List<string> sequence_1, List<int> sequence_2, List<int> sequence_3)
        {
            List<string> combinedList = new List<string>();
           
            if (sequence_1.Count == sequence_2.Count)
            {
                for(int i = 0; i < sequence_1.Count; i++)
                {
                    string offset = sequence_2[i].ToString();
                    string combinedString = sequence_1[i] + " " + offset + " " + sequence_3[i];

                    combinedList.Add(combinedString);
                }
                return combinedList;
            }
            return combinedList;
        }

        //Write information from a list (search result)  to a txt file
        static public void WriteToFile(string indexFileName, List<string> sequence)
        {
            FileStream createFile = new FileStream(indexFileName, FileMode.Create, FileAccess.Write);
            StreamWriter writeFile = new StreamWriter(createFile);
            foreach (string elem in sequence)
            {
                writeFile.WriteLine(elem);
            }
            writeFile.Close();
            createFile.Close();
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.Clear();
            string[] input = args;                                      // Hold the parameters entered by the user
            bool check = false;                                         // Used to check if the arguments enterd by the user is valid
            check = Validation.ValidationInput(input);                  // Validate the arguments entered by the user

            if(check)
            {
                string fileName = args[0];                              // Name of the fasta file entered by the user
                string indexFileName = args[1];                         // Name of the index file entered by the user
                int sequenceCount = 0;                                  // Hold the number of sequences found
                int offSetCounter = 0;                                  // Used to control the offset of  each sequence found
                string line;                                            // Used to hold information from the readed line
                List<string> sequenceId = new List<string>();           // Used to hold all sequences ID found in the fasta file 
                List<int> sequenceOffSet = new List<int>();             // Used to hold all offset numbers found in the fast file
                List<int> lineList = new List<int>();                   // Used to hold the line which the sequence was found
                List<int> sequenceSizeList= new List<int>();            // Used to hold the size of each line plus the DNA code.
                List<int> sizeLineFile = new List<int>();               // Used to hold the size of each line of the file
                int lineCounter = 1;                                    // Identify the line in which the sequece was found
                int lineSize = 0;                                       // Identify the size of the sequence plus DNA 
                int numLinesFile = 0;                                   // Count the number of sequences found in the file 
                int sequenceFoundLine = 0;                              // Identify the line where the sequence was found

                FileStream newFile = new FileStream(fileName, FileMode.Open, FileAccess.Read);
                StreamReader readFile = new StreamReader(newFile);
                line = readFile.ReadLine();
                
                while (line != null)
                {
                    string[] fileLine = line.Split(' ');
                    numLinesFile++;
                    
                    if (line.Contains('>'))                          // Define the offset of each sequenceID in the file
                    {
                        foreach (char element in line)
                        {
                            if (element == '>')
                            {
                                sequenceOffSet.Add(offSetCounter);
                                lineList.Add(lineCounter);
                                sequenceFoundLine++;
                            }
                        }
                        offSetCounter = offSetCounter + line.Length + 1;
                        lineCounter++;

                        for (int i = 0; i < fileLine.Length; i++)   // Add sequenceID in a list
                        {
                            if (fileLine[i][0] == '>')
                            {
                                sequenceCount = sequenceCount + 1;
                                fileLine[i] = fileLine[i].Replace(">", "");
                                sequenceId.Add(fileLine[i]);
                            }
                        }
                        lineSize = lineSize + line.Length + 1;      //  Define the length of the sequence plus the dna sequence 
                    }
                    else
                    {
                        offSetCounter = offSetCounter + line.Length + 1;
                        lineCounter++;
                        lineSize = lineSize + line.Length + 1;      //  Define the length of the sequence plus the dna sequence 

                        for (int i = 0; i < sequenceFoundLine ; i++)
                        {
                            sequenceSizeList.Add(lineSize);             
                        }
                        sequenceFoundLine = 0;
                        lineSize = 0;                              // Reset the line size to calculate the next sequence offset and length
                    }
                    line = readFile.ReadLine();
                }
                readFile.Close();
                newFile.Close();

                // Create the file with sequence offset and length size 
                List<string> sequenceWithOffSet = Function.CombineList(sequenceId, sequenceOffSet, sequenceSizeList);
                try
                {
                    Function.WriteToFile(indexFileName, sequenceWithOffSet);
                    Alerts.Alert_3(sequenceCount, indexFileName);
                }
                catch
                {
                    Alerts.Alert_2(indexFileName);
                }
            }
        }
    }
}
