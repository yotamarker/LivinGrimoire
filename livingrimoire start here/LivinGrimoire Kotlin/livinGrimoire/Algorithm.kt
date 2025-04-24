package livinGrimoire

import java.util.*

// a step-by-step plan to achieve a goal
class Algorithm(val algParts: ArrayList<Mutatable>) {
    // Secondary constructor for varargs
    constructor(vararg algParts: Mutatable) : this(ArrayList(algParts.toList()))

    // Property to get the size of algParts
    val size: Int
        get() = algParts.size
}


