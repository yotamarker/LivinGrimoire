#include "LivinGrimoire.h"

//APSay:Mutatable
APSay::APSay(int repetitions, const std::string& szParam) : AlgPart(), param(szParam) {
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
Algorithm::Algorithm(std::vector<std::shared_ptr<AlgPart>>& vecAlgParts) {
	algParts.insert(algParts.begin(), vecAlgParts.begin(), vecAlgParts.end());
}

Algorithm::Algorithm(std::initializer_list<std::shared_ptr<AlgPart>> vecAlgParts) {
	for (auto& word : vecAlgParts) {
		algParts.push_back(word);
	}
}

std::vector<std::shared_ptr<AlgPart>>& Algorithm::getAlgParts() {
	return algParts;
}

int Algorithm::getSize() {
	return static_cast<int>(algParts.size());
}

//APVerbatim:APVerbatim

APVerbatim::APVerbatim(std::initializer_list<std::string> initlist) : AlgPart() {
	for (auto& word : initlist) {
		sentences.push(word);
	}
}

APVerbatim::APVerbatim(std::vector<std::string>& list1) : AlgPart() {
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

void Kokoro::setGrimoireMemento(std::shared_ptr<AbsDictionaryDB> absDictionaryDB) {
	grimoireMemento = absDictionaryDB;
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
	std::initializer_list<std::shared_ptr<AlgPart>> list = { mut };
	outAlg = std::make_shared<Algorithm>(list);
	outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
}

void Skill::setSimpleAlg(std::initializer_list<std::string> sayThis) {
	// based on the setVerbatimAlg method
	// build a simple output algorithm to speak std::string by std::string per think cycle
	// uses varargs param
	std::shared_ptr<APVerbatim> mut = std::make_shared<APVerbatim>(sayThis);
	std::initializer_list<std::shared_ptr<AlgPart>> list = { mut };
	outAlg = std::make_shared<Algorithm>(list);
	outpAlgPriority = 4; // 1->5 1 is the highest algorithm priority
}

void Skill::setVerbatimAlgFromList(int priority, std::vector<std::string> sayThis) {
	// build a simple output algorithm to speak std::string by std::string per think cycle
	// uses list param
	std::shared_ptr<APVerbatim> mut = std::make_shared<APVerbatim>(sayThis);
	std::initializer_list<std::shared_ptr<AlgPart>> list = { mut };
	outAlg = std::make_shared<Algorithm>(list);
	outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
}

void Skill::algPartsFusion(int priority, std::initializer_list<std::shared_ptr<AlgPart>> algParts) {
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

std::string DiSysOut::skillNotes(std::string& param) {
	if (param == "notes") {
		return "console print skill";
	}
	else if ("triggers" == param) {
		return "prints any string input";
	}
	return "note unavailable";
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

void Cerabellum::setAlgorithm(const std::shared_ptr<Algorithm> algorithm) {
	if (!bIsActive && (!algorithm->getAlgParts().empty())) {
		alg = algorithm;
		at = 0;
		fin = algorithm->getSize();
		bIsActive = true;
		emot = alg->getAlgParts().at(at)->myName(); // updated line
	}
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
		std::shared_ptr<AlgPart> mut = alg->getAlgParts().at(at);
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
Chobits::Chobits() : isThinking(false),algTriggered(false), fusion(std::make_unique<Fusion>()), neuron(std::make_unique<Neuron>()) {
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

void Chobits::addContinuousSkill(Skill* skill) {
	skill->setKokoro(kokoro.get());
	ctsSkills.push_back(skill);
}

void Chobits::addSkillAware(Skill* skill) {
	skill->setKokoro(kokoro.get());
	awareSkills.push_back(skill);
}

void Chobits::clearSkills() {
	if (isThinking) return;

	for_each(dClasses.begin(), dClasses.end(), [](Skill* lpSkill) { delete lpSkill; });
	dClasses.clear();
}

void Chobits::clearContinuousSkills() {
	if (isThinking) return;

	for_each(ctsSkills.begin(), ctsSkills.end(), [](Skill* lpSkill) { delete lpSkill; });
	ctsSkills.clear();
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

void Chobits::removeContinuousSkill(Skill* skill) {
	if (isThinking) return;
	if (skill != nullptr) {
		auto it = find(ctsSkills.begin(), ctsSkills.end(), skill);
		if (it != ctsSkills.end())
			delete* it;
		ctsSkills.erase(it);
	}
}

bool Chobits::containsSkill(Skill* skill) {
	return (skill != nullptr && find(dClasses.begin(), dClasses.end(), skill) != dClasses.end());
}

std::string Chobits::think(const std::string& ear, const std::string& skin, const std::string& eye) {
	algTriggered = false;
	isThinking = true;
	for (Skill* dCls : dClasses) {
		inOut(dCls, ear, skin, eye);
	}
	isThinking = false;
	for (Skill* dCls : awareSkills) {
		inOut(dCls, ear, skin, eye);
	}
	isThinking = true;
	for (Skill* dCls : ctsSkills) {
		inOut(dCls, ear, skin, eye);
	}
	isThinking = false;
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
	dClass->input(ear, skin, eye);
	if (dClass->pendingAlgorithm()) { algTriggered = true; }
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