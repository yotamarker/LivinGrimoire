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


//**IMPLEMENTATION**//

//AbsDictionaryDB

//Mutatable

//APSay:Mutatable
APSay::APSay(int repetitions, const std::string& szParam) : Mutable(), param(szParam) {
	if (repetitions > 10) {
		repetitions = 10;
	}
	at = repetitions;
}

bool APSay::completed() {
	return at < 1;
}

std::string APSay::action(const std::string& ear, const std::string& skin, const std::string& eye) {
	std::string axnStr = "";
	if (at > 0) {

		if (!lgUtil::iequals(ear, param)) {
			axnStr = param;
			at--;
		}
	}
	return axnStr;
}

//Algorithm
Algorithm::Algorithm(std::vector<std::shared_ptr<Mutable>>& vecAlgParts) {
	algParts.insert(algParts.begin(), vecAlgParts.begin(), vecAlgParts.end());
}

Algorithm::Algorithm(std::initializer_list<std::shared_ptr<Mutable>> vecAlgParts) {
	for (auto& word : vecAlgParts) {
		algParts.push_back(word);
	}
}

std::vector<std::shared_ptr<Mutable>>& Algorithm::getAlgParts() {
	return algParts;
}

int Algorithm::getSize() {
	return static_cast<int>(algParts.size());
}

//APVerbatim:APVerbatim

APVerbatim::APVerbatim(std::initializer_list<std::string> initlist) : Mutable() {
	for (auto& word : initlist) {
		sentences.push(word);
	}
}

APVerbatim::APVerbatim(std::vector<std::string>& list1) : Mutable() {
	for (auto& word : list1) {
		sentences.push(word);
	}
}

std::string APVerbatim::action(const std::string& ear, const std::string& skin, const std::string& eye) {
	if (!sentences.empty()) {
		std::string szNext = sentences.front();
		sentences.pop();
		return szNext;
	}

	return "";
}

bool APVerbatim::completed() {
	return sentences.empty();
}

//Kokoro
Kokoro::Kokoro(std::shared_ptr<AbsDictionaryDB> lpAbsDictionaryDB) {
	grimoireMemento = lpAbsDictionaryDB;
}

std::string Kokoro::getEmot() {
	return emot;
}

void Kokoro::setEmot(const std::string& szEmot) {
	emot = szEmot;
}

AbsDictionaryDB* Kokoro::getGrimoireMemento() {
	return grimoireMemento.get();
}

void Kokoro::setGrimoireMemento(std::shared_ptr<AbsDictionaryDB> absDictionaryDB) {
	grimoireMemento = absDictionaryDB;
}

//Neuron
Neuron::Neuron() {}

void Neuron::insertAlg(int priority, const std::shared_ptr<Algorithm> alg) {
	defcons[priority].push(alg);
}

std::shared_ptr<Algorithm> Neuron::getAlg(int defcon) {
	if (defcons.at(defcon).empty())
		return nullptr;
	std::shared_ptr<Algorithm> alg = defcons.at(defcon).front();
	defcons.at(defcon).pop();
	return alg;
}

//Skill
bool Skill::pendingAlgorithm() {
	// is an algorithm pending?
	return outAlg != nullptr;
}

// in skill algorithm building shortcut methods:
void Skill::setVerbatimAlg(int priority, std::initializer_list<std::string> sayThis) {
	// build a simple output algorithm to speak std::string by std::string per think cycle
	// uses varargs param
	std::shared_ptr<APVerbatim> mut = std::make_shared<APVerbatim>(sayThis);
	std::initializer_list<std::shared_ptr<Mutable>> list = { mut };
	outAlg = std::make_shared<Algorithm>(list);
	outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
}

void Skill::setSimpleAlg(std::initializer_list<std::string> sayThis) {
	// based on the setVerbatimAlg method
	// build a simple output algorithm to speak std::string by std::string per think cycle
	// uses varargs param
	std::shared_ptr<APVerbatim> mut = std::make_shared<APVerbatim>(sayThis);
	std::initializer_list<std::shared_ptr<Mutable>> list = { mut };
	outAlg = std::make_shared<Algorithm>(list);
	outpAlgPriority = 4; // 1->5 1 is the highest algorithm priority
}

void Skill::setVerbatimAlgFromList(int priority, std::vector<std::string> sayThis) {
	// build a simple output algorithm to speak std::string by std::string per think cycle
	// uses list param
	std::shared_ptr<APVerbatim> mut = std::make_shared<APVerbatim>(sayThis);
	std::initializer_list<std::shared_ptr<Mutable>> list = { mut };
	outAlg = std::make_shared<Algorithm>(list);
	outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
}

void Skill::algPartsFusion(int priority, std::initializer_list<std::shared_ptr<Mutable>> algParts) {
	// build a custom algorithm out of a chain of algorithm parts(actions)
	outAlg = std::make_shared<Algorithm>(algParts);
	outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
}

// extraction of skill algorithm to run (if there is one)
void Skill::output(Neuron* neuron) {
	if (outAlg != nullptr) {
		neuron->insertAlg(outpAlgPriority, outAlg);
		outpAlgPriority = -1;
		outAlg = nullptr;
	}
}

void Skill::setKokoro(Kokoro* lpKokoro) {
	// use this for telepathic communication between different chobits objects
	kokoro = lpKokoro;
}

std::string Skill::skillNotes(std::string& param) {
	return "notes unknown";
}


//DiSysOut
void DiSysOut::input(const std::string& ear, const std::string& skin, const std::string& eye) {
	if (!ear.empty() && ear.find("#") == std::string::npos) {
		std::cout << ear << std::endl;
	}
}

//DiHelloWorld:Skill
void DiHelloWorld::input(const std::string& ear, const std::string& skin, const std::string& eye) {
	if (ear == "hello") {
		setVerbatimAlg(4, { "hello world" }); // 1->5 1 is the highest algorithm priority
	}
}

std::string DiHelloWorld::skillNotes(std::string& param) {
	if (param == "notes") {
		return "plain hello world skill";
	}
	else if ("triggers" == param) {
		return "say hello";
	}
	return "note unavailable";
}

//Cerabellum
int Cerabellum::getAt() {
	return at;
}

void Cerabellum::advanceInAlg() {
	if (incrementAt) {
		incrementAt = false;
		at++;
		if (at == fin) {
			bIsActive = false;
		}
	}
}

std::string Cerabellum::getEmot() {
	return emot;
}

bool Cerabellum::setAlgorithm(const std::shared_ptr<Algorithm> algorithm) {
	if (!bIsActive && (!algorithm->getAlgParts().empty())) {
		alg = algorithm;
		at = 0;
		fin = algorithm->getSize();
		bIsActive = true;
		emot = alg->getAlgParts().at(at)->myName(); // updated line
		return false;
	}
	return true;
}

bool Cerabellum::isActive() {
	return bIsActive;
}

std::string Cerabellum::act(const std::string& ear, const std::string& skin, const std::string& eye) {
	std::string axnStr = "";
	if (!bIsActive) {
		return axnStr;
	}
	if (at < fin) {
		std::shared_ptr<Mutable> mut = alg->getAlgParts().at(at);
		axnStr = mut->action(ear, skin, eye);
		emot = alg->getAlgParts().at(at)->myName();
		if (alg->getAlgParts().at(at)->completed()) {
			incrementAt = true;
		}
	}
	return axnStr;
}

void Cerabellum::deActivation() {
	bIsActive = bIsActive && !alg->getAlgParts().at(at)->algKillSwitch;
}

//Fusion
Fusion::Fusion() {}

std::string Fusion::getEmot() {
	return emot;
}

void Fusion::loadAlgs(Neuron* neuron) {
	for (int i = 0; i < ceraArr.size(); i++) {
		if (!ceraArr[i].isActive()) {
			std::shared_ptr<Algorithm> temp = neuron->getAlg(i);
			if (temp != nullptr) {
				ceraArr[i].setAlgorithm(temp);
			}
		}
	}
}

std::string Fusion::runAlgs(const std::string& ear, const std::string& skin, const std::string& eye) {
	std::string result;
	for (int i = 0; i < 5; i++) {
		if (!ceraArr[i].isActive()) {
			continue;
		}
		result = ceraArr[i].act(ear, skin, eye);
		ceraArr[i].advanceInAlg();
		emot = ceraArr[i].getEmot();
		ceraArr[i].deActivation(); // deactivation if Mutatable.algkillswitch = true
		return result;
	}
	emot.clear();
	return result;
}

//Chobits
Chobits::Chobits() : isThinking(false), fusion(std::make_unique<Fusion>()), neuron(std::make_unique<Neuron>()) {
	kokoro = std::make_shared<Kokoro>(std::make_shared<AbsDictionaryDB>());
}

Chobits::~Chobits() {
	clearSkills();
}

void Chobits::setDataBase(std::shared_ptr<AbsDictionaryDB> absDictionaryDB) {
	kokoro->setGrimoireMemento(absDictionaryDB);
}

Chobits* Chobits::addSkill(Skill* skill) {
	// add a skill (builder design patterned func))
	if (isThinking) return this;
	skill->setKokoro(kokoro.get());
	dClasses.push_back(skill);
	return this;
}

Chobits* Chobits::addSkillAware(Skill* skill) {
	skill->setKokoro(kokoro.get());
	awareSkills.push_back(skill);
	return this;
}

void Chobits::clearSkills() {
	if (isThinking) return;

	for_each(dClasses.begin(), dClasses.end(), [](Skill* lpSkill) { delete lpSkill; });
	dClasses.clear();
}

void Chobits::addSkills(std::initializer_list<Skill*> skills) {
	if (isThinking) return;

	for (auto skill : skills) {
		skill->setKokoro(kokoro.get());
		dClasses.push_back(skill);
	}
}

void Chobits::removeSkill(Skill* skill) {
	if (isThinking) return;
	if (skill != nullptr) {
		auto it = find(dClasses.begin(), dClasses.end(), skill);
		if (it != dClasses.end())
			delete* it;
		dClasses.erase(it);
	}
}

bool Chobits::containsSkill(Skill* skill) {
	return (skill != nullptr && find(dClasses.begin(), dClasses.end(), skill) != dClasses.end());
}

std::string Chobits::think(const std::string& ear, const std::string& skin, const std::string& eye) {
	isThinking = true;
	for (Skill* dCls : dClasses) {
		inOut(dCls, ear, skin, eye);
	}
	isThinking = false;
	for (Skill* dCls : awareSkills) {
		inOut(dCls, ear, skin, eye);
	}
	fusion->loadAlgs(neuron.get());
	return fusion->runAlgs(ear, skin, eye);
}

std::string Chobits::getSoulEmotion() {
	return fusion->getEmot();
}

std::shared_ptr<Kokoro> Chobits::getKokoro() {
	return kokoro;
}

void Chobits::setKokoro(std::shared_ptr<Kokoro> lpKokoro) {
	kokoro = lpKokoro;
}


Fusion* Chobits::getFusion() {
	return fusion.get();
}

std::vector<std::string> Chobits::getSkillList(std::vector<std::string>& result) {
	for (Skill* skill : dClasses) {
		result.push_back(skill->myName());
	}
	return result;
}

std::string Skill::myName() {
	// Returns the class name
	return typeid(this).name();
}

void Chobits::inOut(Skill* dClass, const std::string& ear, const std::string& skin, const std::string& eye) {
	dClass->input(ear, skin, eye); // new
	dClass->output(neuron.get());
}

//Brain
Brain::Brain() {
	logicChobit = std::make_unique<Chobits>();
	hardwareChobit = std::make_unique<Chobits>();
	ear = std::make_unique<Chobits>();
	skin = std::make_unique<Chobits>();
	eye = std::make_unique<Chobits>();
	imprintSoul(logicChobit->getKokoro(), { hardwareChobit.get(), ear.get(), skin.get(), eye.get() });
}

Chobits* Brain::getLogicChobit() {
	return logicChobit.get();
}

Chobits* Brain::getHardwareChobit() {
	return hardwareChobit.get();
}

std::string Brain::getEmotion() {
	return emotion;
}

std::string Brain::getLogicChobitOutput() {
	return logicChobitOutput;
}

void Brain::doIt(const std::string& ear, const std::string& skin, const std::string& eye) {
	logicChobitOutput = logicChobit->think(ear, skin, eye);
	emotion = logicChobit->getSoulEmotion();
	// case: hardware skill wishes to pass info to logical chobit
	hardwareChobit->think(logicChobitOutput, skin, eye);
}

void Brain::addLogicalSkill(Skill* skill) {
	logicChobit->addSkill(skill);
}

void Brain::addHardwareSkill(Skill* skill) {
	hardwareChobit->addSkill(skill);
}

void Brain::addEarSkill(Skill* skill) {
	ear->addSkill(skill);
}

void Brain::addSkinSkill(Skill* skill) {
	skin->addSkill(skill);
}

void Brain::addEyeSkill(Skill* skill) {
	eye->addSkill(skill);
}

void Brain::think() {
	doIt(ear->think("", "", ""), skin->think("", "", ""), eye->think("", "", ""));
}

void Brain::think(const std::string& keyIn) {
	if (!keyIn.empty()) {
		// handles typed inputs(keyIn)
		doIt(keyIn, "", "");
	}
	else {
		// accounts for sensory inputs
		doIt(ear->think("", "", ""), skin->think("", "", ""), eye->think("", "", ""));
	}
}

void Brain::imprintSoul(std::shared_ptr<Kokoro> kokoro, std::initializer_list<Chobits*> args) {
	for (auto arg : args) {
		arg->setKokoro(kokoro);
	}
}

//Main
int main() {
	Brain b1;
	b1.addLogicalSkill(new DiHelloWorld());
	b1.addLogicalSkill(new DiHelloWorld());
	b1.addHardwareSkill(new DiSysOut());
	b1.think("hello");
	b1.getLogicChobit()->clearSkills();
	b1.addLogicalSkill(new DiHelloWorld());
	b1.doIt("", "", "");
	b1.doIt("hello", "", "");
}
