#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

void println(const char *message) {
    printf(message);
    printf("\n");
}

void customStrncpy(char *dest, const char *src, size_t n)
{
    strncpy(dest, src, n);
    // Ensure the destination string is null-terminated
    dest[n] = '\0';
}

// Check to see if a keyword argument passed matches, returns 1 if keyword is valid and matches, 0 if keyword is valid and doesn't match, -1 if there is an error
/*
argv - the actual keyword argument string passed
check_val - the value to compare the argument to
return_val - the value to return from parent function
inc - the value to increment the return value by if function returns true
*/
int check_kwarg(char *argv, char *check_val, int *return_val, int inc) {
    char kwarg_str[14];
    int bool_val;
    // Check to see if the first part of the keyword argument is equal to the passed val
    customStrncpy(kwarg_str, argv + 2, 8);
    if (strcmp(kwarg_str, check_val) == 0) {
        // Check to see if the last part of the keyword (lowercase) is equal to true or false
        customStrncpy(kwarg_str, argv + 10, 5);
        if(strlen(kwarg_str) != 4 && strlen(kwarg_str) != 5) {
            return -1;
        }
        for(int i = 0; i < 5; i++) {
            kwarg_str[i] = tolower(kwarg_str[i]);
        }
        if (strcmp(kwarg_str, "true") == 0) {
            *return_val += inc;
            return 1;
        }
        else if (strcmp(kwarg_str, "false") == 0) {
            return 1;
        }
        else  {
            return -1;
        }
    }
    // Return 0 here because the keyword COULD be correct, just not the one we're checking
    return 0;
}

// Open file passed as an argument, and return false if file cannot be found
/*
fptr - file pointer to load file into
file_path - file path to use to open file
file type - either "key" or "file to encrypt/decrypt". used in error message
*/
bool check_file(FILE **fptr, char *file_path, char * file_type) {
    *fptr = fopen(file_path, "rb");
    if(*fptr == NULL) {
        printf("The %s could not be found. Please supply a different file name,", file_type);
        printf("\n");
        return false;
    }
    return true;
}

// Returns an integer that determines which optional arguments have been passed
// Returns -1 if there is an error
/*
argc - number of arguments passed
argv - array of arguments passed
key - file pointer to load key file into
file - file pointer to load file into
*/
int validate_input(int argc, char *argv[], FILE **key, FILE **file) {
    int return_val = 0;
    int decrypt_val;
    int inplace_val;

    const char *unknown_format_str = "Unknown format, optional args must begin in \"--\" and seperate argument and value with \"=\"";
    const char *invalid_value_str = "Keyword arguments must be either \"true\", or \"false\"";

    if (argc < 3) {
        println("Too few inputs");
        return -1;
    }

    // Check to see if the path_to_file and _path_to_key filepaths are valid
    if (!check_file(key, argv[2], "key") || 
        !check_file(file, argv[1], "file to encrypt/decrypt")) {
        fclose(*key);
        fclose(*file);
        return -1;
    }

    // Parse the keyword arguments, if they exist
    /*
    00 - not inplace or decrypt
    01 - inplace but not decrypt
    10 - decrypt but not inplace
    11 - both inplace and decrypt 
    */
    if (argc > 3) {
        for(int i=3; i < argc; i++) {
            // Wrong input length means input cannot be correct format
            if (strlen(argv[i]) < 2 || strlen(argv[i]) > 15) {
                println(unknown_format_str);
                return -1;
            }
            // Input does not start with "--"
            if (argv[i][0] != '-' || argv[i][1] != '-') {
                println(unknown_format_str);
                return -1;
            }

            // Check formatting of inplace and decrypt values
            inplace_val = check_kwarg(argv[i], "inplace=", &return_val, 1);
            decrypt_val = check_kwarg(argv[i], "decrypt=", &return_val, 2);

            // If either is -1, the value after the "=" sign is invalid
            if(inplace_val == -1 || decrypt_val == -1) {
                println(invalid_value_str);
                return -1;
            }
            // Unknown argument - value before "=" sign is not decrypt or inplace
            else if (inplace_val == 0 && decrypt_val == 0) {
                println("Unknown optional argument.");
                return -1;
            }
        }
    }
    return return_val;
}



int main(int argc, char *argv[]) {
    char help_str[88] = "Enigma.exe <path_to_file> <path_to_key> (--decrypt=<false/true> --inplace=<false/true>)";
    FILE *key;
    FILE *file;

    char *rotors;
    long file_length;

    int val = validate_input(argc, argv, &key, &file);
    if (val == -1) {
        printf(help_str);
        return 1;
    }

    // Read key file
    fseek(key, 0, SEEK_END);
    file_length = ftell(key);
    rewind(key);
    if(file_length % 256 != 0) {
        println("Key file has invalid format. File length must be a multiple of 256.");
        fclose(key);
        fclose(file);
        return 1;
    }

    rotors = (char *)malloc(file_length * sizeof(char));
    fread(rotors, sizeof(char), file_length, key);

    // Perform closing actions
    free(rotors);
    fclose(key);
    fclose(file);
    return 0;
    }