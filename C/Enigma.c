#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

void customStrncpy(char *dest, const char *src, size_t n)
{
    strncpy(dest, src, n);
    // Ensure the destination string is null-terminated
    dest[n] = '\0';
}

// Check to see if a string input is equivalent to true or false, or an invalid value
int boolean_inp(char inp[]) {
    char check_val[6];

    if(strlen(inp) != 4 && strlen(inp) != 5) {
        return -1;
    }

    customStrncpy(check_val, inp, 5);
    for(int i = 0; i < 5; i++) {
        check_val[i] = tolower(check_val[i]);
    }

    if (strcmp(check_val, "true") == 0) {
        return 1;
    }
    else if (strcmp(check_val, "false") == 0) {
        return 0;
    }
    else {
        return -1;
    }
}




// A string of length 2 if the inputs are valid
// If there is an error with the inputs, return a string array of size 1 with the error string
char * validate_input(int argc, char *argv[]) {
    int return_val = 0;
    int bool_val;
    char kwarg_str[14];

    char unknown_format_str[89] = "Unknown format, optional args must begin in \"--\" and seperate argument and value with \"=\"";
    char invalid_value_str[51] = "Keyword arguments must be either \"true\", or \"false\"";

    if (argc < 2) {
        return "Too few inputs";
    }
    // Parse the keyword arguments, if they exist
    /*
    00 - not inplace or decrypt
    01 - inplace but not decrypt
    10 - decrypt but not inplace
    11 - both inplace and decrypt 
    */
    if (argc > 2) {
        for(int i=3; i < argc; i++) {
            // Wrong input length means input cannot be correct format
            if (strlen(argv[i]) < 2 || strlen(argv[i]) > 15) {
                return unknown_format_str;
            }
            // Input does not start with "--"
            if (argv[i][0] != '-' || argv[i][1] != '-') {
                return unknown_format_str;
            }
            // Check for inplace argument
            customStrncpy(kwarg_str, argv[i] + 2, 8);
            if (strcmp(kwarg_str, "inplace=") == 0) {
                customStrncpy(kwarg_str, argv[i] + 11, 5);
                bool_val = boolean_inp(kwarg_str);
                if (bool_val == 1) {
                    return_val += 1;
                }
                else if (bool_val == -1) {
                    return invalid_value_str;
                }
            }
            // Check for decrypt argument
            else if (strcmp(kwarg_str, "decrypt=") == 0){
                customStrncpy(kwarg_str, argv[i] + 11, 5);
                bool_val = boolean_inp(kwarg_str);
                if (bool_val == 1) {
                    return_val += 2;
                }
                else if (bool_val == -1) {
                    return invalid_value_str;
                }
            }
            // Unknown argument
            else {
                return "Unknown optional argument";
            }


        }
    }
    return return_val + '0';
}



int main(int argc, char *argv[]) {
  char help_str[88] = "Enigma.exe <path_to_file> <path_to_key> (--decrypt=<false/true> --inplace=<false/true>)";
  char * err_str = validate_input(argc, argv);
  if (strlen(err_str) > 1) {
    printf(err_str);
    printf("\n");
    printf(help_str);
    return 1;
  }
  return 0;
}