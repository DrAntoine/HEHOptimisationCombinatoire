#include <fstream>
#include <iostream>
#include<vector>
#include "Experience.h"

Experience::Experience(std::string fileName) {
	std::ifstream myFile(fileName);
	if (myFile) {
		std::cout << "fichier trouvable" << std::endl;
		myFile >> this->nbCouvertures;
		myFile >> this->nbSlots;
		std::vector <int> nbImpressionsCouvertures(this->nbCouvertures);
		this->nbImpressions = &nbImpressionsCouvertures;
		for (int i = 0; i<this->nbCouvertures; i++) {
			myFile >> nbImpressionsCouvertures[i];
		};
		myFile >> this->coutFeuille;
		myFile >> this->coutPlaque;
	}
	else {
		std::cout << "fichier introuvable" << std::endl;
	}
};
Experience::~Experience() {
	//delete this->nbImpressions;
};
