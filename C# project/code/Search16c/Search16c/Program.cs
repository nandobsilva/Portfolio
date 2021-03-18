using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Text.RegularExpressions;

namespace Search16s
{
    // Alert messages used in the program
    class Alerts
    {
        static public void Alert_1()
        {
            string fileNameExample = "16s.fasta";
            Console.WriteLine();
            Console.WriteLine("Please enter the correct parameters for the search.");
            Console.WriteLine();
            Console.WriteLine("SEARCH OPTIONS.");
            Console.WriteLine();
            Console.WriteLine("Search level 1: '-level1 {0} 273 10'.", fileNameExample);
            Console.WriteLine("Search level 2: '-level2 {0} NR_115365.1'.", fileNameExample);
            Console.WriteLine("Search level 3: '-level3 {0} query.txt result.txt'.", fileNameExample);
            Console.WriteLine("Search level 4: '-level4 {0} 16s.index query.txt results.txt'", fileNameExample);
            Console.WriteLine("Search level 5: '-level5 {0} CTGGTACGGTVAA'.", fileNameExample);
            Console.WriteLine("Search level 6: '-level6 {0} Streptomyces'.", fileNameExample);
            Console.WriteLine("Search level 7: '-level7 {0} ACTG*GTAC*AC'.", fileNameExample);
        }

        static public void Alert_2(string filename)
        {
            Console.WriteLine("Error, file {0} not found.", filename);
            Console.WriteLine();
        }

        static public void Alert_3(double parameter)
        {
            Console.WriteLine("Error, parameter '{0}' exceed the number of DNA lines in the file.", parameter);
        }

        static public void Alert_4(double totalDna, string fileName)
        {
            Console.WriteLine("There are '{0}' lines of DNA in the file '{1}'.", totalDna, fileName);
        }

        static public void Alert_5(string parameter)
        {
            Console.WriteLine("Error, invalid search parameter '{0}'.", parameter);
            Console.WriteLine();
        }

        static public void Alert_5(string parameter1, string parameter2)
        {
            Console.WriteLine("Error, invalid search parameters '{0}' '{1}'.", parameter1, parameter2);
            Console.WriteLine();
        }

        static public void Alert_6(string fileName)
        {
            Console.WriteLine("Please, enter a positive number bigger than '0' in the followed format.");
            Console.WriteLine();
            Console.WriteLine("EXAMPLES:");
            Console.WriteLine("1) 'search16c -level1 {0} 1 1'", fileName);
            Console.WriteLine("2) 'search16c -level1 {0} 5000 10'", fileName);
        }

        static public void Alert_7(string parameter)
        {
            Console.WriteLine("Sequence '{0}' not found.", parameter);
            Console.WriteLine("Please, check if you are using the correct parameters for the search.");
        }

        static public void Alert_8(string paramenter)
        {
            Console.WriteLine("Error, invalid file name: '{0}'", paramenter);
        }
        static public void Alert_9(string parameter)
        {
            Console.WriteLine("Sequence '{0}' not found.", parameter);
        }
    }

    // Validation code used in the program in order to fulfill the assingment's requeriments 
    class Validation
    {
        // Validate parameters for search level 1 and return alerts to the user
        static public bool ValidationLevel_1(string fileName, string parameter1, string parameter2)
        {
            int param1;
            int param2;
            bool success1 = Int32.TryParse(parameter1, out param1);
            bool success2 = Int32.TryParse(parameter2, out param2);

            if ((!success1 || param1 <= 0) && (success2 && param2 > 0))
            {
                Alerts.Alert_5(parameter1);
            }
            else if ((!success2 || param2 <= 0) && (success1 && param1 > 0))
            {
                Alerts.Alert_5(parameter2);
            }
            else if ((!success2 && !success1) || (param1 <= 0 && param2 <= 0))
            {
                Alerts.Alert_5(parameter1, parameter2);
            }

            if (!success1 || !success2 || param1 <= 0 || param2 <= 0)
            {
                Alerts.Alert_6(fileName);
                return false;
            }
            return true;
        }

        // Validate parameters for search level 3 and return alerts to the user
        static public bool ValidationLevel_3(string parameter1)
        {
            if (!File.Exists(parameter1))
            {
                Alerts.Alert_2(parameter1);
                return false;
            }
            return true;
        }

        // Validate parameters for search level 4 and return alerts to the user
        static public bool ValidationLevel_4(string[] argms)
        {
            bool result = true;
            for (int i = 1; i < 4; i++)
            {
                result = ValidationLevel_3(argms[i]);
                if (result == false){break;}
            }
            return result;
        }

        // Validate the input parameters and return alerts to the user
        static public bool ValidationInput(string[] input)
        {
            if (
                 (input.Length <= 2 || input.Length > 5) ||
                 (input.Length == 3 && (input[0] != "-level2" && input[0] != "-level5" && input[0] != "-level6" && input[0] != "-level7")) ||
                 (input.Length == 4 && (input[0] != "-level1" && input[0] != "-level3")) ||
                 (input.Length == 5 && input[0] != "-level4")
               )
            {
                Alerts.Alert_1();
                return false;
            }
            else if (!File.Exists(input[1]))
            {
                Alerts.Alert_2(input[1]);
                return false;
            }
            else if (input[0] == "-level1")
            {
                return Validation.ValidationLevel_1(input[1], input[2], input[3]);
            }
            else if (input[0] == "-level3")
            {
                return Validation.ValidationLevel_3(input[2]);
            }
            else if (input[0] == "-level4")
            {
                return ValidationLevel_4(input);
            }
            else if (input[0] == "-level2" || input[0] == "-level5" || input[0] == "-level6" || input[0] == "-level7")
            {
                return true;  
            }
            return false;
        }

        //  Print error messages for sequences lines that exceed the number of the lines in the file (Search level 1)
        static public void ValidationOutput(string fileName, string searchParameter1, string searchParameter2, double countDna)
        {
            double totalDna = countDna / 2;
            double lineRequested = Convert.ToInt32(searchParameter1);
            double sequeceRequested = Convert.ToInt32(searchParameter2);
            if (totalDna < lineRequested)
            {
                Alerts.Alert_3(lineRequested);
                Alerts.Alert_4(totalDna, fileName);
            }
            else if (totalDna < lineRequested + sequeceRequested - 1)
            {
                Console.WriteLine();
                Alerts.Alert_3(sequeceRequested);
                Alerts.Alert_4(totalDna, fileName);
            }
        }
        // Write to file sequences found and print message for sequences not found (Search level 3)
        static public void ValidationOutput(string searchParameter2, List<string> query, int[] queryFound, string[] sequencesFound)
        {
            try
            {
                Function.WriteToFile(searchParameter2, sequencesFound);
                for (int i = 0; i < queryFound.Length; i++)
                {
                    if (queryFound[i] == 0)
                    {
                        Alerts.Alert_9(query[i]);
                    }
                }
            }
            catch
            {
                Alerts.Alert_8(searchParameter2);
            }
        }
    }

    class Search
    {
        //Search level 1 code  
        static public void SearchLevel_1(string element, double countDna, string searchParameter1, string searchParameter2)
        {
            int lineStartSurch = Convert.ToInt32(searchParameter1);
            int numSequence = Convert.ToInt32(searchParameter2);

            if (countDna >= (lineStartSurch * 2) - 1 && countDna <= (lineStartSurch + numSequence - 1) * 2)

            {
                Console.WriteLine(element);
            }
        }
        //Search level 2 code
        static public bool SearchLevel_2(string element, double countDna, string sequence)
        {
            if (countDna % 2 != 0)
            {
                string[] wordList = element.Split(' ');
                sequence = ">" + sequence;
                for (int index = 0; index < wordList.Length; index++)
                {
                    if (wordList[index] == sequence)
                    {
                        Console.WriteLine(element);
                        return true;
                    }
                }
            }
            return false;
        }
        //Search level 3 code  
        static public string SearchLevel_3(string element, double countDna, string sequence)
        {
            if (countDna % 2 != 0)
            {
                string[] queryList = element.Split(' ');
                sequence = ">" + sequence;
                for (int index = 0; index < queryList.Length; index++)
                {
                    if (queryList[index] == sequence)
                    {
                        return element;
                    }
                }
            }
            return null;
        }
        //search level 4 code
        static public void SearchLevel_4(string fileName, string parameter1, string parameter2, string resultFile)
        {
            List<string> indexList = Function.CreateListFromFile(parameter1); // List whith the sequeces plus offset
            List<string> queryList = Function.CreateListFromFile(parameter2); // List with the sequeces to be searched
            List<string> sequenceFound = new List<string>();
            List<int> sequenceOffSet = new List<int>();                       // Hold the list of offset to be used in the direct access
            List<int> sequenceSize = new List<int>();                         // Hold the sequence size to be used in the direct access
            List<string> sequenceDnaList = new List<string>();                // Hold the sequence found to be used in writed file and erro alerts

            // Split the data from the file index and put in lists
            for (int q = 0; q < queryList.Count; q++)
            {
                for (int i = 0; i < indexList.Count; i++)
                {
                    string[] sequenceId = indexList[i].Split(' ');
                    if (queryList[q] == sequenceId[0])
                    {
                        int offSet = Int32.Parse(sequenceId[1]);
                        int size = Int32.Parse(sequenceId[2]);
                        sequenceFound.Add(sequenceId[0]);
                        sequenceOffSet.Add(offSet);
                        sequenceSize.Add(size);
                    }
                }
            }
            // Search the file using direct access
            using (FileStream fs = new FileStream(fileName, FileMode.Open, FileAccess.Read))
            {
                for (int i = 0; i < sequenceFound.Count; i++)
                {
                    byte[] bytes = new byte[sequenceSize[i] - 1];
                    fs.Seek(sequenceOffSet[i], SeekOrigin.Begin);
                    fs.Read(bytes, 0, sequenceSize[i] - 1);         // Get data from the file
                    string sequenceDna = Encoding.Default.GetString(bytes);
                    if (!sequenceDnaList.Contains(sequenceDna))     // Avoid duplicate data in the file
                    {
                        sequenceDnaList.Add(sequenceDna);
                    }
                }
            }
            // Write sequences found in a file
            try
            {
                Function.WriteToFile(resultFile, sequenceDnaList.ToArray());
                // Send alerts to the user informing the sequeces not found
                for (int i = 0; i < queryList.Count; i++)
                {
                    if (!sequenceFound.Contains(queryList[i]))
                    {
                        Alerts.Alert_9(queryList[i]);
                    }
                }
            }
            catch  // If 'resulFile' name is invalid
            {
                Alerts.Alert_8(resultFile);
            }  
           
        }
        //Search level 5 code
        static public int SearchLevel_5(string fileName, string parameter1, double countDna, string line)
        {
            if (countDna % 2 == 0)
            {
                if (line.Contains(parameter1))
                {
                    double lineFound = countDna;
                    string sequenceLine = Function.searchFile(fileName, lineFound - 2);
                    string[] splitSequenceLine = sequenceLine.Split(' ');
                    for (int i = 0; i < splitSequenceLine.Length; i++)
                    {
                        if (splitSequenceLine[i][0] == '>')
                        {
                            string sequence = splitSequenceLine[i];
                            sequence = sequence.Remove(0, 1);
                            Console.WriteLine(sequence);
                        }
                    }
                    return 1;
                }
            }
            return 0;
        }
        //Search level 6 code
        static public int SearchLevel_6(string parameter1, double countDna, string line)
        {
            int printControl = 0;      // Used to control the alert when information is not found
            if (countDna % 2 != 0)
            {
                string sequenceLine = line;
                string[] splitSequenceLine = sequenceLine.Split('>');
                for (int i = 0; i < splitSequenceLine.Length; i++)
                {
                    string[] sequence = splitSequenceLine[i].Split(' ');
                    if (sequence.Contains(parameter1))
                        foreach (string word in sequence)
                        {
                            if (word == parameter1)
                            {
                                Console.WriteLine(sequence[0]);
                                printControl = 1;
                            }
                        }
                }
            }
            return printControl;

        }
        //Search level 7 code
        static public void SearchLevel_7(string fileName, double countDna)
        {
            double lineFound = countDna;
            string sequenceLine = Function.searchFile(fileName, countDna - 2);
            string[] splitSequenceLine = sequenceLine.Split(' ');
            for (int i = 0; i < splitSequenceLine.Length; i++)
            {
                if (splitSequenceLine[i][0] == '>')
                {
                    string sequence = splitSequenceLine[i];
                    sequence = sequence.Remove(0, 1);
                    Console.WriteLine(sequence);
                }
            }
        }
    }

    class Function
    {
        //Count number of lines in a file
        static public int CounLine(string fileName)
        {
            FileStream newQuery = new FileStream(fileName, FileMode.Open, FileAccess.Read);
            StreamReader readFile = new StreamReader(newQuery);
            string recordIn;
            recordIn = readFile.ReadLine();
            int numLine = 0;
            while (recordIn != null)
            {
                numLine++;
                recordIn = readFile.ReadLine();
            }
            readFile.Close();
            newQuery.Close();
            return numLine;
        }
        //Write information from a list (search result)  to a txt file
        static public void WriteToFile(string fileName, string[] sequence)
        {
            FileStream createFile = new FileStream(fileName, FileMode.Create, FileAccess.Write);
            StreamWriter writeFile = new StreamWriter(createFile);
            foreach (string elem in sequence)
            {
                writeFile.WriteLine(elem);
            }
            writeFile.Close();
            createFile.Close();
        }
        // Return a specified line from a file .
        static public string searchFile(string fileName, double lineNumber)
        {
            FileStream newFile = new FileStream(fileName, FileMode.Open, FileAccess.Read);
            StreamReader readFile = new StreamReader(newFile);
            string recordIn = readFile.ReadLine();
            double line = 0;

            while (recordIn != null)
            {
                if (lineNumber == line)
                {
                    return recordIn;
                }
                line++;
                recordIn = readFile.ReadLine();
            }
            readFile.Close();
            newFile.Close();
            return null;
        }
        // Read a file and return a list with each line of the file
        static public List<string> CreateListFromFile(string fileName)
        {
            List<string> result = new List<string>();

            FileStream newFile = new FileStream(fileName, FileMode.Open, FileAccess.Read);
            StreamReader readFile = new StreamReader(newFile);
            string recordIn = readFile.ReadLine();

            while (recordIn != null)
            {
                result.Add(recordIn);
                recordIn = readFile.ReadLine();
            }
            readFile.Close();
            newFile.Close();
            return result;
        }
    }

    class Program
    {
        //###################################  MAIN PROGRAM   #########################################
        static void Main(string[] args)
        {
            Console.Clear();
            string[] input = args;
            bool check;
            //Check if all input variables are valid. If valid check = true.
            check = Validation.ValidationInput(input);

            if (check)
            {
                // Variables to hold the arguments passed by the user
                string searchType = input[0];
                string fileName = input[1];
                string fullpath = fileName;
                string searchParameter1 = input[2];
                string searchParameter2;
                if (input.Length <= 3)
                {
                    searchParameter2 = "";
                }
                else
                {
                    searchParameter2 = input[3];
                }
                // Variables used to print and save sequence in the search type: level2 and level3
                bool printControl = false;
                int numLines = 0;
                bool searchFound = false;                                    //Used to print message for sequences not found 
                List<string> query = new List<string>();
                if (searchType == "-level3")
                {
                    numLines = Function.CounLine(searchParameter1);          // Count the number of line in a file
                    query = Function.CreateListFromFile(searchParameter1);   // Save sequences found in a list to be saved in a file (-level3) 
                }
                int[] queryFound = new int[numLines];                        //Used to print message for sequences not found (-level3) 
                string[] sequencesFound = new string[numLines * 2];          //Hold the sequences found in a list (-level3)

                // Open file (input[1]) and execute the search program.
                FileStream newFile = new FileStream(fullpath, FileMode.Open, FileAccess.Read);
                StreamReader readFile = new StreamReader(newFile);
                string recordIn = readFile.ReadLine();
                double countDna = 0;
                int indexNumber = 0;

                // Search 4 using direct access
                if (searchType == "-level4")
                {
                    Search.SearchLevel_4(fileName, searchParameter1, searchParameter2, input[4]);
                }
                else
                {
                    while (recordIn != null)
                    {
                        string line = recordIn;
                        countDna = countDna + 1;

                        if (searchType == "-level1")
                        {
                            Search.SearchLevel_1(line, countDna, searchParameter1, searchParameter2);
                        }
                        else if (searchType == "-level2")
                        {
                            if (printControl)
                            {
                                Console.WriteLine(line);
                                printControl = false;
                            }
                            printControl = Search.SearchLevel_2(line, countDna, searchParameter1);
                            if (printControl) { searchFound = true; }
                        }
                        else if (searchType == "-level3")
                        {
                            // Lines which will be included in the file
                            if (printControl)
                            {
                                sequencesFound[indexNumber] = line;
                                indexNumber++;
                                printControl = false;
                            }
                            bool controlLine = false; // Controle the line that will be save in the array.
                            for (int i = 0; i < query.Count; i++)
                            {
                                string lineFound = Search.SearchLevel_3(line, countDna, query[i]);
                                // Lines which will be included in the file
                                if (lineFound != null && controlLine == false)
                                {
                                    sequencesFound[indexNumber] = line;
                                    indexNumber++;
                                    printControl = true;
                                    controlLine = true;
                                }
                                // Control the sequences that were not found to return an alert to the user
                                if (lineFound != null)
                                {
                                    queryFound[i] = 1;
                                }
                            }
                        }
                        else if (searchType == "-level5")
                        {
                            int count = 0;  
                            int sequenceFound = Search.SearchLevel_5(fileName, searchParameter1, countDna, line);
                            count = count + sequenceFound;
                            if (count > 0)
                            {
                                searchFound = true;
                            }
                        }
                        else if (searchType == "-level6")
                        {
                            int count = 0; 
                            int sequenceFound = Search.SearchLevel_6(searchParameter1, countDna, line);
                            count = count + sequenceFound;
                            if (count > 0)
                            {
                                searchFound = true;
                            }
                        }
                        else if (searchType == "-level7")
                        {
                            string pattern = searchParameter1.Replace("*", "[A-Z]*");  // Create a regex pattern
                            pattern = "^" + pattern + "$";                             // Create a regex pattern
                            Match patterFound = Regex.Match(line, pattern);            // Compare the pattern to each line of the file
                            if (patterFound.Success)
                            {
                                Search.SearchLevel_7(fileName, countDna);
                                searchFound = true;
                            }
                        }
                        recordIn = readFile.ReadLine();
                    }
                    readFile.Close();
                    newFile.Close();
                }

                //  Print error messages for sequences lines that exceed the number of the lines in the file
                if (searchType == "-level1")
                {
                    Validation.ValidationOutput(fileName, searchParameter1, searchParameter2, countDna);
                }
                // Write to file seqeunces found and print message for sequences not found
                if (searchType == "-level3")
                {
                    Validation.ValidationOutput(searchParameter2, query, queryFound, sequencesFound);
                }
                //  Print message for sequences not found in search -level2, 5, 6 and 7.
                if (
                    (searchType == "-level2" && searchFound != true) ||
                    (searchType == "-level5" && searchFound != true) ||
                    (searchType == "-level6" && searchFound != true) ||
                    (searchType == "-level7" && searchFound != true)
                   )
                {
                    Alerts.Alert_7(searchParameter1);
                }
            }
        }
    }
}