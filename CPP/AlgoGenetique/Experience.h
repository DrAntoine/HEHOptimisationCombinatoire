#pragma once
#include<vector>
class Experience {
public:
	Experience(std::string fileName);
	~Experience();
	int nbCouvertures;
	int nbSlots;
	std::vector<int>* nbImpressions;
	float coutFeuille;
	float coutPlaque;
private:
	//int nbCouvertures;
	//int nbSlots;
	//std::vector<int>* nbImpressions;
	//float coutFeuille;
	//float coutPlaque;

};

