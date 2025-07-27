//
//  main.swift
//  LivinGrimoireSwiftV1
//
//  Created by moti barski
//
import Foundation



let brain = Brain()
    .chained(DiHelloWorld())
    .chained(DiTime())
    .chained(DiSysOut())

let brainQueue = DispatchQueue(label: "com.livingrimoire.queue")
let tickInterval: TimeInterval = 2

func brainLoop() {
    while true {
        let message = readLine() ?? ""
        brain.think(message)

        if message.lowercased() == "exit" {
            print("Exiting...")
            exit(0)
        }
    }
}

func tickLoop() {
    var nextTick = Date().timeIntervalSince1970
    while true {
        let now = Date().timeIntervalSince1970
        if now >= nextTick {
            brainQueue.async {
                brain.think()
            }
            nextTick += tickInterval
        }
        Thread.sleep(forTimeInterval: 0.01)
    }
}

DispatchQueue.global().async { tickLoop() }
brainLoop()
