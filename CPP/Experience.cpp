#include <fstream>
#include <iostream>
#include "Experience.h"

Experience::Experience(std::string fileName) {
	ifstream myFile(fileName);
	if (myfile) {
		std::cout << "hello world" << std::endl;
	}
	else {
		std::cout <<"fichier introuvable"<<std::endl;
	}
}
