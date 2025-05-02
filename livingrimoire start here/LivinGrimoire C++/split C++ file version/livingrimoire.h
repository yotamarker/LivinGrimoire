#ifndef LIVIN_GRIMOIRE_H
#define LIVIN_GRIMOIRE_H
#pragma once
#include <iostream>
#include <cctype>
#include <string>
#include <typeinfo>
#include <cctype>
#include <algorithm>
#include <vector>
#include <memory>
#include <map>
#include <unordered_map>
#include <array>
#include <queue>
#include <cstdarg>


//Utility functions
namespace lgUtil {
	//Source: https://stackoverflow.com/questions/11635/case-insensitive-std::string-comparison-in-c
	inline bool ichar_equals(char a, char b) {
		return std::tolower(static_cast<unsigned char>(a)) ==
			std::tolower(static_cast<unsigned char>(b));
	}

	//Case insensitive comparison
	inline bool iequals(const std::string& a, const std::string& b) {
		return std::equal(a.begin(), a.end(), b.begin(), b.end(), ichar_equals);
	}
}

//AbsDictionaryDB

class AbsDictionaryDB {
public:
	inline void save(const std::string& key, const std::string& value) {
		// save to DB (override me)
	}

	inline std::string load(const std::string& key) {
		// override me
		return "null";
	}
};

//Mutatable
class Mutable {
public:
	Mutable() : algKillSwitch(false) {}
	virtual ~Mutable() {}

	virtual std::string action(const std::string& ear, const std::string& skin, const std::string& eye) = 0;
	virtual bool completed() = 0;
	std::string myName() {
		// Returns the class name
		return typeid(this).name();
	}

	bool algKillSwitch;
};

//APSay:Mutatable
class APSay : public Mutable {
public:
	APSay(int repetitions, const std::string& param);

	virtual bool completed();
	virtual std::string action(const std::string& ear, const std::string& skin, const std::string& eye);

protected:
	std::string param;
private:

	int at;
};

//APVerbatim:Mutatable
class APVerbatim : public Mutable {
public:
	APVerbatim(std::initializer_list<std::string> initlist);
	APVerbatim(std::vector<std::string>& list1);

	virtual std::string action(const std::string& ear, const std::string& skin, const std::string& eye);
	virtual bool completed();
private:
	std::queue<std::string> sentences;
};

//Algorithm
// a step-by-step plan to achieve a goal
class Algorithm {
public:
	Algorithm(std::vector<std::shared_ptr<Mutable>>& algParts);
	Algorithm(std::initializer_list<std::shared_ptr<Mutable>> algParts);

	std::vector<std::shared_ptr<Mutable>>& getAlgParts();
	int getSize();
private:
	std::vector<std::shared_ptr<Mutable>> algParts;
};

//Kokoro
class Kokoro {
public:
	Kokoro(std::shared_ptr<AbsDictionaryDB> absDictionaryDB);
	~Kokoro() {}

	std::string getEmot();

	void setEmot(const std::string& emot);

	AbsDictionaryDB* getGrimoireMemento();
	void setGrimoireMemento(std::shared_ptr<AbsDictionaryDB> absDictionaryDB);

	std::unordered_map<std::string, std::string> toHeart;

private:
	std::string emot;
	std::shared_ptr<AbsDictionaryDB> grimoireMemento;
};

//Neuron
class Neuron {
public:
	Neuron();

	void insertAlg(int priority, const std::shared_ptr<Algorithm> alg);
	std::shared_ptr<Algorithm> getAlg(int defcon);

private:
	std::array<std::queue<std::shared_ptr<Algorithm>>, 6> defcons;
};

//Skill
class Skill {
public:
	Skill() : outAlg(nullptr), outpAlgPriority(-1), kokoro(nullptr) {}
	virtual ~Skill() {}

	// skill triggers and algorithmic logic
	virtual void input(const std::string& ear, const std::string& skin, const std::string& eye) = 0;
	virtual std::string skillNotes(std::string& param);

	bool pendingAlgorithm();
	void output(Neuron* neuron);
	void setKokoro(Kokoro* kokoro);
	std::string myName();
protected:
	void setVerbatimAlg(int priority, std::initializer_list<std::string> sayThis);
	void setSimpleAlg(std::initializer_list<std::string> sayThis);
	void setVerbatimAlgFromList(int priority, std::vector<std::string> sayThis);
	void algPartsFusion(int priority, std::initializer_list<std::shared_ptr<Mutable>> algParts);

	Kokoro* kokoro; // consciousness, shallow ref class to enable interskill communications
	std::shared_ptr<Algorithm> outAlg; // skills output
	int outpAlgPriority; // defcon 1->5
private:
};

//DiSysOut
class DiSysOut : public Skill {
public:
	virtual void input(const std::string& ear, const std::string& skin, const std::string& eye);
};

//DiHelloWorld:Skill
class DiHelloWorld : public Skill {
public:
	DiHelloWorld() : Skill() {}

	virtual void input(const std::string& ear, const std::string& skin, const std::string& eye);
	virtual std::string skillNotes(std::string& param);
};

//Cerabellum
class Cerabellum {
public:
	Cerabellum() : fin(0), at(0), incrementAt(false), bIsActive(false), alg(nullptr) {}
	~Cerabellum() {}

	int getAt();
	void advanceInAlg();
	std::string getEmot();
	bool setAlgorithm(const std::shared_ptr<Algorithm> algorithm);
	bool isActive();
	std::string act(const std::string& ear, const std::string& skin, const std::string& eye);


	void deActivation();

private:
	std::shared_ptr<Algorithm> alg;
	int fin;
	int at;
	bool incrementAt;
	bool bIsActive;
	std::string emot;

};

//Fusion
class Fusion {
public:
	Fusion();
	~Fusion() {};

	std::string getEmot();
	void loadAlgs(Neuron* neuron);
	std::string runAlgs(const std::string& ear, const std::string& skin, const std::string& eye);


private:
	std::string emot;
	std::array<Cerabellum, 5> ceraArr;
};

//Thinkable

//Chobits
class Chobits {
public:
	Chobits();
	~Chobits();

	void setDataBase(std::shared_ptr<AbsDictionaryDB> absDictionaryDB);
	Chobits* addSkill(Skill* skill);
	Chobits* addSkillAware(Skill* skill);
	void clearSkills();
	void addSkills(std::initializer_list<Skill*> skills);
	void removeSkill(Skill* skill);
	bool containsSkill(Skill* skill);
	std::string think(const std::string& ear, const std::string& skin, const std::string& eye);
	std::string getSoulEmotion();
	std::shared_ptr<Kokoro> getKokoro();
	void setKokoro(std::shared_ptr<Kokoro> kokoro);
	Fusion* getFusion();
	std::vector<std::string> getSkillList(std::vector<std::string>&);
protected:
	void inOut(Skill* dClass, const std::string& ear, const std::string& skin, const std::string& eye);

	std::vector<Skill*> dClasses;
	std::unique_ptr<Fusion> fusion;
	std::unique_ptr<Neuron> neuron;
	std::shared_ptr<Kokoro> kokoro; // consciousness
	bool isThinking;
private:
	std::vector<Skill*> awareSkills;
};

//Brain
class Brain {
public:
	Brain();
	~Brain() {}

	Chobits* getLogicChobit();
	Chobits* getHardwareChobit();
	std::string getEmotion();
	std::string getLogicChobitOutput();
	void doIt(const std::string& ear, const std::string& skin, const std::string& eye);
	void addLogicalSkill(Skill* skill);
	void addHardwareSkill(Skill* skill);
	void addEarSkill(Skill* skill);
	void addSkinSkill(Skill* skill);
	void addEyeSkill(Skill* skill);

	void think();
	void think(const std::string& keyIn);
private:
	void imprintSoul(std::shared_ptr < Kokoro> kokoro, std::initializer_list<Chobits*> args);

	std::string emotion;
	std::string logicChobitOutput;
	std::unique_ptr<Chobits> logicChobit;
	std::unique_ptr<Chobits> hardwareChobit;

	std::unique_ptr<Chobits> ear;
	std::unique_ptr<Chobits> skin;
	std::unique_ptr<Chobits> eye;
};
#endif // LIVIN_GRIMOIRE_H

