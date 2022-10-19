#include <iostream>
#include "Experience.h"

int main(){
	int nombreGeneration = 1500;
	std::string filePath = "../../Dataset-Dev/I001.in";
	Experience experience(filePath);

	std::cout << "nbcouvertures : " << experience.nbCouvertures << std::endl<<"nbslot : "<< experience.nbSlots<<std::endl<<"nbimpression : "<<experience.nbImpressions<<std::endl<<"cout feuille : "<<experience.coutFeuille<<std::endl<<"cout plaque : "<<experience.coutPlaque<<std::endl;
}