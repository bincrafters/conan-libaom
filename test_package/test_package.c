#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "aom/aom_codec.h"

int main(int argc, char **argv) {

  printf("Libaom version is %s \n", aom_codec_version_str());

  return EXIT_SUCCESS;
}