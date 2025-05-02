#include "LivinGrimoire.h"

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
