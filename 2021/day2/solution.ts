import { PathOrFileDescriptor, readFileSync } from 'fs'
import assert from 'assert'

interface Command {
    type: string
    qty: number
}

interface State {
    x: number
    y: number
    aim: number
}

type CmdFunctions = Record<string, (s: State, qty: number) => State>

const cmdFunctionsPart1: CmdFunctions = {
    forward: (s, qty) => ({ ...s, x: s.x + qty }),
    down: (s, qty) => ({ ...s, y: s.y + qty }),
    up: (s, qty) => ({ ...s, y: s.y - qty }),
}

const cmdFunctionsPart2: CmdFunctions = {
    forward: (s, qty) => ({ ...s, x: s.x + qty, y: s.y + s.aim * qty }),
    down: (s, qty) => ({ ...s, aim: s.aim + qty }),
    up: (s, qty) => ({ ...s, aim: s.aim - qty }),
}

function parseCommands(filename: PathOrFileDescriptor): Command[] {
    function parseCommand(line: String): Command {
        const [type, qty] = line.split(' ')
        return { type, qty: parseInt(qty) }
    }

    return readFileSync(filename, 'utf-8').split('\n').map(parseCommand)
}

function finalState(commands: Command[], cmdFunctions: CmdFunctions) {
    let state = { x: 0, y: 0, aim: 0 }
    for (const cmd of commands) {
        state = cmdFunctions[cmd.type](state, cmd.qty)
    }
    return state
}

const commands = parseCommands('input.txt')

const finalPosPart1 = finalState(commands, cmdFunctionsPart1)
const finalPosPart2 = finalState(commands, cmdFunctionsPart2)

assert.equal(1480518, finalPosPart1.x * finalPosPart1.y)
assert.equal(1282809906, finalPosPart2.x * finalPosPart2.y)
