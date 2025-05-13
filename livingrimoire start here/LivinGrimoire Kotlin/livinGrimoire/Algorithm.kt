package livinGrimoire

import java.util.*

// a step-by-step plan to achieve a goal
class Algorithm(val algParts: ArrayList<AlgPart>) {
    // Secondary constructor for varargs
    constructor(vararg algParts: AlgPart) : this(ArrayList(algParts.toList()))

    // Property to get the size of algParts
    val size: Int
        get() = algParts.size
}


