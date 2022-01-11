import Solution.CommandFunctions
import kotlin.io.path.Path
import kotlin.io.path.readLines

data class Command(val type: String, val qty: Int)
data class State(val x: Int, val y: Int, val aim: Int = 0)

typealias CommandFunctions = Map<String, (State, Int) -> State>

val commandFunctionsPart1: CommandFunctions = mapOf(
    "forward" to { s, qty -> s.copy(x = s.x + qty) },
    "down" to { s, qty -> s.copy(y = s.y + qty) },
    "up" to { s, qty -> s.copy(y = s.y - qty) },
)

val commandFunctionsPart2: CommandFunctions = mapOf(
    "forward" to { s, qty -> s.copy(x = s.x + qty, y = s.y + s.aim * qty) },
    "down" to { s, qty -> s.copy(aim = s.aim + qty) },
    "up" to { s, qty -> s.copy(aim = s.aim - qty) }
)

fun parseCommands(filename: String): List<Command> {
    fun parseCommand(line: String) =
        line.split(' ').let { (type, qty) -> Command(type, qty.toInt()) }

    return Path(filename).readLines().map(::parseCommand)
}

fun finalState(commands: List<Command>, commandFunctions: CommandFunctions): State {
    var state = State(0, 0)
    commands.forEach {
        state = commandFunctions[it.type]!!(state, it.qty)
    }
    return state
}

val commands = parseCommands("input.txt")

val finalPosPart1 = finalState(commands, commandFunctionsPart1)
val finalPosPart2 = finalState(commands, commandFunctionsPart2)

check(finalPosPart1.x * finalPosPart1.y == 1480518)
check(finalPosPart2.x * finalPosPart2.y == 1282809906)
