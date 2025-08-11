//
//  Personality.swift
//  LivinGrimoireSwiftV1
//
//  Created by moti barski on 11/08/2025.
//

import Foundation


func loadPersonality(_ brain: Brain) {
    brain.addSkill(DiHelloWorld())
    brain.addSkill(DiTime())
    brain.addSkill(DiSysOut())
    // brain.chained(DiHelloWorld()).chained(DiTime()).chained(DiSysOut())
}
