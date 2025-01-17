#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

// Check to see if a string input is equivalent to 'true'
bool boolean_inp(char inp[]) {
    char check_val[4] = "true";
    if(strlen(inp) < 4) {
        return false;
    }
    for (int i = 0; i < 4; i++) {
        if (tolower(inp[i]) != check_val[i]) {
            return false;
        }
    }

    return true;
}

//return {i.split('=')[0]:i.split('=')[1] for i in kwargs}
char ** convert_kwargs(int argc, char *argv[]) {
    char ** kwargs;
    for(int i=3; i < argc; i++) {
        printf(argv[i]);
    }
    return kwargs;
}

char * validate_input(int argc, char *argv[]) {
    char ** kwargs;
    if (argc < 2) {
        return "Too few inputs";
    }
    else {
        if (argc > 2) {
            kwargs = convert_kwargs(argc, argv);
        }
        return "Unknown format, optional args must begin in \"--\" and seperate argument and value with \"=\"";
    }
}



int main(int argc, char *argv[]) {
  char help_str[88] = "Enigma.exe <path_to_file> <path_to_key> (--decrypt=<false/true> --inplace=<false/true>)";
  char * err_str = validate_input(argc, argv);
  if (strlen(err_str) > 0) {
    printf(err_str);
    printf("\n");
    printf(help_str);
    return 1;
  }
  return 0;
}