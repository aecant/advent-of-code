import { readFileSync } from 'fs'
import assert from 'assert'
import { sum } from 'lodash'

const input = readFileSync('input.txt').toString()

const calories = input
    .split('\n\n')
    .map(line =>
        line
            .split('\n')
            .map(Number)
            .reduce((a, b) => a + b, 0),
    )
    .sort((a, b) => b - a)

const maxCalories = calories[0]
const top3 = calories.slice(0, 3)

assert.equal(71124, maxCalories)
assert.equal(204639, sum(top3))
